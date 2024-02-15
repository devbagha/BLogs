
from django.shortcuts import render, redirect
from .models import *
from datetime import datetime  
from django.contrib.auth.decorators import login_required  
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile




def dashboard(request):
    pass


def site_list(request):
    sites = Site.objects.all()
    return render(request, 'site/site_list.html', {'sites': sites})


def create_site(request):
    if request.method == "POST":
        name = request.POST['name']
        Site.objects.create(
            name=name,
            is_active = True
        ).save()
        return redirect('sitelist') 
    else:
        return render(request, 'site/site_create.html')



def edit_site(request, id):
    site = Site.objects.get(id=id)

    if request.method == "POST":
        name = request.POST.get('name', '')  
        is_active = request.POST.get('is_active', False)  

        site.name = name
        site.is_active = is_active
        site.save()


    return render(request, 'site/site_update.html', {'site': site})



def sub_list(request):
    sub_cat = SubCategory.objects.all()
    return render(request, 'sub_category/sub_category_list.html', {'sub_category': sub_cat})



@login_required
def create_sub_category(request):
    categories= Category.objects.all()
    
    if request.method == "POST":
        name = request.POST['name']
        slug = request.POST['slug']
        author = request.user
        site_id = Site.objects.get(id = 1)
        featured_image = request.FILES['featured_image'] 
        
        subCategory = SubCategory.objects.create(
            name=name,
            is_active=True,
            slug=slug,
            published_date=datetime.now(),
            author=author,
            category= Category.objects.get(id= request.POST['category']),
            site_id=site_id,
            featured_image= featured_image
        )
        subCategory.save()
        return redirect('sub_category_list')
    else:
        return render(request, 'sub_category/sub_category_create.html',{'categories':categories})
    
    
    
    
def edit_sub_category(request,id):
    sub_categories= SubCategory.objects.get(id=id)
    if request.method == 'POST':
        img = request.FILES.get('featured_image','')
        if img != '':
            sub_categories.featured_image = img
        sub_categories.name = request.POST['name']
        sub_categories.slug = request.POST['slug']
        sub_categories.save()
        
    return render(request, 'sub_category/edit_sub_category.html',{'sub_categories':sub_categories})
    

    

def cat_list(request):
    category = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': category})

@login_required
def create_category(request):
    if request.method == "POST":
        name = request.POST['name']
        slug = request.POST['slug']
        author = request.user
        site_id = Site.objects.get(id = 1) 
        featured_image = request.FILES['featured_image'] 
        
        category = Category.objects.create(
            name=name,
            is_active=True,
            slug=slug,
            published_date=datetime.now(),
            author=author,
            site_id=site_id,
            featured_image= featured_image
        )
        category.save()
        return redirect('category_list')
    else:
        return render(request, 'category/category_create.html')
    
    
def edit_category(request,id):
    category = Category.objects.get(id = id)
    if request.method == 'POST':
        img = request.FILES.get('featured_image','')
        if img != '':
            category.featured_image = img
            
        category.name = request.POST['name']
        category.slug = request.POST['slug']
        category.save()

    return render(request, 'category/category_edit.html',{'category':category})



def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post/post_list.html', {'posts': posts})

@login_required
def create_post(request):
    cat = Category.objects.all()
    sub_cat = SubCategory.objects.all()
    
    if request.method == "POST":

        title = request.POST['title']
        slug = request.POST['slug']
        content = request.POST['content']
        meta = request.POST['meta']
        content = request.POST['content']
        featured_image = request.FILES['featured_image'] 
        published_date = datetime.now()  
        author =  request.user 
        site_id = Site.objects.get(id = 1) 

        post = Post.objects.create(
            title=title,
            slug=slug,
            content=content,
            meta=meta,
            site_id= site_id,
            featured_image= featured_image,
            published_date= published_date,
            author= author,
        )
        post.save()
        
        categories =  request.POST.getlist('category[]')
        sub_categories =  request.POST.getlist('sub_category[]')
        
        for cat in categories:
            post.categories.add(Category.objects.get(id=cat))
            post.save()
        
        for cat in categories:
            post.sub_categories.add(SubCategory.objects.get(id=cat))
            post.save()
            
        images = request.FILES.getlist('multiple')
        for img in images:
            PostImage.objects.create(
                image = img,
                is_active= True,
                post = post,
                site_id = Site.objects.get(id=1)
                ).save()
            
        return redirect('post_list')
    else:
        return render(request, 'post/post_create.html',{'category':cat,'sub_category':sub_cat})
    






