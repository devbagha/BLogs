from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteMenu,Categories,PagesViewSet, CategoryDetail,get_post_by_site,get_category_by_site,get_post_by_slug,get_category_by_slug,get_sub_category_by_slug,Post_Detail_Slug,Posts,PostDetail,Title_Content_Search,Desc_Search,SubCategories,Title_Search,SubCategoryDetail,File,HomePageSection,Menu,Category_Post,Subcat_Post 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'category', Categories, basename='category')
router.register(r'category', CategoryDetail, basename='category-detail')
router.register(r'sub-category', SubCategories, basename='post')
router.register(r'sub-category', SubCategoryDetail, basename='post-detail')
router.register(r'posts', Posts, basename='post')
router.register(r'posts', PostDetail, basename='post-detail')
router.register(r'files', File, basename='files')
router.register(r'sections', HomePageSection, basename='sections')
router.register(r'pages', PagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('menu', Menu.as_view(), name='menu-hierarchy'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('category_post/<str:category_slug>/', Category_Post.as_view(), name='category-posts'),
    path('subcategory/<str:subcategory_slug>/', Subcat_Post.as_view(), name='subcategory-posts'),
    path('title_search/<str:title>/', Title_Search.as_view(), name='title_search-posts'),
    path('content_search/<str:content>/', Desc_Search.as_view(), name='content_search-posts'),
    path('title_content_search/<str:content>/', Title_Content_Search.as_view(), name='title_content_search-posts'),
    path('post-slug/<str:slug>',get_post_by_slug,name='post_detail-posts'),
    path('cat-slug/<str:slug>',get_category_by_slug,name='post_detail-posts'),
    path('subcat-slug/<str:slug>',get_sub_category_by_slug,name='post_detail-posts'),
    path('menu/<str:site_id>', SiteMenu.as_view(), name='menu'),
    path('post-site/<str:site_id>',get_post_by_site,name='post_detail-site_id'),
    path('category-site/<str:site_id>',get_category_by_site,name='category_detail-site_id'),

]