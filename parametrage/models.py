from django.db import models

# Create your models here.

"""Model pour parametrer un etablissement"""
class Etablissement(models.Model):
    nom = models.CharField(max_length=200,unique=True)
    lieu = models.CharField(max_length=400)
    def __unicode__(self):
        return u'%s' % (self.nom)


"""Model pour parametrer un etablissement"""
class CodeProgram(models.Model):
    domaine = models.CharField(max_length=100)
    mention = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    typecours = models.CharField(max_length=100)
    langue = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    def __unicode__(self):
        return u'%s-%s-%s-%s-%s' % (self.domaine,self.mention,self.specialite,self.typecours,self.langue)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(CodeProgram, self).save(force_insert, force_update, using, update_fields)
        self.code = u'%s-%s-%s-%s-%s' % (self.domaine,self.mention,self.specialite,self.typecours,self.langue)
        return  self.id



class CodeCours(models.Model):
    codeprogram = models.ForeignKey(CodeProgram,blank=True, null=True, on_delete=models.SET_NULL)
    etablissement =  models.ForeignKey("Etablissement")
    grade = models.CharField(max_length=200)
    semestre = models.CharField(max_length=3)
    nomcours = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    def __unicode__(self):
        return u'%s' % (self.code)