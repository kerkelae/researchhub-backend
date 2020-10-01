from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q, F, Count

from discussion.models import Thread
from discussion.serializers import (
    ThreadSerializer
)

from paper.models import Paper, Vote
from paper.views import PaperViewSet
from paper.serializers import PaperSerializer, HubPaperSerializer
from user.filters import AuthorFilter
from user.models import User, University, Author, Major
from user.permissions import UpdateAuthor
from user.serializers import (
    AuthorSerializer,
    AuthorEditableSerializer,
    UniversitySerializer,
    UserEditableSerializer,
    UserSerializer,
    UserActions,
    MajorSerializer
)

from utils.http import RequestMethods
from utils.permissions import CreateOrUpdateIfAllowed
from utils.throttles import THROTTLE_CLASSES
from datetime import timedelta
from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserEditableSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'get_subscribed': True, 'get_balance': True}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        elif user.is_authenticated:
            return User.objects.filter(id=user.id)
        else:
            return User.objects.none()

    @action(
        detail=False,
        methods=[RequestMethods.GET],
    )
    def leaderboard(self, request):
        """
        Leaderboard serves both Papers and Users
        """
        hub_id = request.GET.get('hub_id')
        if hub_id:
            hub_id = int(hub_id)

        leaderboard_type = request.GET.get('type', 'users')
        """
        createdByOptions can be values:
        1. created_date
        2. published_date
        """
        created_by_options = request.GET.get('dateOption', 'created_date')

        """
        Timeframe can be values:
        1. all_time
        2. today
        3. past_week
        4. past_month
        5. past_year
        """
        timeframe = request.GET.get('timeframe', 'all_time')

        time_filter = {}
        if leaderboard_type == 'papers':
            if created_by_options == 'created_date':
                keyword = 'uploaded_date__gte'
            else:
                keyword = 'paper_publish_date__gte'
        else:
            keyword = 'created_date__gte'

        if timeframe == 'today':
            time_filter = {keyword: timezone.now().date()}
        elif timeframe == 'past_week':
            time_filter = {keyword: timezone.now().date() - timedelta(days=7)}
        elif timeframe == 'past_month':
            time_filter = {keyword: timezone.now().date() - timedelta(days=30)}
        elif timeframe == 'past_year':
            if leaderboard_type == 'papers':
                keyword = 'uploaded_date__year__gte'
            else:
                keyword = 'created_date__year__gte'
            time_filter = {keyword: timezone.now().year}

        items = []
        if leaderboard_type == 'papers':
            serializerClass = HubPaperSerializer
            if hub_id and hub_id != 0:
                items = Paper.objects.exclude(
                    is_public=False,
                ).filter(
                    **time_filter,
                    hubs__in=[hub_id]
                ).order_by('-score')
            else:
                items = Paper.objects.exclude(
                    is_public=False
                ).filter(
                    **time_filter
                ).order_by(
                    '-score'
                )
        elif leaderboard_type == 'users':
            serializerClass = UserSerializer
            if hub_id and hub_id != 0:
                items = User.objects.filter(
                    is_active=True
                ).annotate(
                    hub_rep=Sum(
                        'reputation_records__amount',
                        filter=Q(
                            **time_filter,
                            reputation_records__hubs__in=[hub_id]
                        )
                    )
                ).order_by(F('hub_rep').desc(nulls_last=True))
            else:
                items = User.objects.filter(
                    is_active=True
                ).annotate(
                    hub_rep=Sum(
                        'reputation_records__amount',
                        filter=Q(**time_filter)
                    )
                ).order_by(F('hub_rep').desc(nulls_last=True))
        elif leaderboard_type == 'authors':
            serializerClass = AuthorSerializer
            authors = Author.objects.filter(authored_papers__isnull=False)
            upvotes = Count(
                'authored_papers__vote',
                filter=Q(authored_papers__vote__vote_type=Vote.UPVOTE)
            )
            downvotes = Count(
                'authored_papers__vote',
                filter=Q(authored_papers__vote__vote_type=Vote.DOWNVOTE)
            )
            if hub_id and hub_id != 0:
                authors = authors.filter(authored_papers__hubs=hub_id)

            authors = authors.annotate(
                paper_count=Count('authored_papers'),
                score=upvotes-downvotes
            )

            items = authors.annotate(total_score=F('paper_count') + F('score'))
            items = items.order_by('-total_score')

        page = self.paginate_queryset(items)
        serializer = serializerClass(
            page,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=[RequestMethods.GET],
        permission_classes=[IsAuthenticated]
    )
    def actions(self, request, pk=None):
        user_actions = UserActions(user=request.user)
        page = self.paginate_queryset(user_actions.serialized)
        return self.get_paginated_response(page)

    @action(
        detail=False,
        methods=[RequestMethods.PATCH],
    )
    def has_seen_first_coin_modal(self, request):
        user = request.user
        user = User.objects.get(pk=user.id)
        user.set_has_seen_first_coin_modal(True)
        serialized = UserSerializer(user)
        return Response(serialized.data, status=200)

    @action(
        detail=False,
        methods=[RequestMethods.PATCH],
    )
    def has_seen_orcid_connect_modal(self, request):
        user = request.user
        user = User.objects.get(pk=user.id)
        user.set_has_seen_orcid_connect_modal(True)
        serialized = UserSerializer(user)
        return Response(serialized.data, status=200)


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ('name', 'city', 'state', 'country')
    permission_classes = [AllowAny]


class MajorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ('major', 'major_category')
    permission_classes = [AllowAny]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    filter_class = AuthorFilter
    search_fields = ('first_name', 'last_name')
    permission_classes = [
        IsAuthenticatedOrReadOnly
        & UpdateAuthor
        & CreateOrUpdateIfAllowed
    ]
    throttle_classes = THROTTLE_CLASSES

    def create(self, request, *args, **kwargs):
        '''Override to use an editable serializer.'''
        serializer = AuthorEditableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        '''Override to use an editable serializer.'''
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = AuthorEditableSerializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(
        detail=True,
        methods=['get'],
    )
    def get_authored_papers(self, request, pk=None):
        authors = Author.objects.filter(id=pk)
        if authors:
            author = authors.first()
            authored_papers = author.authored_papers.all()
            page = self.paginate_queryset(authored_papers)
            serializer = PaperSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(status=404)

    @action(
        detail=True,
        methods=['get'],
    )
    def get_user_discussions(self, request, pk=None):
        authors = Author.objects.filter(id=pk)
        if authors:
            author = authors.first()
            user = author.user
            user_discussions = Thread.objects.exclude(
                created_by=None
            ).filter(
                created_by=user
            )
            page = self.paginate_queryset(user_discussions)
            serializer = ThreadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(status=404)

    @action(
        detail=True,
        methods=['get'],
    )
    def get_user_contributions(self, request, pk=None):
        authors = Author.objects.filter(id=pk)
        if authors:
            author = authors.first()
            user = author.user

            prefetch_lookups = PaperViewSet.prefetch_lookups(self)
            user_paper_uploads = Paper.objects.exclude(
                uploaded_by=None
            ).filter(
                uploaded_by=user
            ).prefetch_related(
                *prefetch_lookups
            )

            page = self.paginate_queryset(user_paper_uploads)
            serializer = PaperSerializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            return response
        return Response(status=404)
