from django.template.defaulttags import register

@register.filter
def index(dictionary, key):
    return dictionary.get(key, '')
