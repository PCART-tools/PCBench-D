def ungettext(singular, plural, number):
    """
    A legacy compatibility wrapper for Unicode handling on Python 2.
    Alias of ngettext() since Django 2.0.
    """
    warnings.warn(
        'django.utils.translation.ungettext() is deprecated in favor of '
        'django.utils.translation.ngettext().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return ngettext(singular, plural, number)
