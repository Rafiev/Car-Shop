from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from applications.product.models import Car, Comment, Like, Rating, Sale, Save
from applications.product.permissions import IsOwner, IsCommentSaveOwner
from applications.product.serializers import CarSerializer, CarListSerializer, CommentSerializer, RatingSerializer, \
    SaleSerializer, OrderConfirmSerializer, SaveSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CarAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                 GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsOwner]

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):
        like_obj, _ = Like.objects.get_or_create(post_id=pk, owner=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status_of_like = 'liked'
        if not like_obj.like:
            status_of_like = 'unliked'
        return Response({'status': status_of_like})

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(post_id=pk, owner=request.user)
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    permission_classes = [IsOwner]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title']
    ordering_fields = ['created_at']


class CommentAPIView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentSaveOwner]


class SaleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = SaleSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.send_code()
        return Response('Confirm the order by mail!')


class SaleConfirmAPIView(APIView):

    @staticmethod
    def post(request, pk, *args, **kwargs):
        serializer = OrderConfirmSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order_obj = Sale.objects.get(post=pk, owner=request.user)
        order_obj.status = True
        order_obj.save()
        return Response('You have successfully confirmed the order')


class SaveAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    permission_classes = [IsCommentSaveOwner]

    @action(detail=True, methods=['POST'])
    def save_car(self, request, pk, *args, **kwargs):
        save_obj, _ = Save.objects.get_or_create(post_id=pk, owner=request.user)
        save_obj.save_status = not save_obj.save_status
        save_obj.save()
        status_of_save = 'saved'
        if not save_obj.save_status:
            status_of_save = 'deleted'
        return Response({'status': status_of_save})

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset