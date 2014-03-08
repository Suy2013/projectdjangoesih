#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
from projectesih.databasemanager import ManageEtablissement
from projectesih.databasemanager import ManageCodeProgram
from projectesih.databasemanager import ManageCodeCours, ManageUser
from parametrage.models import CodeProgram
from parametrage.models import CodeCours
from parametrage.models import Etablissement
from projectesih.util.fonctionalite import Action
from projectesih.util.domaine import Domaine
from projectesih.util.mention import Mention
from projectesih.util.gradeEtsemestre import Grade
from projectesih.util.specialite import Specialite
from projectesih.util.gradeEtsemestre import Semestre
# Create your views here.

"""Views et controller etablissement"""
manageEtablissement = ManageEtablissement()
manage = ManageUser()


def listetablissement(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = manageEtablissement.listall()
    listaction = {'mod': Action.MODIFIER, 'del': Action.DEL}
    t = get_template('parametrage/etablissement/list.html')

    html = t.render(Context({'login':True,'list': dic, 'mod': Action.MODIFIER, 'del': Action.DEL, 'user': user}))
    return HttpResponse(html)


def formetablissement(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = {'login':True,'action': Action.CREER, 'user': user}
    t = get_template('parametrage/etablissement/form.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def modetablissement(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    try:
        title = 'Modification'
        etablissement = manageEtablissement.searchById(id)
        color = '#999999'
    except:
        title = "Avertissement!!!"
        color = 'red'
        message = "Une erreur c'est produite!  Le système n'arrive pas à trouver l'établissement demandé."
        dic = {'login':True,'nom': '', 'user': user,'message':message,'color':color,'title':title}
        t = get_template('parametrage/etablissement/repmod.html')
        html = t.render(Context(dic))
        return HttpResponse(html)
    dic = {'login':True,'nom': etablissement.nom, 'lieu': etablissement.lieu, 'action': Action.SUCCES_MOD, 'user': user,'id':id}
    t = get_template('parametrage/etablissement/modform.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def deletablissement(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])


    try:
           etablissement = manageEtablissement.searchById(id)
    except:
        message = "Une erreur c'est produite!  Le système n'arrive pas à trouver l'établissement demandé."

        dic = {'login':True,'nom': '', 'user': user,'message':message,'color':'red','title':'Avertissement!!!'}
        t = get_template('parametrage/etablissement/succdel.html')
        html = t.render(Context(dic))
        return HttpResponse(html)
    dic = {'login':True,'action': Action.SUCCES_DEL, 'user': user,'id':id,'title':'Supression éffectuée avec succès.'}
    t = get_template('parametrage/etablissement/repdel.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def controlleretablissement(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    if 'action' in request.POST:
        if str(request.POST['action']).__eq__(Action.CREER):
            dic = {'login':True}
            dic['user'] = user
            empty = False
            if str(request.POST['nom']).__eq__(''):
                dic['error1'] = 'Field empty'
                empty = True
            if str(request.POST['lieu']).__eq__(''):
                dic['error2'] = 'Field empty'
                empty = True
            if empty:
                t = get_template('parametrage/etablissement/form.html')
                html = t.render(Context(dic))
                return HttpResponse(html)
            dic['nom'] = request.POST['nom']
            etablissement = Etablissement(nom=str(request.POST['nom']), lieu=str(request.POST['lieu']))
            manageEtablissement.save(etablissement)
            t = get_template('parametrage/etablissement/repform.html')
            html = t.render(Context(dic))
            return HttpResponse(html)

        if str(request.POST['action']).__eq__(Action.SUCCES_DEL):
            try:
                etab = manageEtablissement.searchById(request.POST['id'])
                etab.delete()
                title = 'Supression'
                message = "L'établissement {} a ete suprimé avec succès.".format(etab)
                color='#999999'
            except:
                title = 'Avertissement!!!'
                color ='red'
                message = "Une erreur c'est produite!  Le système n'arrive pas à supprimer l'établissement demandé."

            dic = {'login':True,'nom': '', 'user': user,'message':message,'color':color,'title':title}
            t = get_template('parametrage/etablissement/succdel.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
        if str(request.POST['action']).__eq__(Action.SUCCES_MOD):
            dic = {'login':True,'action': Action.SUCCES_MOD, 'user': user}
            empty = False
            id = request.POST['id']
            dic['id']=id
            if str(request.POST['nom']).__eq__(''):
                dic['error1'] = 'Field empty'
                empty = True
            else:
                dic['nom'] = request.POST['nom']

            if str(request.POST['lieu']).__eq__(''):
                dic['error2'] = 'Field empty'
                empty = True
            else:
                dic['lieu'] = request.POST['lieu']
            if empty:
                return redirect('/parametrage/etablissement/change/{}/'.format(id))
            etablissement = manageEtablissement.searchById(request.POST['id'])
            etablissement.nom = request.POST['nom']
            etablissement.lieu = request.POST['lieu']
            etablissement.save()
            title = 'Modification'
            message = 'La modification de {} a été fait avec succès'.format(etablissement)
            dic['message'] = message
            dic['title'] = title
            t = get_template('parametrage/etablissement/repmod.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
        else:
            return HttpResponse("error...{}...".format(request.POST['action']))
    return redirect('/parametrage/etablissement/list/')


"""FIN"""

"""Views et controller codecours"""

"""Views"""
manageCodeCours = ManageCodeCours()


def formcodecours(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    t = get_template("parametrage/codecours/form.html")
    grade = Grade()
    semestre = Semestre()
    list = manageCodeCours.loadEtablissement()
    listprogram = manageCodeProgram.listall()
    dic = {'login':True,'grade': grade, 'semestre': semestre, 'etablissements': list, 'listprogram': listprogram,
           'action': Action.CREER, 'user': user}
    html = t.render(Context(dic))
    return HttpResponse(html)


def listcodecours(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    dic = manageCodeCours.listall()
    user = manage.searchById(request.session['userid'])
    listaction = {'mod': Action.MODIFIER, 'del': Action.DEL}
    t = get_template('parametrage/codecours/list.html')
    html = t.render(Context({'login':True,'list': dic, 'mod': Action.MODIFIER, 'del': Action.DEL, 'user': user}))
    return HttpResponse(html)


def modcodecours(request, id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    try:
        codecours = manageCodeCours.searchById(id)
    except:
         message = "Une erreur c'est produite!  Le système n'arrive pas à trouver le code demandé."
         dic = {'login':True,'code': '', 'user': user,'message':message,'title':'Avertissement!!!','color':'red'}
         t = get_template('parametrage/codecours/repmod.html')
         html = t.render(Context(dic))
         return HttpResponse(html)

    grade = Grade()
    semestre = Semestre()
    list = manageCodeCours.loadEtablissement()
    dic = {'login':True,'grade': grade, 'semestre': semestre, 'etablissements': list, 'code': codecours,
    'action': Action.SUCCES_MOD, 'user': user}
    t = get_template('parametrage/codecours/modform.html')
    html = t.render(Context(dic))
    return HttpResponse(html)



def delcodecours(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    try:
        codecours = manageCodeCours.searchById(id)
    except:
         message = "Une erreur c'est produite!  Le système n'arrive pas à trouver le code demandé."
         dic = {'login':True,'code': '', 'user': user,'message':message,'title':'Avertissement!!!','color':'red'}
         t = get_template('parametrage/codecours/repmod.html')
         html = t.render(Context(dic))
         return HttpResponse(html)
    dic = {'action': Action.SUCCES_DEL, 'user': user,'id':id}
    t = get_template('parametrage/codecours/repdel.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def controllercodecours(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    if request.POST['action']:
        if str(request.POST['action']).__eq__(Action.CREER):
            dic = {'login':True}
            dic['user'] = user
            empty = False
            if str(request.POST['grade']).__eq__(''):
                dic['error1'] = 'Field empty'
                empty = True
            if str(request.POST['semestre']).__eq__(''):
                dic['error2'] = 'Field empty'
                empty = True
            if empty:
                t = get_template('parametrage/codecours/form.html')
                html = t.render(Context(dic))
                return HttpResponse(html)
            etablissement = manageCodeCours.findEtablissement(str(request.POST['etablissement']))
            codeprogram=manageCodeProgram.searchById(request.POST['program'])
            codecours = CodeCours(codeprogram=codeprogram, etablissement=etablissement, nomcours=str(request.POST['nomcours']),
                                  grade=str(request.POST['grade']), semestre=str(request.POST['semestre']))
            codecours.code = "{}-{}{}-{}".format(etablissement.nom, str(request.POST['grade']),
                                                 str(request.POST['semestre']), str(request.POST['nomcours']))
            manageCodeCours.save(codecours)
            dic = {'message': "L'enregistrement {} a été effectué avec succès.".format(codecours.code) , 'user': user}
            t = get_template('parametrage/codecours/repform.html')
            html = t.render(Context(dic))
            return HttpResponse(html)

        # if str(request.POST['action']).__eq__(Action.DEL):
        #     id = request.POST['id']
        #     dic = {'action': Action.SUCCES_DEL, 'user': user}
        #     t = get_template('parametrage/codecours/repdel.html')
        #     html = t.render(Context(dic))
        #    return HttpResponse(html)
        if str(request.POST['action']).__eq__(Action.SUCCES_DEL):
            try:
                codecours = manageCodeCours.searchById(request.POST['id'])
                codecours.delete()
                title = 'Supression'
                message = "{} a ete suprimé avec succès.".format(codecours)
                color='#999999'
            except:
                title = 'Avertissement!!!'
                color ='red'
                message = "Une erreur c'est produite!  Le système n'arrive pas à supprimer le code demandé."

            dic = {'login':True,'nom': '', 'user': user,'message':message,'color':color,'title':title}
            t = get_template('parametrage/codecours/succdel.html')
            html = t.render(Context(dic))
            return HttpResponse(html)

        # if str(request.POST['action']).__eq__(Action.MODIFIER):
        #     id = request.GET['id']
        #     codecours = manageCodeCours.searchById(id)
        #     grade = Grade()
        #     semestre = Semestre()
        #     list = manageCodeCours.loadEtablissement()
        #     dic = {'grade': grade, 'semestre': semestre, 'etablissements': list, 'code': codecours,
        #            'action': Action.SUCCES_MOD, 'user': user}
        #     t = get_template('parametrage/codecours/modform.html')
        #     html = t.render(Context(dic))
        #     return HttpResponse(html)
        if str(request.POST['action']).__eq__(Action.SUCCES_MOD):
            dic = {'code': '', 'user': user}
            codecours = manageCodeCours.searchById(request.POST['id'])
            empty = False
            if str(request.POST.get('domaine')).__eq__(''):
                dic['error1'] = 'Field empty'
                empty = True
            if str(request.POST.get('mention')).__eq__(''):
                dic['error2'] = 'Field empty'
                empty = True
            if str(request.POST.get('specialite')).__eq__(''):
                dic['error3'] = 'Field empty'
                empty = True
            if str(request.POST.get('typecours')).__eq__(''):
                dic['error3'] = 'Field empty'
                empty = True
            if str(request.POST.get('langue')).__eq__(''):
                dic['error4'] = 'Field empty'
                empty = True
            if empty:
                dic['code'] = codecours
                t = get_template('parametrage/codecours/form.html')
                html = t.render(Context(dic))
                return HttpResponse(html)
            else:
                codecours.domaine = request.POST.get('domaine')
                codecours.mention = request.POST.get('mention')
                codecours.specialite = request.POST.get('specialite')
                codecours.typecours = request.POST.get('typecours')
                codecours.langue = request.POST.get('langue')
                codecours.save()
            message='Le code programme a été modifié avec succès.'
            dic['message'] = message

            t = get_template('parametrage/codecours/repmod.html')
            html = t.render(Context(dic))
            return HttpResponse(html)


"""FIN"""

"""Views et controller codeprogram"""

"""Views"""
manageCodeProgram = ManageCodeProgram()


def formcodeprogram(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    t = get_template("parametrage/codeprogram/form.html")
    domaine = Domaine()
    mention = Mention()
    grade = Grade()
    specialite = Specialite()
    dic = {'login':True,'domaine': domaine, 'mention': mention, 'grade': grade, 'specialite': specialite, 'action': Action.CREER,
           'user': user}
    html = t.render(Context(dic))
    return HttpResponse(html)


def modcodeprogram(request, id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    try:
        codeprogram = manageCodeProgram.searchById(id)

    except:
        message = "Une erreur c'est produite!  Le système n'arrive pas à trouver le code demandé."
        dic = {'login':True,'nom': '', 'user': user,'message':message,'color':'red','title':'Avertissement!!!'}
        t = get_template('parametrage/codeprogram/succdel.html')
        html = t.render(Context(dic))
        return HttpResponse(html)
    codeprogram = manageCodeProgram.searchById(id)
    dic = {'login':True,'code': codeprogram,
           'action': Action.SUCCES_MOD, 'user': user,'id':id}
    t = get_template('parametrage/codeprogram/modform.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def delcodeprogram(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    try:
        codeprogram = manageCodeProgram.searchById(id)

    except:
        message = "Une erreur c'est produite!  Le système n'arrive pas à trouver le code demandé."
        dic = {'login':True,'nom': '', 'user': user,'message':message,'color':'red','title':'Avertissement!!!'}
        t = get_template('parametrage/codeprogram/succdel.html')
        html = t.render(Context(dic))
        return HttpResponse(html)
    dic = {'login':True,'action': Action.SUCCES_DEL, 'user': user,'id':id,'codeprogram':codeprogram}
    t = get_template('parametrage/codeprogram/repdel.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def listcodeprogram(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])
    dic = manageCodeProgram.listall()
    listaction = {'mod': Action.MODIFIER, 'del': Action.DEL}
    t = get_template('parametrage/codeprogram/list.html')
    html = t.render(Context({'login':True,'list': dic, 'mod': Action.MODIFIER, 'del': Action.DEL, 'user': user}))
    return HttpResponse(html)


def controllercodeprogram(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session == None:
        return redirect("/admin/")
    user = manage.searchById(request.session['userid'])

    if request.POST['action']:
        if str(request.POST.get('action')).__eq__(Action.CREER):
            dic = {'login':True}
            dic['user'] = user
            empty = False
            if str(request.POST.get('domaine')).__eq__(''):
                dic['error1'] = 'Field empty'
                empty = True
            if str(request.POST.get('mention')).__eq__(''):
                dic['error2'] = 'Field empty'
                empty = True
            if str(request.POST.get('specialite')).__eq__(''):
                dic['error3'] = 'Field empty'
                empty = True
            if str(request.POST.get('typecours')).__eq__(''):
                dic['error3'] = 'Field empty'
                empty = True
            if str(request.POST.get('langue')).__eq__(''):
                dic['error4'] = 'Field empty'
                empty = True
            if empty:
                t = get_template('parametrage/codeprogram/form.html')
                html = t.render(Context(dic))
                return HttpResponse(html)
            codeprogram = CodeProgram(domaine=str(request.POST.get('domaine')),
                                      mention=str(request.POST.get('mention')),
                                      specialite=str(request.POST.get('specialite')),
                                      typecours=str(request.POST.get('typecours')),
                                      langue=str(request.POST.get('langue')))
            dic = {'login':True,'code': manageCodeProgram.code(codeprogram), 'user': user}
            if not manageCodeProgram.existingcode(codeprogram):
                manageCodeProgram.save(codeprogram)
                t = get_template('parametrage/codeprogram/repform.html')
                html = t.render(Context(dic))
                return HttpResponse(html)

        # if str(request.POST['action']).__eq__(Action.DEL):
        #     id = request.POST['id']
        #     dic = {'action': Action.SUCCES_DEL, 'user': user}
        #     t = get_template('parametrage/codeprogram/repdel.html')
        #     html = t.render(Context(dic))
        #     return HttpResponse(html)
        if str(request.POST['action']).__eq__(Action.SUCCES_DEL):
            try:
                codeprogram = manageCodeProgram.searchById(request.POST['id'])
                codeprogram.delete()
                title = 'Supression'
                message = "{} a ete suprimé avec succès.".format(codeprogram)
                color='#999999'
            except:
                title = 'Avertissement!!!'
                color ='red'
                message = "Une erreur c'est produite!  Le système n'arrive pas à supprimer le code demandé."

            dic = {'login':True,'nom': '', 'user': user,'message':message,'color':color,'title':title}
            t = get_template('parametrage/codeprogram/succdel.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
            # if str(request.POST.get('action')).__eq__(Action.MODIFIER):
        #     id = request.POST['id']
        #     codeprogram = manageCodeProgram.searchById(id)
        #     grade = Grade()
        #     dic = {'domaine': codeprogram.domaine, 'mention': codeprogram.mention, 'specialite': codeprogram.specialite,
        #        'typecours': codeprogram.typecours, 'langue': codeprogram.langue, 'grade': grade,
        #        'action': Action.SUCCES_MOD,'user':user}
        #     t = get_template('parametrage/codeprogram/modform.html')
        #     html = t.render(Context(dic))
        #     return HttpResponse(html)
        if str(request.POST['action']).__eq__(Action.SUCCES_MOD):
            codeprogram = manageCodeProgram.searchById(request.POST['id'])
            empty = False
            if str(request.POST.get('domaine')).__eq__(''):
                dic['error1'] = 'Field empty'
                empty = True
            if str(request.POST.get('mention')).__eq__(''):
                dic['error2'] = 'Field empty'
                empty = True
            if str(request.POST.get('specialite')).__eq__(''):
                dic['error3'] = 'Field empty'
                empty = True
            if str(request.POST.get('typecours')).__eq__(''):
                dic['error3'] = 'Field empty'
                empty = True
            if str(request.POST.get('langue')).__eq__(''):
                dic['error4'] = 'Field empty'
                empty = True
            if empty:
                dic['code'] = codeprogram
                t = get_template('parametrage/codeprogram/form.html')
                html = t.render(Context(dic))
                return HttpResponse(html)
            else:
                codeprogram.domaine = request.POST.get('domaine')
                codeprogram.mention = request.POST.get('mention')
                codeprogram.specialite = request.POST.get('specialite')
                codeprogram.typecours = request.POST.get('typecours')
                codeprogram.langue = request.POST.get('langue')
                codeprogram.save()
            dic = {'login':True,'code': '', 'user': user,'message':'Le code programme a été modifié avec succès.'}
            t = get_template('parametrage/codeprogram/repmod.html')
            html = t.render(Context(dic))
            return HttpResponse(html)


"""FIN"""