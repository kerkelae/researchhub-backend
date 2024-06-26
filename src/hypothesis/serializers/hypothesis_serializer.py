from rest_framework.serializers import ModelSerializer, SerializerMethodField

from discussion.reaction_models import Vote
from discussion.reaction_serializers import (
    DynamicVoteSerializer,
    GenericReactionSerializerMixin,
)
from hub.serializers import DynamicHubSerializer, SimpleHubSerializer
from hypothesis.models import Hypothesis
from note.serializers import DynamicNoteSerializer, NoteSerializer
from researchhub.serializers import DynamicModelFieldSerializer
from researchhub_document.serializers import DynamicUnifiedDocumentSerializer
from user.serializers import (
    AuthorSerializer,
    DynamicAuthorSerializer,
    DynamicUserSerializer,
    UserSerializer,
)
from utils.http import get_user_from_request


class HypothesisSerializer(ModelSerializer, GenericReactionSerializerMixin):
    class Meta:
        model = Hypothesis
        fields = [
            *GenericReactionSerializerMixin.EXPOSABLE_FIELDS,
            "aggregate_citation_consensus",
            "authors",
            "boost_amount",
            "created_by",
            "created_date",
            "discussion_count",
            "full_markdown",
            "hubs",
            "id",
            "from_bounty",
            "from_post",
            "is_removed",
            "note",
            "renderable_text",
            "slug",
            "src",
            "title",
            "unified_document",
            "vote_meta",
        ]
        read_only_fields = [
            *GenericReactionSerializerMixin.READ_ONLY_FIELDS,
            "aggregate_citation_consensus",
            "authors",
            "boost_amount",
            "bounties",
            "created_by",
            "created_date",
            "discussion_count",
            "id",
            "is_removed",
            "note",
            "renderable_text",
            "slug",
            "src",
            "unified_document",
            "vote_meta",
        ]

    aggregate_citation_consensus = SerializerMethodField()
    authors = AuthorSerializer(many=True)
    boost_amount = SerializerMethodField()
    created_by = UserSerializer()
    discussion_count = SerializerMethodField()
    full_markdown = SerializerMethodField()
    hubs = SerializerMethodField()
    vote_meta = SerializerMethodField()
    note = NoteSerializer()
    from_post = SerializerMethodField()

    # GenericReactionSerializerMixin
    promoted = SerializerMethodField()
    user_endorsement = SerializerMethodField()
    user_flag = SerializerMethodField()
    # user_vote = SerializerMethodField()  # NOTE: calvinhlee - deprecate?

    def get_from_post(self, hypothesis):
        if hypothesis.from_bounty:
            from_bounty_item = hypothesis.from_bounty.item
            post = from_bounty_item.posts.first()
            return {
                "post_id": post.id,
                "unified_document_id": from_bounty_item.id,
                "post_slug": post.slug,
                "post_name": post.title,
            }

    def get_aggregate_citation_consensus(self, hypothesis):
        return hypothesis.get_aggregate_citation_consensus()

    def get_discussion_count(self, hypothesis):
        return hypothesis.get_discussion_count()

    def get_full_markdown(self, hypothesis):
        byte_string = hypothesis.src.read()
        full_markdown = byte_string.decode("utf-8")
        return full_markdown

    def get_hubs(self, hypothesis):
        serializer = SimpleHubSerializer(hypothesis.unified_document.hubs, many=True)
        return serializer.data

    def get_boost_amount(self, hypothesis):
        return hypothesis.get_boost_amount()

    def get_vote_meta(self, hypothesis):
        context = self.context
        _context_fields = context.get("hyp_dcs_get_vote_meta", {})
        votes = hypothesis.votes
        user = get_user_from_request(context)
        user_vote = None

        try:
            if user and not user.is_anonymous:
                user_vote = votes.get(created_by=user)
                serializer = DynamicVoteSerializer(
                    user_vote, context=context, **_context_fields
                )
        except Vote.DoesNotExist:
            pass

        return {
            "down_count": votes.filter(vote_type=Vote.DOWNVOTE).count(),
            "up_count": votes.filter(vote_type=Vote.UPVOTE).count(),
            "user_vote": (serializer.data if user_vote is not None else None),
        }


