from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    description = models.CharField(null=True, blank=True, max_length=250, verbose_name='Краткое описание', default='')
    avatar = models.ImageField(null=True, blank=True, upload_to='appcourses/images/subjects/', verbose_name='Аватар')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return ''


class Course(models.Model):
    owner = models.ForeignKey(User, null=True, related_name='course_owner', on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, null=True, related_name='course_subject', on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, verbose_name='Название курса')
    slug = models.SlugField(max_length=210, unique=True)
    overview = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='appcourses/images/courses/', verbose_name='Аватар')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return ''


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='module_course', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название модуля')
    description = models.TextField(blank=True, verbose_name='Описание модуля')
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'model__in':('text',
                                                                    'video',
                                                                    'image',
                                                                    'file')},
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
            ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('appcourses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()
