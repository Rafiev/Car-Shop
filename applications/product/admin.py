from django.contrib import admin
from applications.product.models import Car, Comment, Like, Rating, Image, Sale, Save


class ImageAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 5


class LikeAdmin(admin.TabularInline):
    model = Like
    fields = ('like',)
    max_num = 1


class CarAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin, LikeAdmin]

    list_display = ['id', 'title', 'price', 'likes']

    @staticmethod
    def likes(obj):
        return obj.likes.filter(like=True).count()


admin.site.register(Car, CarAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Image)
admin.site.register(Sale)
admin.site.register(Save)