from django.db import models
from PIL import Image
from django.conf import settings
from django.template.defaultfilters import slugify


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def post_count(self):
        return self.posts.all().count()

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    publishing_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts',default=1)
    tag = models.ManyToManyField(Tag, related_name='posts')
    slider_post = models.BooleanField(default=False)
    hit = models.PositiveIntegerField(default=0)
    
    def comment_count(self):
        return self.comments.all().count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    def __str__(self):
        return self.title
    
    def post_tag(self):
        return ", ".join([tag.title for tag in self.tag.all()])
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
