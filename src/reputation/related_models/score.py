import json

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import JSONField

from utils.models import DefaultModel


class Score(DefaultModel):
    author = models.ForeignKey("user.Author", on_delete=models.CASCADE, db_index=True)
    hub = models.ForeignKey("hub.Hub", on_delete=models.CASCADE, db_index=True)
    score = models.IntegerField(default=0)
    version = models.IntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "author",
            "hub",
        )

    @classmethod
    def get_or_create_score(cls, author, hub, score_version=1):
        try:
            score = cls.objects.get(author=author, hub=hub)
            if score.version != score_version:
                score.version = score_version
                score.score = 0
                score.save()
        except cls.DoesNotExist:
            score = cls(
                author=author,
                hub=hub,
                version=1,
                score=0,
            )
            score.save()

        return score

    @classmethod
    def get_version(cls, author):
        try:
            score_version = (
                cls.objects.filter(author=author).latest("created_date").version
            ) + 1
        except cls.DoesNotExist:
            score_version = 1

        return score_version

    @classmethod
    def update_score(
        cls,
        author,
        hub,
        algorithm_version,
        score_version,
        raw_value_change,
        variable_key,
        object_id,
    ):
        algorithm_variables = AlgorithmVariables.objects.filter(hub=hub).latest(
            "created_date"
        )

        score = cls.get_or_create_score(author, hub, score_version)

        score_change = ScoreChange.create_score_change(
            score,
            algorithm_version,
            algorithm_variables,
            raw_value_change,
            variable_key,
            object_id,
            score_version,
        )

        score.score = score_change.score_after_change
        score.version = score_version
        score.save()

        return score


class ScoreChange(DefaultModel):
    algorithm_version = models.IntegerField(default=1)
    algorithm_variables = models.ForeignKey(
        "reputation.AlgorithmVariables", on_delete=models.CASCADE
    )
    score_after_change = models.IntegerField()
    score_change = models.IntegerField()
    raw_value_change = models.IntegerField()  # change of number of citations or votes.
    changed_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE
    )  # content type of citation or vote.
    changed_object_id = (
        models.PositiveIntegerField()
    )  # id of the paper (with updated citation) or vote.
    changed_object_field = models.CharField(
        max_length=100
    )  # field name of the changed object, citation, upvote.
    variable_counts = JSONField(default=dict)
    # {
    #     "citations": 10,
    #     "votes": 5,
    # }
    score = models.ForeignKey(
        "reputation.Score", on_delete=models.CASCADE, db_index=True
    )
    score_version = models.IntegerField(
        default=1
    )  # version of the score to allow for recalculation.
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)

    @classmethod
    def get_lastest_score_change(
        cls, score, score_version, algorithm_version, algorithm_variables
    ):
        try:
            previous_score_change = cls.objects.filter(
                score=score,
                score_version=score_version,
                algorithm_version=algorithm_version,
                algorithm_variables=algorithm_variables,
            ).latest("created_date")
        except cls.DoesNotExist:
            previous_score_change = None

        return previous_score_change

    def get_object_field(variable_key):
        if variable_key == "citations":
            return "citations"
        elif variable_key == "votes":
            return "vote_type"
        else:
            return None

    def get_content_type(variable_key):
        from discussion.models import Vote  # Lazy import
        from paper.models import Paper  # Lazy import

        if variable_key == "citations":
            return ContentType.objects.get_for_model(Paper)
        elif variable_key == "votes":
            return ContentType.objects.get_for_model(Vote)
        else:
            return None

    @classmethod
    def create_score_change(
        cls,
        score,
        algorithm_version,
        algorithm_variables,
        raw_value_change,
        variable_key,
        object_id,
        score_version,
    ):
        previous_score_change = ScoreChange.get_lastest_score_change(
            score, score_version, algorithm_version, algorithm_variables
        )

        previous_score = 0
        previous_variable_counts = {
            "citations": 0,
            "votes": 0,
        }
        if previous_score_change:
            previous_score = previous_score_change.score_after_change
            previous_variable_counts = previous_score_change.variable_counts

        current_variable_counts = previous_variable_counts
        current_variable_counts[variable_key] = (
            current_variable_counts[variable_key] + raw_value_change
        )

        score_value_change = ScoreChange.calculate_score_change(
            score,
            algorithm_variables,
            algorithm_version,
            variable_key,
            raw_value_change,
        )
        current_rep = previous_score + score_value_change

        field = ScoreChange.get_object_field(variable_key)
        content_type = ScoreChange.get_content_type(variable_key)

        score_change = ScoreChange(
            algorithm_version=algorithm_version,
            algorithm_variables=algorithm_variables,
            score_after_change=current_rep,
            score_change=score_value_change,
            raw_value_change=raw_value_change,
            changed_content_type=content_type,
            changed_object_id=object_id,
            changed_object_field=field,
            variable_counts=current_variable_counts,
            score=score,
            score_version=score_version,
        )
        score_change.save()

        return score_change

    @classmethod
    def calculate_score_change(
        cls,
        score,
        algorithm_variables,
        algorithm_version,
        variable_key,
        raw_value_change,
    ):
        previous_score_change = cls.get_lastest_score_change(
            score, score.version, algorithm_version, algorithm_variables
        )

        previous_total_count = 0

        if previous_score_change:
            previous_total_count = previous_score_change.variable_counts[variable_key]

        prev_rep = 0
        current_rep = 0

        if variable_key == "citations":
            prev_rep = cls.calculate_citation_score_v1(
                previous_total_count,
                algorithm_variables.variables["citations"]["bins"],
            )
            current_rep = cls.calculate_citation_score_v1(
                previous_total_count + raw_value_change,
                algorithm_variables.variables["citations"]["bins"],
            )
        elif variable_key == "votes":
            prev_rep = previous_total_count
            current_rep = previous_total_count + raw_value_change

        return current_rep - prev_rep

    def calculate_citation_score_v1(citation_count, bins):
        rep = 0
        for key, val in bins.items():
            key_tuple = json.loads(key)

            citation_count_curr_bin = max(
                min(citation_count, key_tuple[1]) - key_tuple[0], 0
            )  # Take min of the citation count and the upper bound of the bin range then subtract the lower bound of the bin range and avoid going negative.
            rep += citation_count_curr_bin * val

        return rep


# AlgorithmVariables stores the variables required to calculate the reputation score.
# Currently each upvote is worth 1 point.
class AlgorithmVariables(DefaultModel):
    # {"citations":
    #   {"bins":{(0, 2): 50, (2, 12): 100, (12, 200): 250, (200, 2800): 100}},
    #  "votes": {"value": 1},
    #  "bins": [1000, 10_000, 100_000, 1_000_000]
    # }
    variables = JSONField()
    hub = models.ForeignKey("hub.Hub", on_delete=models.CASCADE, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
