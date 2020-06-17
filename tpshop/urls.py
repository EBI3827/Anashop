from django.contrib import admin
from django.urls import path, include,re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from tpshop import settings
from .views import home
from api.views import TestView
from product.views import handler404


handler404 = handler404
# handler500 = myapp.views.handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':"path\to\your\static\folder"}),
    path('accounts/', include('allauth.urls')),
    path('',include('product.urls'),name='product'),
    path('cart/',include('cart.urls'),name='cart'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',TestView.as_view(),name='api'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()