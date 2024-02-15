from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

urlpatterns = [
    path('save-site',create_site,name="save-site"),
    path('site-list',site_list,name="sitelist"),
    path('save-category',create_category,name="save-category"),
    path('cat-list',cat_list,name="category_list"),
    path('save-sub_category',create_sub_category,name="save-sub_category"),
    path('sub_cat_list',sub_list,name="sub_category_list"),
    path('save-post',create_post,name="save-post"),
    path('post_list',post_list,name="post_list"),
    path('save-primary-menu',create_primary_menu,name="save-primary-menu"),
    path('save-sub-menu',create_sub_menu,name="save-sub-menu"),
    path('save-child-menu',create_child_menu,name="save-child-menu"),
    path('menu-list',menu_list,name="menu_list"),
    path('menu-list',menu_list,name="menu_list"),
    path('create_section',create_sections,name="create_section"),
    path('create_section',create_sections,name="create_section"),
    path('page_create',create_pages,name="page_create"),
    path('edit_site/<int:id>',edit_site,name="edit_site"),
    path('edit_section/<int:id>',edit_section,name="edit_section"),
    path('edit_category/<int:id>',edit_category,name="edit_category"),
    path('edit_sub_category/<int:id>',edit_sub_category,name="edit_sub_category"),
    path('edit-post/<int:post_id>',edit_post,name="edit-post"),
    path('pages',page_list,name='page_list'),
    path('section',sections_list,name='sections_list'),
]