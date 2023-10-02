from .models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


#class UsersSerializer(serializers.ModelSerializer):
#class UsersSerializer(serializers.HyperlinkedModelSerializer):

class AuthorSerializer(serializers.ModelSerializer):
   class Meta:
       model = Author
       fields = ['surname', 'name', 'patronymic', 'email', 'telephone']


class CoordinateSerializer(serializers.ModelSerializer):
   class Meta:
       model = Coordinate
       fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
   class Meta:
       model = Level
       fields = ['winter', 'spring', 'summer', 'autumn']


class ImageSerializer(serializers.ModelSerializer):
   #photo = serializers.CharField()
   class Meta:
       model = Image
       fields = ['title', 'photo', 'peak']


#class PeakSerializer(WritableNestedModelSerializer):
class PeakSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    coords = CoordinateSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
       model = Peak
       fields = ['country', 'category', 'title', 'other_titles', 'connect', 'add_time', 'status', 'activities', 'user', 'coords', 'level',
                'images']

    def create(self, validated_data, **kwargs):
        user_data = validated_data.pop('user')
        images_data = validated_data.pop('images')
        coordinates_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')

        current_user = Author.objects.filter(email=user_data['email'])
        if current_user.exists():
            user_serializer = AuthorSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_data = user_serializer.save()
        else:
            user_data = Author.objects.create(**user_data)

        user = Author.objects.create(**user_data)
        coords = Coordinate.objects.create(**coordinates_data)
        level = Level.objects.create(**level_data)

        peak = Peak.objects.create(**validated_data, user=user, coords=coords, level=level)

        if images_data:
            for image in images_data:
                image_name = image.pop('title')
                image = image.pop('photo')
                Image.objects.create(peak=peak, title=image_name, photo=image)

        peak.save()
        return peak

