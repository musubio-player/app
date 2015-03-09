import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

ACTION_SAVE_INSERT = 'insert'
ACTION_SAVE_UPDATE = 'update'

class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, save=False):
        """
        Override model save method to modify the object before and after saving.
        """
        instance = super(BaseModel, self)

        if self.id:
            action = ACTION_SAVE_UPDATE
        else:
            action = ACTION_SAVE_INSERT

        # Before save
        try:
            self.before_save(action, save)
        except AttributeError:
            pass

        # The save
        instance.save()

        # After save
        try:
            self.after_save(action, save)
        except AttributeError:
            pass

        return instance

    def is_loaded(self):
        """
        Checks to see if the object is loaded.
        """
        if self.id is not None:
            return True
        else:
            return False

class ContentModel(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, help_text='A slug will be genereated if left blank.')
    user = models.ForeignKey(User)
    date_published = models.DateTimeField(default=datetime.datetime.now)
    date_last_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Publish')

    def before_save(self, action, save):
        self.slug = slugify(self.title)

    class Meta:
        abstract = True