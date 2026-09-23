def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    warnings.warn(
        'force_text() is deprecated in favor of force_str().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return force_str(s, encoding, strings_only, errors)
