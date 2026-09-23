@keep_lazy_text
def unescape_entities(text):
    return _entity_re.sub(_replace_entity, str(text))
