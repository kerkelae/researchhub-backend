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
    def get_or_create_score(cls, author, hub):
        try:
            score = cls.objects.get(author=author, hub=hub)
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