#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from projectesih.util.fonctionalite import Action
from projectesih.databasemanager import ManageUser, ManageCours, ManageCodeCours, ManageProfesseur
from admin.models import Type, Cours,User,UserProf
from django.db import IntegrityError
from django.shortcuts import redirect
from parametrage.models import CodeCours
from professeur.models import Professor
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
        if not user.type.__eq__(Type.ADMIN):
            profe=UserProf.objects.get(user_id=user.id).professeur
            dic['userprof']=profe
            return redirect("/prof/{}/".format(profe.id))

        try:
            choix = request.POST['choixdash']
            if choix.__eq__('v'):
                codes = CodeCours.objects.all()

                dictio = {}
                c = ""
                for code in codes:
                    dictio[code.grade] = []
                for code in codes:
                    cours = managecours.searchByCode(code)
                    c = "{}--{}".format(c, managecours.calculNbrHreCours(cours))
                    if cours != None:
                        #volumeH.append(managecours.calculNbrHreCours(cours))
                        list = dictio[code.grade]
                        list.append(managecours.calculNbrHreCours(cours))
                        dictio[code.grade] = list
                l = []
                for key, value in dictio.items():
                    color = 'red'
                    if key.__eq__('DUT1'):
                        color = '#83A697'
                    if key.__eq__('DUT2'):
                        color = '#112222'
                    if key.__eq__('L1'):
                        color = '#002277'
                    if key.__eq__('L2'):
                        color = '#8800ee'
                    if key.__eq__('L3'):
                        color = '#ccff44'
                    if key.__eq__('M1'):
                        color = '#83A697'
                    if key.__eq__('M2'):
                        color = '#83A697'
                    l.append((key, sommedictio(value), color))
                if len(l) > 0:
                    dic['dash'] = l
                    dic['max'] = 1200
                    dic['titledash'] = 'volume horaire'
            if choix.__eq__('e'):
                codes = CodeCours.objects.all()

                dictio = {}
                c = ""
                for code in codes:
                    dictio[code.grade] = []
                for code in codes:
                    cours = managecours.searchByCode(code)
                    c = "{}--{}".format(c, cours.ects)
                    if cours != None:
                        #volumeH.append(managecours.calculNbrHreCours(cours))
                        list = dictio[code.grade]
                        list.append(cours.ects)
                        dictio[code.grade] = list
                l = []
                for key, value in dictio.items():
                    color = 'red'
                    if key.__eq__('DUT1'):
                        color = '#83A697'
                    if key.__eq__('DUT2'):
                        color = '#112222'
                    if key.__eq__('L1'):
                        color = '#002277'
                    if key.__eq__('L2'):
                        color = '#8800ee'
                    if key.__eq__('L3'):
                        color = '#ccff44'
                    if key.__eq__('M1'):
                        color = '#83A697'
                    if key.__eq__('M2'):
                        color = '#83A697'
                    l.append((key, sommedictio(value), color))
                if len(l) > 0:
                    dic['dash'] = l
                    dic['max'] = 80
                    dic['titledash'] = 'crédits ECTS'
            if choix.__eq__('-------'):
                codes = CodeCours.objects.all()

                dictio = {}
                c = ""
                for code in codes:
                    dictio[code.grade] = []
                for code in codes:
                    cours = managecours.searchByCode(code)
                    c = "{}--{}".format(c, managecours.calculNbrHreCours(cours))
                    if cours != None:
                    #volumeH.append(managecours.calculNbrHreCours(cours))
                        list = dictio[code.grade]
                        list.append(managecours.calculNbrHreCours(cours))
                        dictio[code.grade] = list
                l = []
                for key, value in dictio.items():
                    color = 'red'
                    if key.__eq__('DUT1'):
                        color = '#83A697'
                    if key.__eq__('DUT2'):
                        color = '#112222'
                    if key.__eq__('L1'):
                        color = '#002277'
                    if key.__eq__('L2'):
                        color = '#8800ee'
                    if key.__eq__('L3'):
                        color = '#ccff44'
                    if key.__eq__('M1'):
                        color = '#83A697'
                    if key.__eq__('M2'):
                        color = '#83A697'
                    l.append((key, sommedictio(value), color))
                if len(l) > 0:
                    dic['dash'] = l
                    dic['max'] = 1200
                    dic['titledash'] = 'volume horaire'
        except:
            codes = CodeCours.objects.all()

            dictio = {}
            c = ""
            for code in codes:
                dictio[code.grade] = []
            for code in codes:
                cours = managecours.searchByCode(code)
                c = "{}--{}".format(c, managecours.calculNbrHreCours(cours))
                if cours != None:
                #volumeH.append(managecours.calculNbrHreCours(cours))
                    list = dictio[code.grade]
                    list.append(managecours.calculNbrHreCours(cours))
                    dictio[code.grade] = list
            l = []
            for key, value in dictio.items():
                color = 'red'
                if key.__eq__('DUT1'):
                    color = '#83A697'
                if key.__eq__('DUT2'):
                    color = '#112222'
                if key.__eq__('L1'):
                    color = '#002277'
                if key.__eq__('L2'):
                    color = '#8800ee'
                if key.__eq__('L3'):
                    color = '#ccff44'
                if key.__eq__('M1'):
                    color = '#83A697'
                if key.__eq__('M2'):
                    color = '#83A697'
                l.append((key, sommedictio(value), color))
            if len(l) > 0:
                dic['dash'] = l
                dic['max'] = 1200
                dic['titledash'] = 'volume horaire'
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
            if not user.type.__eq__(Type.ADMIN):
                profe=UserProf.objects.get(user_id=user.id).professeur
                dic['userprof']=profe
                return redirect("/prof/{}/".format(profe.id))
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
    user = manage.searchById(id)
    html = t.render(Context({'login':True,'type':Type(), 'user':user}))
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

    dic = {'login':True,'cours': cours, 'user':user}
    t = get_template('admin/cours/detailscours.html')
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
    dic = {'login':True}
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
            r=cours.save()
            cours.prof.add(prof)
            return redirect("/admin/cours/objectif/{}/".format(r))
        else:
            t = get_template('admin/cours/desciptioncours.html')
            codecours = managecours.getCodeCours()
            dic['action'] = Action.CREER
            dic['codecours'] = codecours
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
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
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
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
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
    dic['action'] = Action.CREER
    dic['codecours'] = codecours
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
                    user = User(type=type, active=True, username=username, password=password, firstname=firstname, lastname=lastname,email=email)
                    try:
                        valid = True
                        t = get_template('admin/user/form.html')
                        dic = {'login':True,'type':Type(),'action':Action.CREER,'user':user}
                        dic['type1'] = str(type)
                        dic['username'] = str(username)
                        dic['firstname'] = str(firstname)
                        dic['lastname'] = str(lastname)
                        dic['email'] = str(email)

                        if manager.iscreateuser(username):
                            dic['error2'] = 'Already exist'
                            valid = False
                        if manager.isexistmail(email):
                            dic['error6'] = 'Already exist'
                            valid = False
                        if not valid:
                            html = t.render(Context(dic))
                            return HttpResponse(html)
                        user.save()
                        if user.type.__eq__(Type.PROF):
                            prof=Professor()
                            prof.nom=user.lastname
                            prof.prenom=user.firstname
                            p=Professor.objects.get(id=prof.save())
                            userprof=UserProf()
                            userprof.user=user
                            userprof.professeur=p
                            userprof.save()
                        message = "The account {} has created for {} <a href=\"/admin/user/list/\">Retour</a>".format(type,firstname)
                        t = get_template('admin/user/repform.html')
                        html = t.render(Context({'login':True,'message':message,'user':user}))
                        return HttpResponse(html)
                    except  IntegrityError:
                        message = "Error "
                        t = get_template('admin/user/repform.html')
                        html = t.render(Context({'login':True,'message':message,'user':user}))
                        return HttpResponse(html)



