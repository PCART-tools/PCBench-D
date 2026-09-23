def number_format(value, decimal_pos=None, use_l10n=None, force_grouping=False):
    """
    Format a numeric value using localization settings.

    If use_l10n is provided and is not None, it forces the value to
    be localized (or not), overriding the value of settings.USE_L10N.
    """
    if use_l10n or (use_l10n is None and settings.USE_L10N):
        lang = get_language()
    else:
        lang = None
    return numberformat.format(
        value,
        get_format('DECIMAL_SEPARATOR', lang, use_l10n=use_l10n),
        decimal_pos,
        get_format('NUMBER_GROUPING', lang, use_l10n=use_l10n),
        get_format('THOUSAND_SEPARATOR', lang, use_l10n=use_l10n),
        force_grouping=force_grouping
    )
