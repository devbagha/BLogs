from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework import mixins, viewsets
from .serializers import * 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.decorators import *

## Retrieve All Categories 
class Categories(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.filter(is_active = True)
    serializer_class = CategorySerializer
    
## Retrieve Category Detail of specified id    
class CategoryDetail(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Category.objects.filter(is_active = True)
    serializer_class = CategorySerializer
    lookup_field = 'id' 
    
## Retrieve All SubCategories 
class SubCategories(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = SubCategory.objects.filter(is_active = True)
    serializer_class = SubCategorySerializer
    
    def get_serializer_context(self):
        return {'request':self.request}

## Retrieve Posts based on category name i.e; slug
class Category_Post(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        queryset = Post.objects.filter(categories__slug=category_slug,is_active = True)
        return queryset  
    
## Retrieve Posts based on sub_category name i.e; slug
class Subcat_Post(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        subcategory_slug = self.kwargs['subcategory_slug']
        queryset = Post.objects.filter(sub_categories__slug=subcategory_slug,is_active = True)
        return queryset    
    
## Retrieve SubCategory Detail of specified id    
class SubCategoryDetail(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = SubCategory.objects.filter(is_active = True)
    serializer_class = SubCategorySerializer
    lookup_field = 'id' 
    
## Retrieve All Blog Posts  
class Posts(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Post.objects.filter(is_active = True,)
    serializer_class = PostSerializer
    
## Retrieve specified Blog Post with its images      
class PostDetail(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Post.objects.filter(is_active = True)
    serializer_class = PostSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        post_serializer = self.get_serializer(instance)
        post_image_serializer = PostImageSerializer(instance.postimage_set.all(), many=True)
        
        response_data = {
            'post': post_serializer.data,
            'images': post_image_serializer.data,
        }
        return Response(response_data)
    
## Retrieve Logo & Favicon      
class File(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Files.objects.all()
    serializer_class = FileSerializer

## Retrieve Home Page Sections Contents
class HomePageSection(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = HomePageSections.objects.all()
    serializer_class = HomePageSectionSerializer

## Menu
class Menu(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        primary_menus = PrimaryMenu.objects.all()
        primary_serializer = PrimaryMenuSerializer(primary_menus, many=True)

        data = []

        for primary_data in primary_serializer.data:
            primary_id = primary_data['id']
            primary_data['sub_menus'] = []

            sub_menus = SubMenu.objects.filter(parent_id=primary_id)
            sub_serializer = SubMenuSerializer(sub_menus, many=True)

            for sub_data in sub_serializer.data:
                sub_id = sub_data['id']
                sub_data['child_menus'] = []

                child_menus = ChildMenu.objects.filter(parent_id=sub_id)
                child_serializer = ChildMenuSerializer(child_menus, many=True)

                sub_data['child_menus'] = child_serializer.data
                primary_data['sub_menus'].append(sub_data)

            data.append(primary_data)

        return Response(data)
  
  
class SiteMenu(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request,site_id, *args, **kwargs):
        primary_menus = PrimaryMenu.objects.filter(site_id = site_id)
        primary_serializer = PrimaryMenuSerializer(primary_menus, many=True)

        data = []

        for primary_data in primary_serializer.data:
            primary_id = primary_data['id']
            primary_data['sub_menus'] = []

            sub_menus = SubMenu.objects.filter(parent_id=primary_id)
            sub_serializer = SubMenuSerializer(sub_menus, many=True)

            for sub_data in sub_serializer.data:
                sub_id = sub_data['id']
                sub_data['child_menus'] = []

                child_menus = ChildMenu.objects.filter(parent_id=sub_id)
                child_serializer = ChildMenuSerializer(child_menus, many=True)

                sub_data['child_menus'] = child_serializer.data
                primary_data['sub_menus'].append(sub_data)

            data.append(primary_data)

        return Response(data)
  
class Title_Search(ListAPIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = PostSerializer
    def get_queryset(self):
        query = self.kwargs['title']
        queryset = Post.objects.filter(Q(title__icontains=query),is_active = True)
        return queryset  
    
## Return Posts by searching content in description     
class Desc_Search(ListAPIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    def get_queryset(self):
        query = self.kwargs['content']
        queryset = Post.objects.filter(Q(content__icontains=query),is_active = True)
        return queryset     
    
## Return Posts by searching content in description     
class Title_Content_Search(ListAPIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    def get_queryset(self):
        query = self.kwargs['content']
        queryset = Post.objects.filter(Q(title__icontains=query) & Q(content__icontains=query),is_active = True)
        return queryset

## Return Posts by searching content in description     
class Post_Detail_Slug(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        query = self.kwargs['slug']
        queryset = Post.objects.filter(slug=query,is_active = True)
        return queryset



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_post_by_slug(request,slug):
    queryset = Post.objects.get(slug=slug,is_active = True)
    serializer = PostSerializer(queryset)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_category_by_slug(request,slug):
    queryset = Category.objects.get(slug=slug,is_active = True)
    serializer = CategorySerializer(queryset)
    return Response(serializer.data)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_category_by_site(request,site_id):
    queryset = Category.objects.filter(site_id=site_id,is_active = True)
    serializer = CategorySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_post_by_site(request, site_id):
    queryset = Post.objects.filter(site_id=site_id, is_active=True)
    serializer = PostSerializer(queryset, many=True)  
    return Response(serializer.data)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_sub_category_by_slug(request,slug):
    queryset = SubCategory.objects.get(slug=slug,is_active = True)
    serializer = SubCategorySerializer(queryset)
    return Response(serializer.data)


class PagesViewSet(viewsets.ModelViewSet):
    queryset = Pages.objects.filter(is_active=True)
    serializer_class = PageSerializer

    def list(self, request, *args, **kwargs):
        pages = Pages.objects.filter(is_active=True)
        data = {}

        for page in pages:
            sections_data = []  # To store sections for each page
            sections = Sections.objects.filter(page_id=page)

            for section in sections:
                sections_data.append({
                    section.id: SectionSerializer(section).data
                })

            data[page.name] = {
                'sections': sections_data
            }

        return Response(data)
