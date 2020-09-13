from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)

def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'posts/{0}/{1}'.format(instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = models.ImageField(upload_to=post_directory_path, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
