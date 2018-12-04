from django.db import models
from questionaire.models import Questionaire


class Chat(models.Model):
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=1,null=True)
    log = models.TextField(default='')

    def __str__(self):
        return self.log

