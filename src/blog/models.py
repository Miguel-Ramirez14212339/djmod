from datetime import timedelta, datetime, date
from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.db.models.signals import post_save, pre_save
from .validators import Validate_algo, Validate_author_email

PUBLICH_CHOICES = (
('draft', 'Draft'),
('public', 'Public'),
('private', 'Private'),
)

# Create your models here.
#Custom QuerySet Methods

class PostModelQuery(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def nuevo_title_items(self, value):
        return self.filter(title__icontains=value)

#Model manager
class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostModelQuerySet(self.model, using=self._db)

    def all(se  , *args, **kwargs):
        qs = super(PostModeManager, self).all(*args, **kwargs).active()
        return qs

class Post(models.Model):
    id              = models.BigAutoField(primary_key = True)
    activate        = models.BooleanField(default = True)
    title           = models.CharField(max_length = 250,
                                       verbose_name= 'Post Title',
                                       unique = True,
                                       error_messages={
                                       "unique":"Este titulo no es unico. intenta de nuevo"
                                       },
                                       help_text = 'Debe ser un titulo unico.')
    content         = models.TextField(null = True, blank = True)
    publish         = models.CharField(max_length=120, choices = PUBLICH_CHOICES, default= "draft")
    slug            = models.SlugField(null=True, blank=True)
    view_count      = models.IntegerField(default=0)
    publish_date    = models.DateField(auto_now = False, auto_now_add=False, default = timezone.now )
    author_email    = models.EmailField(max_length = 240, validators = [Validate_author_email, Validate_algo], null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return smart_text(self.content)

    def save(self, *args, **kwargs):
        print ("Guarde algo")
        #super(Post, self).save(*args, **kwargs)
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @property
    def age(self):
        if self.publish == 'publish':
            now = datetime.now()
            publish_time = datetime.combine(
                           self.publish_date,
                           datetime.now().min.time()
                           )
        try:
            differnce = now - publish_time
            print(differnce)
        except:
            difference = "No hay publicacion"

        if differnce <= timedelta(minute=1):
            return "Ahora"
        return "{time} ago".format(time=timestamp(publish_time).split(",")[0])

    # makemigtrations y migrate cada vez que modifiquemos modelos

def post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    print ("Despues Almacenar")
    if not instance.slug and instance.title:
        instance.slug = slugify (instance.title)
        instance.save()
post_save.connect(post_model_post_save_receiver, sender=Post)

def post_model_pre_save_receiver(sender, instance, created, *args, **kwargs):
    print ("Antes de Alamacenar")
    if not instance.slug and instance.title:
        instance.slug = slugify (instance.title)
        instance.save()
pre_save.connect(post_model_post_save_receiver, sender=Post)
