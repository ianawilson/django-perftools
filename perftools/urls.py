from django.conf.urls import patterns, url

urlpatterns = patterns('perftools.views',
    url(r'profiling/$', 'profiling', name='profiling'),
)
