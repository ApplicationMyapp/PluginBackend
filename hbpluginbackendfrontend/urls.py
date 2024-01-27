from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',admin.site.urls),
    path('shopify/',include('shopify.urls')),
    path('shiprocket/',include('shiprocket.urls')),
    path('hotellogix/',include('hotellogix.urls')),
    path('JV/',include('consolidate_hotelogix.urls')),
    path('xml/',include('consolidationsXML.urls')),
    path('tally/',include('TallyExportXML.urls')),
    path('canaraspring/',include('canaraSpring.urls')),
    
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


  
