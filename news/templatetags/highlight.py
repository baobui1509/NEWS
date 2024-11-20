from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='highlight')
def highlight(text, keyword):
    if not keyword:
        return text
    highlighted_text = re.sub(
        rf'({re.escape(keyword)})', 
        r'<span class="highlight">\1</span>', 
        text, 
        flags=re.IGNORECASE
    )
    return mark_safe(highlighted_text)

# re.sub(pattern, repl, string, flags=0)