from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include,re_path
from django.conf.urls.static import static
from product.views import handler404
from django.contrib import admin
from api.views import TestView
from tpshop import settings



handler404 = handler404
# handler500 = myapp.views.handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':"path\to\your\static\folder"}),
    path('accounts/', include('allauth.urls')),
    path('',include('product.urls'),name='product'),
    path('cart/',include('cart.urls'),name='cart'),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls')),
    path('profile/', include('userprofile.urls')),
    path('api/',TestView.as_view(),name='api'),
    path('captcha/', include('captcha.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()