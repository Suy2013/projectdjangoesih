__author__ = 'Cadichon'
from parametrage.models import Etablissement
from parametrage.models import CodeProgram
from parametrage.models import CodeCours
from admin.models import User, Cours, UserProf
from professeur.models import Professor, Formation, Experience, CompetenceOrg, CompetenceCom, CompetenceInfo
from django.core.mail import EmailMultiAlternatives
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
    def isaffect(self,program):
        for cours in Cours.objects.all():
            if cours.codecours.codeprogram.id==program.id:
                return True
        return False

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
    def isaffect(self,codecours):
        for cours in Cours.objects.all():
            if cours.codecours.id==codecours.id:
                return True
        return False

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
    def createUserProf(self,username,prof):
        password='password'
        user=User(type="Prof", active=True, username=username, password=password, firstname=prof.prenom, lastname=prof.nom,email=prof.email)
        UserProf(user=User.objects.get(id=user.save()),professeur=prof).save()
        subject, from_email, to = 'System descriptif cours ESIH', 'emmanuel.suy@esih.edu', prof.email
        link='<a href="http://ancient-ridge-9094.herokuapp.com/">http://ancient-ridge-9094.herokuapp.com/</a>'
        html_content ='Salut {} {}!<p> Votre compte est << {} >> et mot de passe << {} >>. Cliquer sur ce lien {} pour connecter au systeme descriptif cours de l\'ESIH.</p>'.format(prof.prenom,prof.nom,username,password,link)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        print msg.send()

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

    def searchByCode(self,id):
        cours = Cours.objects.filter(codecours_id=id)
        print "ok......"
        #print "length "+len(cours)
        return cours

    def listall(self):
        list = Cours.objects.all()
        return list

    def listcp(self,id):
        list = Cours.objects.all()
        list1 = []
        for cours in list:
            for prof in cours.prof.all():
                if str(prof.id).__eq__(str(id)):
                    print "add"
                    list1.append(cours)
                print prof.id,id
        print list1
        return list1

    def calculNbrHreCours(self,ects):
        t = ects *  15
        return t


