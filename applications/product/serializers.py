from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from applications.product.models import Car, Comment, Rating, Image, Sale, Save
from applications.product.tasks import send_order_confirm

User = get_user_model()


class SaleSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        order = Sale.objects.create(owner=user, **validated_data)
        return order

    def send_code(self):
        request = self.context.get('request')
        email = request.user.email
        post_id = request.data.get('post')
        send_order_confirm.delay(email, post_id)

    class Meta:
        model = Sale
        fields = '__all__'


class OrderConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    @staticmethod
    def validated_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User does not exist.')
        return email

    def validate_password(self, password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')
        return password


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['rating']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        car = Comment.objects.create(owner=user, **validated_data)
        return car

    class Meta:
        model = Comment
        fields = ['owner', 'body']


class CarSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        images_data = request.FILES
        car = Car.objects.create(owner=user, **validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(post=car, image=image)
        return car

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.filter(like=True).count()
        rep['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return rep

    class Meta:
        model = Car
        fields = '__all__'


class CarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['title', 'category', 'price']


class SaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Save
        fields = '__all__'