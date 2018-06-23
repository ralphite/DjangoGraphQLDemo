from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    state = models.ForeignKey(
        State, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
