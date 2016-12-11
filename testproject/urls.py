from django.conf.urls import include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^testapps', include('testapps.urls', namespace='testapps')),
]
