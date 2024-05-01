from django.db import models
from django.urls import reverse

class Test(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['-title']

    def get_absolute_url(self):
        return reverse('test-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    description = models.TextField(default='')
    placeholder = models.CharField(max_length=5, default='coh7$') # tab is always tab$

    def __str__(self):
        return self.description

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class UserResponse(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255, default='')