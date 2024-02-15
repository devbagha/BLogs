from django.db import models
from django.contrib.auth.models import User

class Site(models.Model):  ###########  ###########
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Category(models.Model): ###########  ###########
    name = models.CharField(max_length=100) 
    featured_image = models.ImageField(upload_to='category/',blank=False, null=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories_added')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
   

class SubCategory(models.Model): ###########  ###########
    name = models.CharField(max_length=100)
    featured_image = models.ImageField(upload_to='sub_category/',blank=False, null=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcategories_added')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='category')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Post(models.Model): ######
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    meta = models.TextField()
    categories = models.ManyToManyField(Category)
    sub_categories = models.ManyToManyField(SubCategory)
    tags = models.TextField()
    is_active = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='posts/',blank=False, null=False)
    published_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_added')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    


class PostImage(models.Model): ######
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/',blank=False, null=False)
    is_active = models.BooleanField(default=True)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    

class PrimaryMenu(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SubMenu(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    parent = models.ForeignKey(PrimaryMenu, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ChildMenu(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(SubMenu, null=True, blank=True, on_delete=models.CASCADE)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Files(models.Model):
    logo = models.ImageField(upload_to='images/',blank = False)
    favicon = models.ImageField(upload_to='images/',blank = False)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)


class HomePageSections(models.Model):
    heading = models.CharField(max_length=100,null=True)
    subheading = models.CharField(max_length=100,null=True)
    paragraph = models.CharField(max_length=100,null=True)
    image = models.ImageField(blank=False, null=False)
    background_image = models.ImageField(blank=False, null=False)
    section_id = models.CharField(max_length=100)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)



    
class Pages(models.Model):    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True) 
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class Sections(models.Model): ########### ###########
    heading = models.CharField(max_length=100,null=True)
    subheading = models.CharField(max_length=100,null=True)
    paragraph = models.CharField(max_length=100,null=True)
    image = models.ImageField(blank=False, null=False)
    background_image = models.ImageField(blank=False, null=False)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    orders = models.IntegerField(default=1,null=True)
    page_id = models.ForeignKey(Pages, on_delete=models.CASCADE)
    

    def __str__(self):
        return   self.page_id.name
    