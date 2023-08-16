from django.db import models
from django.utils import timezone
from django.urls import reverse


class OpenPollsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Question.Status.OPEN)


class Question(models.Model):
    # enum to enable poll open and closure
    class Status(models.TextChoices):
        OPEN = 'opn', 'Open'
        CLOSE = 'cls', 'Close'

    question = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=3, 
                              choices=Status.choices,
                              default=Status.CLOSE)

    objects = models.Manager()
    open = OpenPollsManager()

    class Meta:
        ordering = ['-created']
        indexes = models.Index(fields=['-created']),

    def __str__(self):
        return self.question
    
    def get_absolute_url(self):  # absolute url
        return reverse('polls:poll_detail', args=[self.id])
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, 
                                 related_name='choices')
    option = models.CharField(max_length=50)
    vote = models.IntegerField(default=0)


    def __str__(self):
        return self.option
    
