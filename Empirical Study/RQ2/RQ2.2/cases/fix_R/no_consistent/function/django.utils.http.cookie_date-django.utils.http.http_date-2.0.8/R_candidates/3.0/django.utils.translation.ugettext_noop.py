def ugettext_noop(message):
    """
    A legacy compatibility wrapper for Unicode handling on Python 2.
    Alias of gettext_noop() since Django 2.0.
    """
    warnings.warn(
        'django.utils.translation.ugettext_noop() is deprecated in favor of '
        'django.utils.translation.gettext_noop().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return gettext_noop(message)
