from django.db import models

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255)

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = 'Country'


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    director_name = models.CharField(max_length=255)

    def __str__(self):
        return self.director_name

    class Meta:
        db_table = 'Director'


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor_name = models.CharField(max_length=255)

    def __str__(self):
        return self.actor_name

    class Meta:
        db_table = 'Actor'


class Show(models.Model):
    show_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    date_added = models.DateField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Добавил ManyToManyField вместо отдельных таблиц
    countries = models.ManyToManyField(Country, related_name='shows', db_table='Countries Cast')
    directors = models.ManyToManyField(Director, related_name='shows', db_table='Directors Cast')
    actors = models.ManyToManyField(Actor, related_name='shows', db_table='Actors Cast')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Shows'
