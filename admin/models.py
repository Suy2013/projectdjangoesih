from django.db import models
import ast
from parametrage.models import CodeCours
from professeur.models import Professor
# Create your models here.
class User(models.Model):
    active = models.BooleanField()
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=100)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(User, self).save(force_insert, force_update, using, update_fields)
        return  self.id

class UserProf(models.Model):
    professeur = models.ForeignKey(Professor,null=True)
    user=models.ForeignKey(User)
class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Cours(models.Model):
    codecours = models.ForeignKey(CodeCours)
    ects = models.IntegerField(max_length=1)
    prof = models.ManyToManyField(Professor)
    prerequis = models.ManyToManyField("Cours",null=True)
    public = ListField()
    format = ListField()
    objectif = models.TextField(null=True)
    description = models.TextField(null=True)
    plan = models.TextField(null=True)
    ressource = models.TextField(null=True)
    evaluation = models.TextField(null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Cours, self).save(force_insert, force_update, using, update_fields)
        return  self.id


class Type:
    PROF = "Prof"
    ADMIN = "Admin"
    SUPER = "Super Admin"
    