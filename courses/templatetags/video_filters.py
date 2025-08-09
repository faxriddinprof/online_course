# courses/templatetags/video_filters.py
from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Har qanday YouTube linkni embed formatiga aylantiradi.
    Masalan:
    https://youtu.be/abcd1234  -> abcd1234
    https://www.youtube.com/watch?v=abcd1234 -> abcd1234
    """
    if not url:
        return ""
    
    # YouTube video ID ni regex orqali olish
    pattern = r"(?:v=|be/|embed/)([A-Za-z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return url
