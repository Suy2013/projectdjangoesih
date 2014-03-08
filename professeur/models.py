from django.db import models
# Create your models here.
class Professor(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    sexe = models.CharField(max_length=1)
    identite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    email = models.EmailField()
    adresse = models.CharField(max_length=400)
    naissance = models.DateField(null=True)
    def __unicode__(self):
        return u'%s %s' % (self.nom,self.prenom)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Professor, self).save(force_insert, force_update, using, update_fields)
        return  self.id
class Formation(models.Model):
    professor = models.ForeignKey("Professor")
    de = models.DateField()
    a = models.DateField(null=True)
    now = models.CharField(max_length=500, null=True)
    diplome = models.CharField(max_length=100)
    etablissement = models.CharField(max_length=500)
    localite = models.CharField(max_length=400)

class Experience(models.Model):
    professor = models.ForeignKey("Professor")
    de = models.DateField()
    a = models.DateField(null=True)
    now = models.CharField(max_length=500, null=True)
    fonction = models.CharField(max_length=500)
    entreprise = models.CharField(max_length=500)

class Langue(models.Model):
    professor = models.ForeignKey("Professor")
    langue = models.CharField(max_length=50)
    lire = models.CharField(max_length=200)
    comprendre = models.CharField(max_length=200)
    parler = models.CharField(max_length=200)
    ecrire = models.CharField(max_length=200)

class CompetenceOrg(models.Model):
    professor = models.ForeignKey("Professor")
    organisationel = models.CharField(max_length=300)

class CompetenceCom(models.Model):
    professor = models.ForeignKey("Professor")
    communication = models.CharField(max_length=300)

class CompetenceInfo(models.Model):
    professor = models.ForeignKey("Professor")
    informatique = models.CharField(max_length=300)