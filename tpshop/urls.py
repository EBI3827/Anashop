from django.contrib import admin
from django.urls import path, include,re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from tpshop import settings
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':"path\to\your\static\folder"}),
    path('accounts/', include('allauth.urls')),
    path('',include('product.urls'),name='product'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()