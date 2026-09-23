def to_locale(language):
    """Turn a language name (en-us) into a locale name (en_US)."""
    language = language.lower()
    parts = language.split('-')
    try:
        country = parts[1]
    except IndexError:
        return language
    else:
        # A language with > 2 characters after the dash only has its first
        # character after the dash capitalized; e.g. sr-latn becomes sr_Latn.
        # A language with 2 characters after the dash has both characters
        # capitalized; e.g. en-us becomes en_US.
        parts[1] = country.title() if len(country) > 2 else country.upper()
    return parts[0] + '_' + '-'.join(parts[1:])
