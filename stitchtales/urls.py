from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap, CategorySitemap, TagSitemap


sitemaps={
    "posts" : PostSitemap,
    "categories" :CategorySitemap,
    "tags" : TagSitemap,

}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.api_urls')), 
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#Custom Erorr Handlers
handler404="blog.views.handler404"
handler500="blog.views.handler500"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)