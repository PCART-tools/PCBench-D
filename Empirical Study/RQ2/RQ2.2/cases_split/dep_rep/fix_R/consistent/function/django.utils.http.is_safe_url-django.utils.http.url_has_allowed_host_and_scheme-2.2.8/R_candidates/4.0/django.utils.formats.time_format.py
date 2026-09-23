def time_format(value, format=None, use_l10n=None):
    """
    Format a datetime.time object using a localizable format.

    If use_l10n is provided and is not None, it forces the value to
    be localized (or not), overriding the value of settings.USE_L10N.
    """
    return dateformat.time_format(value, get_format(format or 'TIME_FORMAT', use_l10n=use_l10n))
