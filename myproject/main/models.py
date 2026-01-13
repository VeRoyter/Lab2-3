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
    type = models.CharField(max_length=255)  # Movie или TV Show
    date_added = models.DateField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Shows'


class CountriesCast(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, db_column='show_id')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, db_column='country_id')

    def __str__(self):
        return f"{self.show.title} - {self.country.country_name}"

    class Meta:
        db_table = 'Countries Cast'
        unique_together = ('show', 'country')


class DirectorsCast(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, db_column='show_id')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, db_column='director_id')

    def __str__(self):
        return f"{self.show.title} - {self.director.director_name}"

    class Meta:
        db_table = 'Directors Cast'
        unique_together = ('show', 'director')


class ActorsCast(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, db_column='show_id')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, db_column='actor_id')

    def __str__(self):
        return f"{self.show.title} - {self.actor.actor_name}"

    class Meta:
        db_table = 'Actors Cast'
        unique_together = ('show', 'actor')