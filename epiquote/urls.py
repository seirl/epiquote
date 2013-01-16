from django.conf.urls import patterns, include, url
from django.contrib import admin
from quotes import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.last_quotes),
    url(r'^last$', views.last_quotes),
    url(r'^last/(\d+)$', views.last_quotes),
    url(r'^random$', views.random_quotes),
    url(r'^all$', views.all_quotes),
    url(r'^search$', views.search_quotes),
    url(r'^admin/', include(admin.site.urls)),
)
