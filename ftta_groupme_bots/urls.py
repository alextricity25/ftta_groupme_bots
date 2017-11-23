from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import data.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', data.views.index, name='index'),
    url(r'^db', data.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pick_a_song/', data.views.pick_a_song, name='pick_a_song'),
    url(r'^memory_verses/', data.views.memory_verses, name='memory_verses')
]
