from backend.models import * 
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    author = serializers.StringRelatedField()
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_path = representation['featured_image']
        new = str(image_path).split('/')
        new.insert(3, 'static')
        final = '/'.join(new)
        representation['featured_image'] = str(final)
        return representation
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_path = representation['featured_image']
        new = str(image_path).split('/')
        new.insert(3, 'static')
        final = '/'.join(new)
        representation['featured_image'] = str(final)
        return representation
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_path = representation['featured_image']
        new = str(image_path).split('/')
        new.insert(3, 'static')
        final = '/'.join(new)
        representation['featured_image'] = str(final)
        return representation
        
    author = serializers.StringRelatedField()
    categories = serializers.StringRelatedField(many=True)
    sub_categories = serializers.StringRelatedField(many=True)
    published_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Customize the format here

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

class PrimaryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PrimaryMenu
        fields = '__all__'
        
class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = '__all__'
        
class ChildMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMenu
        fields = '__all__'
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'
        
class HomePageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSections
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = '__all__'
        
class PageSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=True, read_only=True)
    class Meta:
        model = Pages
        fields = ('id', 'name', 'type', 'is_active', 'site_id', 'section')