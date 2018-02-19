from django.contrib import admin
# Register your models here.
from .models import Post

#admin.site.register(Post)

class PostModelAdmin(admin.ModelAdmin):
    fields = [
    'title',
    'slug',
    'content',
    'publish',
    'publish_date',
    'active',
    'updated',
    'timestamp',
    'new_content'
]

readonly_fields = [ 'updated', 'timestamp', 'get_age']

def new_content(self, obj, *args, **kwargs):
    return str(obj.title)

def get_age(self, obj, *args, **kwargs):
    return str(obj.age)

class Meta:
    model = Post

admin.site.register(Post, PostModelAdmin)
