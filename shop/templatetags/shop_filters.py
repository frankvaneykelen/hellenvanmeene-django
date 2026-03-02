from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlparse
import calendar
import markdown

register = template.Library()


@register.filter(is_safe=True)
def markdownify(text):
    """Render a Markdown string as safe HTML."""
    if not text:
        return ""
    return mark_safe(markdown.markdown(text, extensions=["nl2br", "fenced_code", "tables"]))


@register.filter
def shop_name(url):
    """Extract a human-readable shop name from a URL.
    e.g. 'https://www.bol.com/...' → 'Bol.com'
         'https://amazon.com/...'  → 'Amazon.com'
    """
    if not url:
        return ""
    try:
        host = urlparse(url).hostname or ""
        # Strip leading 'www.'
        if host.startswith("www."):
            host = host[4:]
        # Capitalise the first segment (e.g. 'bol' → 'Bol')
        parts = host.split(".", 1)
        parts[0] = parts[0].capitalize()
        return ".".join(parts)
    except Exception:
        return url


@register.filter
def month_name(month_int):
    """Convert an integer month (1–12) to an abbreviated month name, e.g. 2 → 'Feb'."""
    try:
        return calendar.month_abbr[int(month_int)]
    except (TypeError, ValueError, IndexError):
        return month_int
