from django.contrib.sitemaps import Sitemap
from .models import Post , Category, Tag


class PostSitemap(Sitemap):
    changefreq="weekly"
    priority=0.9

    def items(self):
        return Post.objects.filter(status="published")
    
    def lastmod(self,obj):
        return obj.updated_at
    
class CategorySitemap(Sitemap):
    changefreq="weekly"
    priority=0.7

    def items(self):
        return Category.objects.all()
    
    def location(self,obj):
        return f'category/{obj.slug}/'
    
class TagSitemap(Sitemap):
    changefreq="monthly"
    priority=0.6

    def items(self):
        return Tag.objects.all()
    
    def location(self,obj):
        return f'/tag/{obj.slug}/'