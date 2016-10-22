from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import arena_data.views
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', arena_data.views.main, name='main'),
    url(r'^stats/', arena_data.views.stats, name='stats'),
    url(r'^dates/', arena_data.views.dates, name='dates'),
    url(r'^pepe/', hello.views.pepe, name='pepe'),
]
