def _join_field_name(prefix, suffix):
    if prefix and suffix:
        return '{}{}{}'.format(prefix, FIELD_SEPARATOR, suffix)
    elif prefix:
        return prefix
    elif suffix:
        return suffix
    else:
        return ''
