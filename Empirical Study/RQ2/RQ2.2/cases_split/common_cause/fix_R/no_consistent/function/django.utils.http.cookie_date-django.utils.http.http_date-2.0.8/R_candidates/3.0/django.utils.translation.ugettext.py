def ugettext(message):
    """
    A legacy compatibility wrapper for Unicode handling on Python 2.
    Alias of gettext() since Django 2.0.
    """
    warnings.warn(
        'django.utils.translation.ugettext() is deprecated in favor of '
        'django.utils.translation.gettext().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return gettext(message)