class DynamicHypothesisSerializer(DynamicModelFieldSerializer):
    aggregate_citation_consensus = SerializerMethodField()
    authors = SerializerMethodField()
    created_by = SerializerMethodField()
    discussions = SerializerMethodField()
    discussion_aggregates = SerializerMethodField()
    discussion_count = SerializerMethodField()
    hubs = SerializerMethodField()
    note = SerializerMethodField()
    purchases = SerializerMethodField()
    score = SerializerMethodField()
    unified_document = SerializerMethodField()

    class Meta(object):
        model = Hypothesis
        fields = "__all__"

    def get_aggregate_citation_consensus(self, hypothesis):
        return hypothesis.get_aggregate_citation_consensus()

    def get_authors(self, hypothesis):
        context = self.context
        _context_fields = context.get("hyp_dhs_get_authors", {})
        serializer = DynamicAuthorSerializer(
            hypothesis.authors, context=context, many=True, **_context_fields
        )
        return serializer.data

    def get_created_by(self, hypothesis):
        context = self.context
        _context_fields = context.get("hyp_dhs_get_created_by", {})
        serializer = DynamicUserSerializer(
            hypothesis.created_by, context=context, **_context_fields
        )
        return serializer.data

    def get_discussions(self, hypothesis):
        from researchhub_comment.serializers import DynamicRhThreadSerializer

        context = self.context
        _context_fields = context.get("hyp_dhs_get_discussions", {})
        _select_related_fields = context.get("hyp_dhs_get_discussions_select", [])
        _prefetch_related_fields = context.get("hyp_dhs_get_discussions_prefetch", [])
        serializer = DynamicRhThreadSerializer(
            hypothesis.rh_threads.select_related(
                *_select_related_fields
            ).prefetch_related(*_prefetch_related_fields),
            many=True,
            context=context,
            **_context_fields,
        )
        return serializer.data

    def get_discussion_aggregates(self, hypothesis):
        return hypothesis.rh_threads.get_discussion_aggregates()

    def get_discussion_count(self, hypothesis):
        return hypothesis.get_discussion_count()

    def get_hubs(self, hypothesis):
        context = self.context
        _context_fields = context.get("hyp_dhs_get_hubs", {})
        serializer = DynamicHubSerializer(
            hypothesis.unified_document.hubs,
            many=True,
            context=context,
            **_context_fields,
        )
        return serializer.data

    def get_note(self, hypothesis):
        context = self.context
        _context_fields = context.get("hyp_dhs_get_note", {})
        serializer = DynamicNoteSerializer(
            hypothesis.note, many=True, context=context, **_context_fields
        )
        return serializer.data

    def get_purchases(self, instance):
        from purchase.serializers import DynamicPurchaseSerializer

        context = self.context
        _context_fields = context.get("hyp_dhs_get_purchases", {})
        _select_related_fields = context.get("hyp_dhs_get_purchases_select", [])
        _prefetch_related_fields = context.get("hyp_dhs_get_purchases_prefetch", [])
        serializer = DynamicPurchaseSerializer(
            instance.purchases.select_related(*_select_related_fields).prefetch_related(
                *_prefetch_related_fields
            ),
            many=True,
            context=context,
            **_context_fields,
        )
        return serializer.data

    def get_unified_document(self, hypothesis):
        context = self.context
        _context_fields = context.get("hyp_dhs_get_unified_document", {})
        serializer = DynamicUnifiedDocumentSerializer(
            hypothesis.unified_document, context=context, **_context_fields
        )
        return serializer.data

    def get_score(self, hypothesis):
        return hypothesis.calculate_score()