def edit_post(request, post_id):
    cat = Category.objects.all()
    sub_cat = SubCategory.objects.all()
    
    post = Post.objects.get(id=post_id)  
    
    if request.method == "POST":
        title = request.POST['title']
        slug = request.POST['slug']
        content = request.POST['content']
        meta = request.POST['meta']
        featured_image = request.FILES.get('featured_image', post.featured_image)
        
        post.title = title
        post.slug = slug
        post.content = content
        post.meta = meta
        if featured_image:
            post.featured_image = featured_image
        post.save()
        
        categories = request.POST.getlist('category[]')
        sub_categories = request.POST.getlist('sub_category[]')
        
        post.categories.clear()
        post.sub_categories.clear()
        post.categories.add(*Category.objects.filter(id__in=categories))
        post.sub_categories.add(*SubCategory.objects.filter(id__in=sub_categories))
        
        images = request.FILES.getlist('multiple')
        for img in images:
            PostImage.objects.create(
                image=img,
                is_active=True,
                post=post,
                site=Site.objects.get(id=1)
            ).save()
            
        return redirect('post_list')  
    else:
        return render(request, 'post/post_edit.html', {'post': post, 'category': cat, 'sub_category': sub_cat})
    
    
def menu_list(request):

    
    primary_menus = PrimaryMenu.objects.filter(site_id=1)
    menu_data = []

    for primary_menu in primary_menus:
        primary = {
            'id': primary_menu.id,
            'title': primary_menu.title,
            'link': primary_menu.link,
            'submenus': [],
        }
        submenus = SubMenu.objects.filter(parent=primary_menu)

        for submenu in submenus:
            submenu_data = {
                'id': submenu.id,
                'title': submenu.title,
                'link': submenu.link,
                'childmenus': [],
            }
            childmenus = ChildMenu.objects.filter(parent=submenu)
            
            for childmenu in childmenus:
                childmenu_data = {
                    'id': childmenu.id,
                    'title': childmenu.title,
                    'link': childmenu.link,
                    # Add any other child menu properties here
                }
                submenu_data['childmenus'].append(childmenu_data)

            primary['submenus'].append(submenu_data)

        menu_data.append(primary)
    print(menu_data)
    return render(request, 'menu/menu_list.html', {'menu_data': menu_data})
        
            
    
def create_primary_menu(request):
    if request.method == "POST":
        title = request.POST['title']
        link = request.POST['link']
        PrimaryMenu.objects.create(title=title,link=link,site_id= Site.objects.get(id=1),is_active= True).save()
    return render(request, 'menu/primary_create.html')
    
def create_sub_menu(request):
    primary = PrimaryMenu.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        link = request.POST['link']
        parent = PrimaryMenu.objects.get(id=request.POST['parent'])
        SubMenu.objects.create(title=title,link=link,parent=parent,site_id= Site.objects.get(id=1),is_active= True).save()
        
    return render(request, 'menu/submenu_create.html',{'primary':primary})

def create_child_menu(request):
    primary = SubMenu.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        link = request.POST['link']
        parent = SubMenu.objects.get(id=request.POST['parent'])
        ChildMenu.objects.create(title=title,link=link,parent=parent,site_id= Site.objects.get(id=1),is_active= True).save()
    return render(request, 'menu/child_create.html',{'primary':primary})


def page_list(request):
    page = Pages.objects.filter(site_id=Site.objects.get(id=1))
    return render(request, 'pages/pages_list.html', {'page': page})
    
    
    

def create_pages(request):
    
    if request.method == "POST":
        Pages.objects.create(
            name=request.POST['name'], 
            type=request.POST['type'],
            site_id= Site.objects.get(id=1),
            is_active= True 
            ).save()

    return render(request, 'pages/pages_create.html')


def sections_list(request):
    sections = Sections.objects.filter(site_id=Site.objects.get(id=1))
    return render(request, 'sections/sections_list.html', {'sections': sections})
    
    

def create_sections(request):
    
    page = Pages.objects.all()
    
    if request.method == "POST":
        background_image = request.FILES.get('background_image', None)
        image = request.FILES.get('image', None)
        section = Sections.objects.create(heading=request.POST['heading'],
                                          paragraph=request.POST['paragraph'],
                                          orders=request.POST['orders'],
                                          subheading=request.POST['subheading'],
                                          page_id= Pages.objects.get(id=request.POST['page']),
                                          background_image = background_image,
                                          image = image,
                                          site_id = Site.objects.get(id=1),
                                          is_active= True ).save()
    return render(request, 'sections/sections_create.html',{'page':page})



def edit_section(request, id):
    section = Sections.objects.get(id=id)
    page = Pages.objects.all()

    if request.method == "POST":
        
        img = request.FILES.get('img','')
        bg = request.FILES.get('bg','')
        
        if img != '':
            section.image = img

        if bg != '':
            section.background_image = bg
        
        section.heading = request.POST.get('heading', '')  
        section.paragraph = request.POST.get('paragraph', '')  
        section.orders = request.POST.get('orders', )  
        section.subheading = request.POST.get('subheading', '')  
        section.is_active = request.POST.get('is_active', False)  
        section.save()

    return render(request, 'sections/sections_update.html',{'section':section,'page':page})


