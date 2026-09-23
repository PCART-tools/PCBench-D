def _string_concat(*strings):
    """
    Lazy variant of string concatenation, needed for translations that are
    constructed from multiple parts.
    """
    warnings.warn(
        'django.utils.translate.string_concat() is deprecated in '
        'favor of django.utils.text.format_lazy().',
        RemovedInDjango21Warning, stacklevel=2)
    return ''.join(str(s) for s in strings)
