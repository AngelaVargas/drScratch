from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'drScratch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    #url(r'^profile', 'DrScratchApp.views.profileSettings',),
    #url(r'^progressBar', 'app.views.progressBar',),
    #url(r'^admin/upload_progress/$', 'app.views.upload_progress', name="admin-upload-progress"),
    url(r'^login', 'app.views.loginUser',),
    url(r'^logout', 'app.views.logoutUser',),
	url(r'^createUser', 'app.views.createUser',),
    #url(r'^uploadUnregistered', 'app.views.uploadUnregistered',),
    #url(r'^uploadRegistered', 'app.views.uploadRegistered',),
    url(r'^myDashboard', 'app.views.myDashboard',),
    url(r'^myHistoric', 'app.views.myHistoric',),
    url(r'^myProjects', 'app.views.myProjects',),
	url(r'^myRoles', 'app.views.myRoles',),
	url(r'^sendUrlProject', 'app.views.processFormURL',),
	url(r'^exportCsv', 'app.views.exportCsvFile',),
	url(r'drawBlocks', 'app.views.exportCsvFile',),
	url(r'^jsonProject', 'app.views.responseMetricsJSON',),
	url(r'^statistics', 'app.views.showStatisticsDr',),
	url(r'^api/v1/project/(.*)/$', 'app.views.apiProject',),
	url(r'^api/v1/project/set/(.*)/(.*)$', 'app.views.apiSetProject',),
	url(r'ajax', 'app.views.ajaxDogs',),
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirectMain'),
    
]
