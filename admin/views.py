#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from projectesih.util.fonctionalite import Action
from projectesih.util.domaine import Domaine
from projectesih.util.mention import Mention
from projectesih.util.gradeEtsemestre import Grade
from projectesih.util.specialite import Specialite
from projectesih.databasemanager import ManageUser, ManageCours, ManageCodeCours, ManageProfesseur
from admin.models import Type, Cours,User,UserProf
from django.db import IntegrityError
from django.shortcuts import redirect
from parametrage.models import CodeCours, CodeProgram
from professeur.models import Professor
from django.core.mail import EmailMultiAlternatives
# Create your views here.

manage = ManageUser()
managecours = ManageCours()
managecodecours = ManageCodeCours()
manageprof = ManageProfesseur()
def sommedictio(l):
    s=0
    for i in l:
        s=s+i
    return s
def home(request):
    comptes = manage.listall()
    if len(comptes)==0:
        User(active=True,username='admin',password='password',lastname='Suy',firstname='Rachele',type=Type.ADMIN).save()
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session != None:
        user = manage.searchById(request.session['userid'])
        dic = {'login':True,'type': Type(), 'action': Action.CREER, 'user': user}
        if user.type.__eq__(Type.PROF):
            profe=UserProf.objects.get(user_id=user.id).professeur
            dic['userprof']=profe
            return redirect("/prof/{}/".format(profe.id))
        try:
            choix = request.GET['choixdash']
        except:
            choix = 'v'
        if choix.__eq__('v'):
            codes = CodeCours.objects.all()
            dictio = {}
            c = ""
            for code in codes:
                if code.codeprogram.domaine.__eq__(Domaine.ST):
                    if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        dictio[code.grade+"ST"] = []
                if code.codeprogram.domaine.__eq__(Domaine.EG):
                    if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        dictio[code.grade+"EG"] = []
                if code.codeprogram.domaine.__eq__(Domaine.EG):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.SDE):
                            dictio[code.grade+"SDE"] = []
                if code.codeprogram.domaine.__eq__(Domaine.EG):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.SC):
                            dictio[code.grade+"SC"] = []
                if code.codeprogram.domaine.__eq__(Domaine.ST):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.TEL):
                            dictio[code.grade+"TEL"] = []
                if code.codeprogram.domaine.__eq__(Domaine.ST):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.BDD):
                            dictio[code.grade+"BDD"] = []
            for code in codes:
                print code
                print code.id
                try:
                    cours = managecours.searchByCode(code.id)
                    #c = "{}--{}".format(c, managecours.calculNbrHreCours(cours))
                    if len(cours)>0:

                     #volumeH.append(managecours.calculNbrHreCours(cours))
                        #return HttpResponse(cours.codecours.nomcours)


                        if code.codeprogram.domaine.__eq__(Domaine.ST):
                            if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                list = dictio[code.grade+"ST"]
                                list.append(managecours.calculNbrHreCours(cours[0].ects))
                                dictio[code.grade+"ST"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.EG):
                            if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                list = dictio[code.grade+"EG"]
                                list.append(managecours.calculNbrHreCours(cours[0].ects))
                                dictio[code.grade+"EG"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.EG):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.SDE):
                                    list = dictio[code.grade+"SDE"]
                                    list.append(managecours.calculNbrHreCours(cours[0].ects))
                                    dictio[code.grade+"SDE"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.EG):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.SC):
                                    list = dictio[code.grade+"SC"]
                                    list.append(managecours.calculNbrHreCours(cours[0].ects))
                                    dictio[code.grade+"SC"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.ST):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.TEL):
                                    list = dictio[code.grade+"TEL"]
                                    list.append(managecours.calculNbrHreCours(cours[0].ects))
                                    dictio[code.grade+"TEL"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.ST):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.BDD):
                                    list = dictio[code.grade+"BDD"]
                                    list.append(managecours.calculNbrHreCours(cours[0].ects))
                                    dictio[code.grade+"BDD"] = list

                except:
                    pass
            l = []
            for key, value in dictio.items():
                color = 'red'
                if key.__eq__('DUT1ST'):
                    color = '#83A697'
                if key.__eq__('DUT2ST'):
                    color = '#83A697'
                if key.__eq__('L1ST'):
                    color = '#83A697'
                if key.__eq__('L2ST'):
                    color = '#83A697'
                if key.__eq__('L3ST'):
                    color = '#83A697'
                if key.__eq__('M1TEL') or key.__eq__('M1BDD'):
                    color = '#83A697'

                if key.__eq__('L1EG'):
                    color = '#6600FF'
                if key.__eq__('L2EG'):
                    color = '#6600FF'
                if key.__eq__('L3EG'):
                    color = '#6600FF'
                if key.__eq__('M1SC') or key.__eq__('M1SDE'):
                    color = '#6600FF'

                if key.__eq__('PropedeutiqueST'):
                    color = '#83A697'

                if key.__eq__('M2'):
                    color = 'red'
                val = sommedictio(value)
                if val >0:
                    if 'ST' in key:
                        key = key.replace('ST','',1)
                    l.append((key, val, color))
            l=sorted(l)
            if len(l) > 0:
                dic['dash'] = l
                dic['max'] = 1200
                dic['titledash'] = 'volume horaire'
        else:
            codes = CodeCours.objects.all()

            dictio = {}
            c = ""
            for code in codes:
                if code.codeprogram.domaine.__eq__(Domaine.ST):
                    if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        dictio[code.grade+"ST"] = []
                if code.codeprogram.domaine.__eq__(Domaine.EG):
                    if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        dictio[code.grade+"EG"] = []
                if code.codeprogram.domaine.__eq__(Domaine.EG):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.SDE):
                            dictio[code.grade+"SDE"] = []
                if code.codeprogram.domaine.__eq__(Domaine.EG):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.SC):
                            dictio[code.grade+"SC"] = []
                if code.codeprogram.domaine.__eq__(Domaine.ST):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.TEL):
                            dictio[code.grade+"TEL"] = []
                if code.codeprogram.domaine.__eq__(Domaine.ST):
                    if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                        if code.codeprogram.specialite.__eq__(Specialite.BDD):
                            dictio[code.grade+"BDD"] = []
            for code in codes:
                print code
                print code.id
                try:
                    cours = managecours.searchByCode(code.id)
                    #c = "{}--{}".format(c, managecours.calculNbrHreCours(cours))
                    if len(cours)>0:

                     #volumeH.append(managecours.calculNbrHreCours(cours))
                        #return HttpResponse(cours.codecours.nomcours)


                        if code.codeprogram.domaine.__eq__(Domaine.ST):
                            if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                list = dictio[code.grade+"ST"]
                                list.append(cours[0].ects)
                                dictio[code.grade+"ST"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.EG):
                            if not code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                list = dictio[code.grade+"EG"]
                                list.append(cours[0].ects)
                                dictio[code.grade+"EG"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.EG):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.SDE):
                                    list = dictio[code.grade+"SDE"]
                                    list.append(cours[0].ects)
                                    dictio[code.grade+"SDE"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.EG):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.SC):
                                    list = dictio[code.grade+"SC"]
                                    list.append(cours[0].ects)
                                    dictio[code.grade+"SC"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.ST):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.TEL):
                                    list = dictio[code.grade+"TEL"]
                                    list.append(cours[0].ects)
                                    dictio[code.grade+"TEL"] = list
                        if code.codeprogram.domaine.__eq__(Domaine.ST):
                            if code.grade.__eq__(Grade.MASTERUN) and not code.grade.__eq__(Grade.MASTERDEUX):
                                if code.codeprogram.specialite.__eq__(Specialite.BDD):
                                    list = dictio[code.grade+"BDD"]
                                    list.append(cours[0].ects)
                                    dictio[code.grade+"BDD"] = list

                except:
                    pass
            l = []
            for key, value in dictio.items():
                color = 'red'
                if key.__eq__('DUT1ST'):
                    color = '#83A697'
                if key.__eq__('DUT2ST'):
                    color = '#83A697'
                if key.__eq__('L1ST'):
                    color = '#83A697'
                if key.__eq__('L2ST'):
                    color = '#83A697'
                if key.__eq__('L3ST'):
                    color = '#83A697'
                if key.__eq__('M1TEL') or key.__eq__('M1BDD'):
                    color = '#83A697'

                if key.__eq__('L1EG'):
                    color = '#6600FF'
                if key.__eq__('L2EG'):
                    color = '#6600FF'
                if key.__eq__('L3EG'):
                    color = '#6600FF'
                if key.__eq__('M1SC') or key.__eq__('M1SDE'):
                    color = '#6600FF'

                if key.__eq__('PropedeutiqueST'):
                    color = '#83A697'

                if key.__eq__('M2'):
                    color = 'red'
                val = sommedictio(value)
                if val >0:
                    if 'ST' in key:
                        key = key.replace('ST','',1)
                    l.append((key, val, color))
            l=sorted(l)
            if len(l) > 0:
                dic['dash'] = l
                dic['max'] = 45
                dic['titledash'] = 'Nombre total credits ECTS'
        t = get_template('admin/index.html')
        html = t.render(Context(dic))
        return HttpResponse(html)

    login = request.POST.get('username')
    password = request.POST.get('password')
    if login!=None and password!=None:
        id = manage.isexistuser(login,password)
        if id!=-1:
            request.session['userid'] = id
            user = manage.searchById(request.session['userid'])
            dic = {'login':True,'type':Type(),'action':Action.CREER, 'user':user}
            if user.type.__eq__(Type.PROF):
                profe=UserProf.objects.get(user_id=user.id).professeur
                dic['userprof']=profe
                return redirect("/profindex/{}/".format(profe.id))
            try:
                choix = request.GET['choixdash']
            except:
                pass
            t = get_template('admin/index.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
    t = get_template('admin/login.html')
    html = t.render(Context({'type':Type(),'action':Action.CREER}))
    return HttpResponse(html)

def logout(request):
    del request.session['userid']
    return redirect("/admin/")


def userform(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    t = get_template('admin/user/form.html')
    html = t.render(Context({'login':True,'type':Type(),'action':Action.CREER,'user':user}))
    return HttpResponse(html)
def deluser(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    try:
        user2 = manage.searchById(id)
    except:
         message = "Une erreur c'est produite!  Le système n'arrive pas à trouver le code demandé."
         dic = {'login':True,'code': '', 'user': user,'message':message,'title':'Avertissement!!!','color':'red'}
         t = get_template('admin/user/repdel.html')
         html = t.render(Context(dic))
         return HttpResponse(html)
    dic = {'login':True,'action': Action.SUCCES_DEL, 'user': user,'id':id,'user2':user2}
    t = get_template('admin/user/repdel.html')
    html = t.render(Context(dic))
    return HttpResponse(html)
def userlist(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])

    t = get_template('admin/user/list.html')
    list = manage.listall()
    html = t.render(Context({'login':True,'type':Type(),'list':list,'user':user}))
    return HttpResponse(html)

def usermodform(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    t = get_template('admin/user/mod.html')
    user1 = manage.searchById(id)
    user = manage.searchById(request.session['userid'])
    html = t.render(Context({'login':True,'type':Type(),'action':Action.CREER, 'user':user,'user1':user1}))
    return HttpResponse(html)


def courslist(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    t = get_template('admin/cours/list.html')
    list = managecours.listall()
    html = t.render(Context({'login':True,'type':Type(),'list':list,'user':user}))
    return HttpResponse(html)


def affectprof(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    try:
        prof = manageprof.searchById(request.POST['idprof'])
        cours = managecours.searchById(request.POST['idcours'])
        cours.prof.add(prof)
        cours.save()
    except KeyError:
        pass

    user = manage.searchById(request.session['userid'])
    cours = managecours.searchById(id)
    professors = manageprof.listall()
    dic = {'login':True,'cours': cours,'list': professors, 'user':user}
    if user.type.__eq__(Type.PROF):
        profe=UserProf.objects.get(user_id=user.id).professeur
        dic['userprof']=profe
    t = get_template('admin/cours/affectprof.html')
    html = t.render(Context(dic))
    return HttpResponse(html)

def detailscours(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")

    user = manage.searchById(request.session['userid'])
    cours = managecours.searchById(id)

    list = managecours.listall()
    dic = {'login':True,'imprimmer':True, 'cours': cours, 'user':user, 'list':list}
    if user.type.__eq__("Prof"):
        p=manageprof.getProf(user)
        dic['userprof']=p
    t = get_template('admin/cours/detailscours.html')
    html = t.render(Context(dic))
    return HttpResponse(html)

def delcours(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    if request.method=='POST':
        cours = Cours.objects.get(id=request.POST['id'])
        for r in cours.prerequis.all():
            cours.prerequis.remove(r)

        for prof in cours.prof.all():
            cours.prof.remove(prof)
        cours.delete()
        return redirect('/admin/cours/')
    try:

        cours = Cours.objects.get(id=id)

    except:
        message = "Une erreur c'est produite!  Le système n'arrive pas à trouver le code demandé."
        dic = {'login':True,'nom': '', 'user': user,'message':message,'color':'red','title':'Avertissement!!!'}
        t = get_template('admin/cours/succdel.html')
        html = t.render(Context(dic))
        return HttpResponse(html)
    dic = {'login':True,'action': Action.SUCCES_DEL, 'user': user,'id':id,'cours':cours}
    t = get_template('admin/cours/repdel.html')
    html = t.render(Context(dic))
    return HttpResponse(html)

def coursform(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    professors =  ManageProfesseur().listall()
    dic = {'login':True,'list':Cours.objects.all()}
    dic['user'] = user
    dic['professors'] = professors
    if 'action' in request.POST:
        valid = True
        public = []
        format = []
        if 'codecours' in request.POST:
            codecours = request.POST['codecours']
            dic['codecours'] = codecours
        else:
            valid = False
            dic['error1'] = "Vous devriez choisir un code cours"
        if 'ects' in request.POST:
            ects = request.POST['ects']
            dic['ects'] = ects
            if str(ects).__eq__(''):
                valid = False
                dic['error2'] = "Vous devriez choisir un credit ECTS"
        else:
            valid = False
            dic['error2'] = "Vous devriez choisir un credit ECTS"
        if 'prof' in request.POST:
            prof = ManageProfesseur().searchById(request.POST['prof'])

            dic['prof'] = prof
            if str(prof).__eq__(''):
                valid = False
                dic['error3'] = "Vous devriez choisir un ou plusieurs professeurs"
        else:
            valid = False
            dic['error3'] = "Vous devriez choisir un ou plusieurs professeurs"

        if 'prerequis' in request.POST:
            prerequis = request.POST['prerequis']

        if 'public_e' in request.POST:
            public.append(request.POST['public_e'])

        if 'public_p' in request.POST:
            public.append(request.POST['public_e'])

        if 'public_a' in request.POST:
            if 'public_autre' in request.POST:
                public.append(request.POST['public_autre'])

        if not 'public_a' and not 'public_e' and not 'public_p'  in request.POST:
            valid = False
            dic['error6'] = "Vous devriez choisir au moins un public cible"

        if 'magistrale' in request.POST:
            format.append(request.POST['magistrale'])

        if 'td' in request.POST:
            format.append(request.POST['td'])

        if 'tp' in request.POST:
            format.append(request.POST['tp'])

        if 'a' in request.POST:
            if 'autre' in request.POST:
                format.append(request.POST['autre'])

        if not 'td' and not 'ip' and not 'magistrale' and not 'a'  in request.POST:
            valid = False
            dic['error6'] = "Vous devriez choisir au moins un public cible"

        if valid:
            code = managecodecours.searchById(codecours)
            cours = Cours(codecours=code, ects=ects, public=public, format=format)
            try:
                r=cours.save()
                cours.prof.add(prof)
                if prerequis:
                    crs = Cours.objects.get(id=prerequis)
                    if crs.codecours!=cours.codecours:
                        cours.prerequis.add(crs)
                return redirect("/admin/cours/objectif/{}/".format(r))
            except IntegrityError:
                dic['errorintegrite'] = 'Ce code existe deja pour un cours'
                valid = False

        if not valid:
            t = get_template('admin/cours/desciptioncours.html')
            codecours = managecours.getCodeCours()
            dic['action'] = Action.CREER
            dic['codecours'] = codecours
            if user.type.__eq__("Prof"):
                p=manageprof.getProf(user)
                dic['userprof']=p
            html = t.render(Context(dic))
            return HttpResponse(html)

    t = get_template('admin/cours/desciptioncours.html')
    codecours = managecours.getCodeCours()
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
    html = t.render(Context(dic))
    return HttpResponse(html)

def coursobjectif(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = {'login':True}
    dic['id']= id
    dic['request'] = request
    dic['user'] = user
    valid = True
    if 'action' in request.POST:
        if 'objectif' in request.POST:
            objectif = request.POST['objectif']
            if str(objectif).__eq__(''):
                valid = False
                dic['error1'] = "Vous devez definir l'objectif du cours"
            if valid:
                cours = managecours.searchById(id)
                cours.objectif = objectif
                r = cours.save()
                return redirect("/admin/cours/description/{}/".format(r),permanent=True)
    cours = managecours.searchById(id)
    dic['cours']=cours
    if user.type.__eq__("Prof"):
        p=manageprof.getProf(user)
        dic['userprof']=p
    t = get_template('admin/cours/objectifs.html')
    codecours = managecours.getCodeCours()
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
    html = t.render(Context(dic))
    return HttpResponse(html)

def coursdescription(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = {'login':True}
    dic['user'] = user
    dic['id']= id
    dic['request'] = request
    valid = True
    if 'action' in request.POST:
        if 'description' in request.POST:
            description = request.POST['description']
            if str(description).__eq__(''):
                valid = False
                dic['error1'] = "Vous devez definir la description du cours"
            if valid:
                cours = managecours.searchById(id)
                cours.description = description
                r = cours.save()
                return redirect("/admin/cours/plan/{}/".format(r),permanent=True)

    t = get_template('admin/cours/description.html')
    codecours = managecours.getCodeCours()
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
    if user.type.__eq__("Prof"):
        p=manageprof.getProf(user)
        dic['userprof']=p
    cours = managecours.searchById(id)
    dic['cours']=cours
    html = t.render(Context(dic))
    return HttpResponse(html)

def coursplan(request, id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = {'login':True}
    dic['user'] = user
    dic['id']= id
    dic['request'] = request
    valid = True
    if 'action' in request.POST:
        if 'plan' in request.POST:
            plan = request.POST['plan']
            if str(plan).__eq__(''):
                valid = False
                dic['error1'] = "Vous devez definir la description du cours"
            if valid:
                cours = managecours.searchById(id)
                cours.plan = plan
                r = cours.save()
                return redirect("/admin/cours/ressource/{}/".format(r),permanent=True)

    t = get_template('admin/cours/plan.html')
    codecours = managecours.getCodeCours()
    cours = managecours.searchById(id)
    dic['cours']=cours
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
    if user.type.__eq__("Prof"):
        p=manageprof.getProf(user)
        dic['userprof']=p
    html = t.render(Context(dic))
    return HttpResponse(html)

def coursressource(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = {'login':True}
    dic['user'] = user
    dic['id']= id
    dic['request'] = request
    valid = True
    if 'action' in request.POST:
        if 'ressource' in request.POST:
            ressource = request.POST['ressource']
            if str(ressource).__eq__(''):
                valid = False
                dic['error1'] = "Vous devez definir des ressources pour le cours"
            if valid:
                cours = managecours.searchById(id)
                cours.ressource = ressource
                r = cours.save()
                return redirect("/admin/cours/evaluation/{}/".format(r),permanent=True)

    t = get_template('admin/cours/ressource.html')
    codecours = managecours.getCodeCours()
    cours = managecours.searchById(id)
    dic['cours']=cours
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
    if user.type.__eq__("Prof"):
        p=manageprof.getProf(user)
        dic['userprof']=p
    html = t.render(Context(dic))
    return HttpResponse(html)

def coursevaluation(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = {'login':True}
    dic['user'] = user
    dic['id']= id
    dic['request'] = request
    valid = True
    if 'action' in request.POST:
        if 'evaluation' in request.POST:
            evaluation = request.POST['evaluation']
            if str(evaluation).__eq__(''):
                valid = False
                dic['error1'] = "Vous devez definir l'evaluation du cours"
            if valid:
                cours = managecours.searchById(id)
                cours.evaluation = evaluation
                cours.save()
                return redirect("/admin/cours/",permanent=True)

    t = get_template('admin/cours/evaluation.html')
    codecours = managecours.getCodeCours()
    cours = managecours.searchById(id)
    dic['cours']=cours
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
    if user.type.__eq__("Prof"):
        p=manageprof.getProf(user)
        dic['userprof']=p
    html = t.render(Context(dic))
    return HttpResponse(html)

def controlleruser(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    manager = ManageUser()
    action = request.POST['action'];
    if action is not None:
        if str(action).__eq__(''):
            return ''
        else:
            if str(action).__eq__(Action.CREER):
                type = request.POST['type']
                username = request.POST['username']
                password = request.POST['password']
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                email = request.POST['email']
                if type!=None and username!=None and password!=None and firstname!=None and lastname!=None and email!=None:
                    user1 = User(type=type, active=True, username=username, password=password, firstname=firstname, lastname=lastname,email=email)
                    try:
                        user1.id=request.POST['id']
                    except:
                        pass
                    try:
                        valid = True
                        t = get_template('admin/user/form.html')
                        dic = {'login':True,'type':Type(),'action':Action.CREER,'user':user}
                        dic['type1'] = str(type)
                        dic['username'] = str(username)
                        dic['firstname'] = str(firstname)
                        dic['lastname'] = str(lastname)
                        dic['email'] = str(email)
                        if 'id' in request.POST:
                            if manager.iscreateuser(username):
                                dic['error2'] = 'Already exist'
                                valid = False
                            if manager.isexistmail(email):
                                dic['error6'] = 'Already exist'
                                valid = False
                        if not valid:
                            html = t.render(Context(dic))
                            return HttpResponse(html)
                        user1.save()
                        if user1.type.__eq__(Type.PROF):
                            prof=Professor()
                            prof.nom=user1.lastname
                            prof.prenom=user1.firstname
                            prof.email=user1.email
                            p=Professor.objects.get(id=prof.save())
                            userprof=UserProf()
                            userprof.user=user1
                            userprof.professeur=p
                            userprof.save()
                            subject, from_email, to = 'System descriptif cours ESIH', 'emmanuel.suy@esih.edu', prof.email
                            link='<a href="http://ancient-ridge-9094.herokuapp.com/">http://ancient-ridge-9094.herokuapp.com/</a>'
                            html_content ='Salut {} {}!<p> Votre compte est << {} >> et mot de passe << {} >>. Cliquer sur ce lien {} pour connecter au systeme descriptif cours de l\'ESIH.</p>'.format(prof.prenom,prof.nom,username,password,link)
                            msg = EmailMultiAlternatives(subject, '', from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                        message = "The account {} has created for {} <a href=\"/admin/user/list/\">Retour</a>".format(type,firstname)
                        t = get_template('admin/user/repform.html')
                        html = t.render(Context({'login':True,'message':message,'user':user}))
                        return HttpResponse(html)
                    except  IntegrityError:
                        message = "Error "
                        t = get_template('admin/user/repform.html')
                        html = t.render(Context({'login':True,'message':message,'user':user}))
                        return HttpResponse(html)

            if str(request.POST['action']).__eq__(Action.SUCCES_DEL):
                #try:
                user2 = manage.searchById(request.POST['id'])
                if user2.type.__eq__(Type.PROF):
                    userp=UserProf.objects.filter(user_id=user2.id)[0]
                    p = Professor.objects.get(id=userp.professeur.id)
                    for us in UserProf.objects.all():
                        if us.id==user2.id:
                            us.delete()
                    p.delete()

                user2.delete()
                title = 'Supression'
                message = "{} a ete suprimé avec succès.".format(user2)
                color='#999999'
                #except:
                    # title = 'Avertissement!!!'
                    # color ='red'
                    # message = "Une erreur c'est produite!  Le système n'arrive pas à supprimer l'utilisateur demandé."

            dic = {'login':True,'nom': '', 'user': user,'message':message,'color':color,'title':title}
            t = get_template('admin/user/succdel.html')
            html = t.render(Context(dic))
            return HttpResponse(html)

def seach(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    list = []
    try:
        query = request.GET['q']
        try:
        #Codecours query
            lstid = []
            try:
                lstid = CodeCours.objects.extra(where=["code LIKE %s"], params=['%'+query+'%'])
            except:
                pass
            try:
                lst = CodeCours.objects.extra(where=["nomcours LIKE %s"], params=['%'+query+'%'])
                if len(lst)>0:
                    for it in lst:
                        lstid.append(it)
            except:
                pass
            if len(lstid):
                for cod in lstid:
                    try:
                        cours = Cours.objects.get(codecours_id=cod.id)
                        list.append(("Cours","/admin/cours/details/{}/".format(cours.id),cours.codecours.nomcours))
                    except:
                        pass
        except:
            pass

        try:
            lstid = CodeProgram.objects.extra(where=["code LIKE %s"], params=['%'+query+'%'])
            print lstid
            for cod in lstid:
                try:
                    codcours = CodeCours.objects.get(codeprogram_id=cod.id)
                    cours = Cours.objects.get(codecours_id=codcours.id)
                    list.append(("Cours","/admin/cours/details/{}/".format(cours.id),cours.codecours.nomcours))
                except:
                    pass
        except:
            pass

        try:
            lstid = []
            lst = User.objects.extra(where=["firstname LIKE %s"], params=['%'+query+'%'])
            if len(lst)>0:
                for it in lst:
                    lstid.append(it)

            lst = User.objects.extra(where=["lastname LIKE %s"], params=['%'+query+'%'])
            if len(lst)>0:
                for it in lst:
                    lstid.append(it)

            lst = User.objects.extra(where=["username LIKE %s"], params=['%'+query+'%'])
            if len(lst)>0:
                for it in lst:
                    lstid.append(it)

            print lstid

            # lst = User.objects.extra(where=["firstname LIKE %s"], params=['%'+query+'%'])
            # if len(lst)>0:
            #     lstid.append(it for it in lst)
            print lstid
            for u in lstid:
                if u.type.__eq__(Type.PROF):
                    try:
                        prof = UserProf.objects.get(user_id=u.id).professeur
                        desc = UserProf.objects.get(user_id=u.id).user.firstname+' '+UserProf.objects.get(user_id=u.id).user.lastname
                        try:
                            for co in Cours.objects.all():
                                for p in co.prof.all():
                                    if p.id == prof.id:
                                        desc = desc + "<br/>--"+co.codecours.nomcours
                        except:
                            pass

                        list.append(("Professeur","/viewcv/{}/".format(prof.id),desc))
                    except:
                        pass
        except:
            pass

    except:
        pass
    t = get_template('admin/search.html')
    html = t.render(Context({'login':True,'type':Type(),'list':list,'user':user}))
    return HttpResponse(html)


