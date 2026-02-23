from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.simple_tag
def get_meta_description(post):
    """Generate meta description from post"""
    if post.meta_description:
        return post.meta_description
    #Fallback on excerpt or cotent
    if post.excerpt:
        return strip_tags(post.excerpt)[:160]
    return strip_tags(post.content)[:160]

@register.simple_tag
def get_og_image(post):
    """Get open graph image URL"""
    if post.cover_image:
        return post.cover_image.url
    return '/static/images/default-og-image.jpg' #Fallback image