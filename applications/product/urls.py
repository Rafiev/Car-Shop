from django.urls import path
from rest_framework.routers import DefaultRouter
from applications.product.views import CarAPIView, CarListAPIView, CommentAPIView, SaleAPIView, SaleConfirmAPIView, \
    SaveAPIView

router = DefaultRouter()
router.register('comment', CommentAPIView)
router.register('save', SaveAPIView)
router.register('', CarAPIView)

urlpatterns = [
    path('list/', CarListAPIView.as_view()),
    path('order/', SaleAPIView.as_view()),
    path('<int:pk>/order_confirm/', SaleConfirmAPIView.as_view()),
]

urlpatterns += router.urls