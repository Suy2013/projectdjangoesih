from django.conf.urls import patterns, include, url
from django.contrib import admin
from projectesih.views import home
from projectesih.views import help
from projectesih.views import current_datetime
from parametrage.views import listetablissement
from parametrage.views import formetablissement, modetablissement, deletablissement
from parametrage.views import controlleretablissement
from parametrage.views import controllercodeprogram
from parametrage.views import controllercodecours
from parametrage.views import formcodeprogram
from parametrage.views import formcodecours
from parametrage.views import listcodeprogram,modcodecours, delcodecours
from parametrage.views import listcodecours,modcodeprogram, delcodeprogram
from admin.views import home
from admin.views import userform, coursform, coursobjectif, coursdescription, coursplan, coursressource,coursevaluation, courslist
from admin.views import userlist
from admin.views import controlleruser,affectprof,detailscours
from admin.views import logout,deluser
from admin.views import usermodform
from professeur.views import formprof, listprof, controllerprof, modprof, editCV,voircv,profindex, \
    listcoursprof,delcompetencesorg, delcompetencescom, delformations, delcompetencesinfo, delexperiences
admin.autodiscover()
urlpatterns = patterns('',
	url(r'^help/$', help),
	url(r'^now/$', current_datetime),
    #url(r'^admin/', include(admin.site.urls)),
    #lien de liste des etablissements
    url(r'^parametrage/etablissement/list/$', listetablissement),
    url(r'^parametrage/etablissement/form/$', formetablissement),
    url(r'^parametrage/etablissement/change/(\d+)/$', modetablissement),
    url(r'^parametrage/etablissement/delete/(\d+)/$', deletablissement),
    url(r'^parametrage/etablissement/controlleretablissement/$', controlleretablissement),
    url(r'^parametrage/codeprogram/form/',formcodeprogram),
    url(r'^parametrage/codeprogram/list/$', listcodeprogram),
    url(r'^parametrage/codeprogram/change/(\d+)/$', modcodeprogram),
    url(r'^parametrage/codeprogram/delete/(\d+)/$', delcodeprogram),
    url(r'^parametrage/codecours/change/(\d+)/$', modcodecours),
    url(r'^parametrage/codecours/delete/(\d+)/$', delcodecours),
    url(r'^parametrage/codeprogram/controllercodeprogram/$', controllercodeprogram),
    url(r'^parametrage/codecours/form/',formcodecours),
    url(r'^parametrage/codecours/list/$', listcodecours),
    url(r'^parametrage/codecours/controllercodecours/$', controllercodecours),
    url(r'^admin/$',home),
    url(r'^$',home),
    url(r'^admin/user/form/$',userform),
    url(r'^admin/user/list/$',userlist),
    url(r'^admin/user/controlleruser/$',controlleruser),
    url(r'^logout/$',logout),
    url(r'^admin/user/change/(\d+)/$',usermodform),
     url(r'^admin/user/delete/(\d+)/$',deluser),
    url(r'^admin/cours/form/$',coursform),
    url(r'^admin/cours/$',courslist),
    url(r'^admin/cours/objectif/(\d+)/$',coursobjectif),
    url(r'^admin/cours/description/(\d+)/$',coursdescription),
    url(r'^admin/cours/plan/(\d+)/$',coursplan),
    url(r'^admin/cours/ressource/(\d+)/$',coursressource),
    url(r'^admin/cours/evaluation/(\d+)/$',coursevaluation),
    url(r'^admin/cours/affectation/(\d+)/$',affectprof),
    url(r'^admin/cours/details/(\d+)/$',detailscours),
    url(r'^admin/professeurs/',listprof),
    url(r'^viewcv/(\d+)/$',voircv),
    url(r'^cours/(\d+)/$',listcoursprof),
    url(r'^profform/',formprof),
    url(r'^profindex/',profindex),
    url(r'^profcontroller/',controllerprof),
    url(r'^profchange/(\d+)/$',modprof),
    url(r'^editcv/(\d+)/$',editCV),
    url(r'^delcompetencesorg/(\d+)/(\d+)/',delcompetencesorg),
    url(r'^delcompetencescom/(\d+)/(\d+)/',delcompetencescom),
    url(r'^delformations/(\d+)/(\d+)/',delformations),
    url(r'^delcompetencesinfo/(\d+)/(\d+)/',delcompetencesinfo),
    url(r'^delexperiences/(\d+)/(\d+)/',delexperiences),
    url(r'^objectifcours/(\d+)/$',coursobjectif),
    url(r'^descriptioncours/(\d+)/$',coursdescription),
    url(r'^plancours/(\d+)/$',coursplan),
    url(r'^ressourcecours/(\d+)/$',coursressource),
    url(r'^evaluationcours/(\d+)/$',coursevaluation),
    url(r'^affectationcours/(\d+)/$',affectprof),
    url(r'^detailscours/(\d+)/$',detailscours),
    #url(r'^admin/user/delete/(\d+)/$',usermodform),
)