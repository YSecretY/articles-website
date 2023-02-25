from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.User', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    REQUIRED_FIELDS = ['title', 'description', 'content', 'author']
