@keep_lazy_text
def unescape_entities(text):
    warnings.warn(
        'django.utils.text.unescape_entities() is deprecated in favor of '
        'html.unescape().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return _entity_re.sub(_replace_entity, str(text))
