def ungettext_lazy(singular, plural, number=None):
    """
    A legacy compatibility wrapper for Unicode handling on Python 2.
    An alias of ungettext_lazy() since Django 2.0.
    """
    warnings.warn(
        'django.utils.translation.ungettext_lazy() is deprecated in favor of '
        'django.utils.translation.ngettext_lazy().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return ngettext_lazy(singular, plural, number)
