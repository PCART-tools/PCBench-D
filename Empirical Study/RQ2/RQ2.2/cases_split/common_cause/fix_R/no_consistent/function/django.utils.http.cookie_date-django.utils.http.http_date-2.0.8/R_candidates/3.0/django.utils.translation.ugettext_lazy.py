def ugettext_lazy(message):
    """
    A legacy compatibility wrapper for Unicode handling on Python 2. Has been
    Alias of gettext_lazy since Django 2.0.
    """
    warnings.warn(
        'django.utils.translation.ugettext_lazy() is deprecated in favor of '
        'django.utils.translation.gettext_lazy().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return gettext_lazy(message)
