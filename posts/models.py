from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight



class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=1000, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts')

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        options = self.title and {'title': self.title} or {}
        super(Post, self).save(*args, **kwargs)

        # limit the number of instances retained
        posts = Post.objects.all()
        if len(posts) > 100:
            posts[0].delete()

