from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from better_profanity import profanity

class Topic(models.Model):
    text = models.TextField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.text
    def censorship(self):
        if profanity.censor(self.text) != self.text:
            raise ValidationError("Do not use bad language in your topic !")
        
    def save(self, *args, **kwargs):
        self.censorship()  # call the censorship() method to check for bad language
        super().save(*args, **kwargs)  # call the original save() method to save the model

class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        return f"{self.text[:50]}..."
    
    def clean(self):
        # Split the text field into words
        words = self.text.split()
        # Check if there are at least 250 words
        if len(words) < 250:
            raise ValidationError('The text field must contain at least 250 words.')
    def censorship(self):
        # Check if the text contains profanity
        if profanity.censor(self.text) != self.text:
            raise ValidationError("Do not use bad language in your entry !")
        
    def save(self, *args, **kwargs):
        self.full_clean()  # call the clean() method to validate the model
        self.censorship()  # call the censorship() method to check for bad language
        super().save(*args, **kwargs)  # call the original save() method to save the model