from django.conf.urls import url
from django.core.urlresolvers import RegexURLPattern

def format_suffix_patterns(urlpatterns, replace=False):
    suffix_pattern = r'\.(?P<format>[a-z]+)$'
    ret = []
    for urlpattern in urlpatterns:
        regex = urlpattern.regex.pattern.rstrip('$') + suffix_pattern
        ret.append(RegexURLPattern(regex, urlpattern.callback, 
            default_args=urlpattern.default_args, name=urlpattern.name))
        if replace == False:
            ret.append(urlpattern)

    return ret
