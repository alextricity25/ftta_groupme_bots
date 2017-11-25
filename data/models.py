from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class MemoryVerse(models.Model):

    CLASSES = (
        ('ECAL', 'Experience of Christ as Life'),
        ('GE', "God's Economy"),
        ('GoW', "God Ordained Way")
    )
    ftta_term = models.CharField(
        max_length=255,
    )
    reference = models.CharField(
        max_length=100,
    )
    verse = models.TextField()
    for_class = models.CharField(max_length=100, choices=CLASSES)

    def __str__(self):
        return self.reference

class RideArranger(models.Model):
    pass
