from django.db import models

class Questionaire(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name


class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    reference_id = models.PositiveIntegerField(null=True)
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('reference_id', 'questionaire',)

    def __str__(self):
        return self.question_text


class Responses(models.Model):
    options = models.CharField(max_length=200)
    next = models.PositiveIntegerField(null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    questionaire = models.ForeignKey(Questionaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.options
