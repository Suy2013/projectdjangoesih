from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import redirect
from projectesih.util.fonctionalite import Action
from projectesih.databasemanager import ManageProfesseur,ManageUser,ManageCours
from professeur.models import Professor, Experience, Formation, CompetenceOrg, CompetenceCom, CompetenceInfo

# Create your views here.
manageProf = ManageProfesseur()
manageUser = ManageUser()
manageCours = ManageCours()


def formprof(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    dic={'login':True,'action': Action.CREER,'user':user}
    if user.type.__eq__("Prof"):
        dic['userprof']=manageProf.getProf(user)
    t = get_template('professeur/formprof.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def listprof(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    list = manageProf.listall()
    dic={'login':True,'action': Action.CREER, 'list': list,'user':user}
    if user.type.__eq__("Prof"):
        dic['userprof']=manageProf.getProf(user)

    t = get_template('professeur/list.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def modprof(request, id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    professor = manageProf.searchById(id)
    dic = {'login':True,'user':user}
    if user.type.__eq__("Prof"):
        dic['userprof']=manageProf.getProf(user)
    dic['professor']=professor
    t = get_template('professeur/mod.html')
    html = t.render(Context(dic))
    return HttpResponse(html)


def controllerprof(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    action = request.POST['action'];
    if action is not None:
        if str(action).__eq__(''):
            return ''
        else:
            if str(action).__eq__(Action.CREER):
                nom = request.POST['nom']
                prenom = request.POST['prenom']
                sexe = request.POST['sexe']
                identite = request.POST['identite']
                telephone = request.POST['telephone']
                email = request.POST['email']
                adresse = request.POST['adresse']
                naissance = request.POST['naissance']
                valid = True
                if nom != None and prenom != None and sexe != None and identite != None and telephone != None and email != None and adresse != None and naissance != None:
                    professor = Professor(nom=nom, prenom=prenom, sexe=sexe, identite=identite, telephone=telephone,
                                          email=email, adresse=adresse, naissance=naissance)
                    dic = {'login':True,'action': Action.CREER, 'professor': professor,'user':user}
                    if user.type.__eq__("Prof"):
                        dic['userprof']=manageProf.getProf(user)
                    if manageProf.isexistmail(email):
                        dic['error6'] = 'Deja existe'
                        valid = False
                    userP=False
                    if 'userprof' in request.POST['userprof']:
                        if not manageUser.iscreateuser(request.POST['userprof']):
                            valid = False
                            dic['error7'] = 'User incorrect'
                    else:
                        userP=True


                    if valid:
                        ide=professor.save()
                        manageUser.createUserProf( request.POST['userprof'],Professor.objects.get(id=ide))

                        message = "L'enregitrement de {} {} est effectue avec succes".format(nom, prenom)
                        t = get_template('professeur/repform.html')
                        dic={'login':True,'message': message,'user':user}
                        if user.type.__eq__("Prof"):
                            dic['userprof']=manageProf.getProf(user)
                        html = t.render(Context(dic))
                        return HttpResponse(html)
                    else:
                        t = get_template('professeur/formprof.html')
                        html = t.render(Context(dic))
                        return HttpResponse(html)


def voircv(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    professor = manageProf.searchById(id)
    formations = manageProf.searchFormation(professor)
    experiences = manageProf.searchExperience(professor)
    competencesorg = manageProf.searchCompetenceOrg(professor)
    competencescom = manageProf.searchCompetenceCom(professor)
    competencesinfo = manageProf.searchCompetenceInfo(professor)
    dic = {'login':True,'imprimmer':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
    if user.type.__eq__("Prof"):
        dic['userprof']=manageProf.getProf(user)
    t = get_template('professeur/readcv.html')
    html = t.render(Context(dic))
    return HttpResponse(html)
def profindex(request):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    dic = {'login':True,'imprimmer':True, 'user':user}
    if user.type.__eq__("Prof"):
        p=manageProf.getProf(user)
        dic['userprof']=p
        professor = manageProf.searchById(p.id)
        formations = manageProf.searchFormation(professor)
        experiences = manageProf.searchExperience(professor)
        competencesorg = manageProf.searchCompetenceOrg(professor)
        competencescom = manageProf.searchCompetenceCom(professor)
        competencesinfo = manageProf.searchCompetenceInfo(professor)
        dic['professor']= professor
        dic['formations']= formations
        dic['experiences']= experiences
        dic['competencesorg']= competencesorg
        dic['competencescom']= competencescom
        dic['competencesinfo']= competencesinfo

    t = get_template('professeur/readcv.html')
    html = t.render(Context(dic))
    return HttpResponse(html)

def listcoursprof(request,id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    dic = {'login':True,'user':user}
    if user.type.__eq__("Prof"):
        p=manageProf.getProf(user)
        dic['userprof']=p
    t = get_template('admin/cours/list.html')
    list = manageCours.listcp(id)
    dic['list']=list
    #return HttpResponse(len(list))
    html = t.render(Context(dic))
    return HttpResponse(html)

def editCV(request, id):
    session = None
    try:
        session = request.session['userid']
    except KeyError:
        pass
    if session==None:
        return redirect("/admin/")
    user = manageUser.searchById(request.session['userid'])
    action = None
    try:
        action = request.POST['action']
    except KeyError:
        pass


    if str(action).__eq__('infoperso'):
        nom = None
        prenom = None
        telephone = None
        email = None
        adresse = None

        try:
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            telephone = request.POST['telephone']
            email = request.POST['email']
            adresse = request.POST['adresse']
        except KeyError:
            pass


        valid = True
        if nom != None and prenom != None and telephone != None and email != None and adresse != None:
            professor =manageProf.searchById(id)
            m = professor.email
            professor.adresse = adresse
            professor.email = email
            professor.nom = nom
            professor.prenom = prenom
            professor.telephone = telephone
            dic = {'login':True,'action': Action.CREER, 'professor': professor,'user':user}
            if user.type.__eq__("Prof"):
                dic['userprof']=manageProf.getProf(user)
            if manageProf.isexistmail(email):
                if m != email:
                    dic['error6'] = 'Deja existe'
                    valid = False
            if valid:
                professor.save()
                message = "L'enregitrement de {} {} est effectue avec succes".format(nom, prenom)
                t = get_template('professeur/repform.html')
                dic={'login':True,'message': message,'user':user}
                if user.type.__eq__("Prof"):
                    dic['userprof']=manageProf.getProf(user)
                html = t.render(Context(dic))
                return HttpResponse(html)
            else:
                t = get_template('professeur/formprof.html')
                html = t.render(Context(dic))
                return HttpResponse(html)



    if str(action).__eq__('exper'):
        de = None
        a = None
        now = None
        fonction = None
        entreprise = None
        try:
            de = request.POST['de']
            if 'a' in request.POST:
                a = request.POST['a']
            if 'now' in request.POST:
                now = request.POST['now']
            fonction = request.POST['fonction']
            entreprise = request.POST['entreprise']
        except KeyError:
            return HttpResponse("OK")
        valid = True
        if a != None and de != None and fonction != None and entreprise != None:
            professor = manageProf.searchById(id)
            experience = Experience(de=de, fonction=fonction, entreprise=entreprise,professor=professor)
            if a:
                experience.a = a
            if now:
                experience.now = now
            experience.save()
            professor = manageProf.searchById(id)
            formations = manageProf.searchFormation(professor)
            experiences = manageProf.searchExperience(professor)
            competencesorg = manageProf.searchCompetenceOrg(professor)
            competencescom = manageProf.searchCompetenceCom(professor)
            competencesinfo = manageProf.searchCompetenceInfo(professor)
            dic = {'login':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
            if user.type.__eq__("Prof"):
                dic['userprof']=manageProf.getProf(user)
            t = get_template('professeur/editercv.html')
            html = t.render(Context(dic))
            # del request.POST['de']
            # del request.POST['a']
            # del request.POST['fonction']
            # del request.POST['entreprise']
            return HttpResponse(html)
        else:
            pass


    if str(action).__eq__('formation'):
        de = None
        a = None
        now = None
        diplome = None
        etablissement = None
        localite = None
        try:
            de = request.POST['de']
            de = request.POST['de']
            if 'a' in request.POST:
                a = request.POST['a']
            if 'now' in request.POST:
                now = request.POST['now']

            diplome = request.POST['diplome']
            etablissement = request.POST['etablissement']
            localite = request.POST['localite']
        except KeyError:
            pass
        valid = True
        if a != None and de != None and diplome != None and etablissement != None:
            professor = manageProf.searchById(id)
            formation = Formation(de=de, diplome=diplome, etablissement=etablissement, localite=localite, professor=professor)
            if a:
                formation.a = a
            if now:
                formation.now = now
            formation.save()
            professor = manageProf.searchById(id)
            formations = manageProf.searchFormation(professor)
            experiences = manageProf.searchExperience(professor)
            competencesorg = manageProf.searchCompetenceOrg(professor)
            competencescom = manageProf.searchCompetenceCom(professor)
            competencesinfo = manageProf.searchCompetenceInfo(professor)
            dic = {'login':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
            if user.type.__eq__("Prof"):
                dic['userprof']=manageProf.getProf(user)
            t = get_template('professeur/editercv.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
        else:
            pass


    if str(action).__eq__('org'):
        organisationel = None
        try:
            organisationel = request.POST['organisationel']
        except KeyError:
            pass
        valid = True
        if organisationel != None:
            professor = manageProf.searchById(id)
            competenceOrg = CompetenceOrg(organisationel=organisationel, professor=professor)
            competenceOrg.save()
            professor = manageProf.searchById(id)
            formations = manageProf.searchFormation(professor)
            experiences = manageProf.searchExperience(professor)
            competencesorg = manageProf.searchCompetenceOrg(professor)
            competencescom = manageProf.searchCompetenceCom(professor)
            competencesinfo = manageProf.searchCompetenceInfo(professor)
            dic = {'login':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
            if user.type.__eq__("Prof"):
                dic['userprof']=manageProf.getProf(user)
            t = get_template('professeur/editercv.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
        else:
            pass



    if str(action).__eq__('commu'):
        communication = None
        try:
            communication = request.POST['communication']
        except KeyError:
            pass
        valid = True
        if communication != None:
            professor = manageProf.searchById(id)
            competenceCom = CompetenceCom(communication=communication, professor=professor)
            competenceCom.save()
            professor = manageProf.searchById(id)
            formations = manageProf.searchFormation(professor)
            experiences = manageProf.searchExperience(professor)
            competencesorg = manageProf.searchCompetenceOrg(professor)
            competencescom = manageProf.searchCompetenceCom(professor)
            competencesinfo = manageProf.searchCompetenceInfo(professor)
            dic = {'login':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
            if user.type.__eq__("Prof"):
                dic['userprof']=manageProf.getProf(user)
            t = get_template('professeur/editercv.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
        else:
            pass


    if str(action).__eq__('informatique'):
        informatique = None
        try:
            informatique = request.POST['informatique']
        except KeyError:
            pass
        valid = True
        if informatique != None:
            professor = manageProf.searchById(id)
            competenceInfo = CompetenceInfo(informatique=informatique, professor=professor)
            competenceInfo.save()
            professor = manageProf.searchById(id)
            formations = manageProf.searchFormation(professor)
            experiences = manageProf.searchExperience(professor)
            competencesorg = manageProf.searchCompetenceOrg(professor)
            competencescom = manageProf.searchCompetenceCom(professor)
            competencesinfo = manageProf.searchCompetenceInfo(professor)
            dic = {'login':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
            if user.type.__eq__("Prof"):
                dic['userprof']=manageProf.getProf(user)
            t = get_template('professeur/editercv.html')
            html = t.render(Context(dic))
            return HttpResponse(html)
        else:
            pass



    professor = manageProf.searchById(id)
    formations = manageProf.searchFormation(professor)
    experiences = manageProf.searchExperience(professor)
    competencesorg = manageProf.searchCompetenceOrg(professor)
    competencescom = manageProf.searchCompetenceCom(professor)
    competencesinfo = manageProf.searchCompetenceInfo(professor)
    dic = {'login':True,'professor': professor, 'formations': formations, 'experiences': experiences, 'competencesorg': competencesorg, 'competencescom': competencescom, 'competencesinfo': competencesinfo,'user':user}
    if user.type.__eq__("Prof"):
        dic['userprof']=manageProf.getProf(user)
    t = get_template('professeur/editercv.html')
    html = t.render(Context(dic))
    return HttpResponse(html)

def delformations(request, id, id1):
    Formation.objects.get(id=id1).delete()
    return redirect("/editcv/{}/".format(id))

def delcompetencesorg(request, id, id1):
    CompetenceOrg.objects.get(id=id1).delete()
    return redirect("/editcv/{}/".format(id))

def delcompetencescom(request, id, id1):
    CompetenceCom.objects.get(id=id1).delete()
    return redirect("/editcv/{}/".format(id))

def delcompetencesinfo(request, id, id1):
    CompetenceInfo.objects.get(id=id1).delete()
    return redirect("/editcv/{}/".format(id))

def delexperiences(request, id, id1):
    Experience.objects.get(id=id1).delete()
    return redirect("/editcv/{}/".format(id))