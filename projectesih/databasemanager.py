__author__ = 'Cadichon'
from parametrage.models import Etablissement
from parametrage.models import CodeProgram
from parametrage.models import CodeCours
from admin.models import User, Cours, UserProf
from professeur.models import Professor, Formation, Experience, CompetenceOrg, CompetenceCom, CompetenceInfo
class ManageEtablissement:
    def save(self,etablissement):
        etablissement.save()

    def listall(self):
        list = Etablissement.objects.all()
        return list

    def searchById(self,id):
        etablissement = Etablissement.objects.get(id=id)
        return etablissement

class ManageCodeProgram:
    def save(self,codeprogram):
        codeprogram.save()

    def listall(self):
        list = CodeProgram.objects.all()
        return list

    def searchById(self,id):
        codeprogram = CodeProgram.objects.get(id=id)
        return codeprogram

    def existingcode(self,codeprogram):
        list = CodeProgram.objects.filter(domaine=codeprogram.domaine,mention=codeprogram.mention,specialite=codeprogram.specialite,typecours=codeprogram.typecours,langue=codeprogram.langue)
        if len(list)>0:
            return True
        else:
            return False
    def code(self,codeprogram):
        cod = "{}-{}-{}-{}-{}".format(codeprogram.domaine,codeprogram.mention,codeprogram.specialite,codeprogram.typecours,codeprogram.langue)
        return cod
class ManageCodeCours:
    def save(self,codecours):
        codecours.save()

    def listall(self):
        list = CodeCours.objects.all()
        return list

    def searchById(self,id):
        codecours = CodeCours.objects.get(id=id)
        return codecours
    def loadEtablissement(self):
        list = Etablissement.objects.all()
        return list
    def findEtablissement(self,id):
        etablissement = Etablissement.objects.get(id=id)
        return etablissement

class ManageUser:
    def isexistuser(self,username,password):
        users = User.objects.filter(username=username)
        if len(users)>0:
            for user in users:
                if user.password==password:
                    return user.id
        else:
            return -1

    def iscreateuser(self,username):
        users = User.objects.filter(username=username)
        if len(users)>0:
            return True
        else:
            return False

    def isexistmail(self,email):
        user = User.objects.filter(email=email)
        if len(user)>0:
            return True
        else:
            return False

    def listall(self):
        list = User.objects.all()
        return list
    def searchById(self,id):
        user = User.objects.get(id=id)
        return user
class ManageProfesseur:
    def isexistmail(self,email):
        user = User.objects.filter(email=email)
        if len(user)>0:
            return True
        else:
            return False

    def listall(self):
        list = Professor.objects.all()
        return list

    def searchById(self,id):
        professor = Professor.objects.get(id=id)
        return professor

    def searchFormation(self,professor):
        list = Formation.objects.filter(professor_id=professor.id)
        return list

    def searchExperience(self,professor):
        list = Experience.objects.filter(professor_id=professor.id)
        return list


    def searchCompetenceOrg(self,professor):
        list = CompetenceOrg.objects.filter(professor_id=professor.id)
        return list

    def searchCompetenceCom(self,professor):
        list = CompetenceCom.objects.filter(professor_id=professor.id)
        return list

    def searchCompetenceInfo(self,professor):
        list = CompetenceInfo.objects.filter(professor_id=professor.id)
        return list
    def getProf(self,user):
        return UserProf.objects.get(user_id=user.id).professeur

class ManageCours:
    def getCodeCours(self):
        return CodeCours.objects.all()

    def searchById(self,id):
        cours = Cours.objects.get(id=id)
        return cours
    def searchByCode(self,code):
        cours = Cours.objects.filter(codecours_id=code.id)
        return cours[0]
    def listall(self):
        list = Cours.objects.all()
        return list
    def calculNbrHreCours(self,cours):
        return cours.ects *  15


