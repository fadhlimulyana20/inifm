from django.db import models
from django.contrib.auth.models import User
from meta.models import ModelMeta
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.
STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)

def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'posts/{0}/{1}'.format(instance.id, filename)

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(ModelMeta, models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = models.ImageField(upload_to=post_directory_path, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    _metadata = {
        'og_title': 'title',
        'description': 'content',
        'image': 'get_meta_image'
    }

    def get_meta_image(self):
        if self.featured_image:
            print(self.featured_image.url)
            return self.featured_image.url

    def __str__(self):
        return self.title

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" %(slug, qs.count()+1)
    instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Post)

