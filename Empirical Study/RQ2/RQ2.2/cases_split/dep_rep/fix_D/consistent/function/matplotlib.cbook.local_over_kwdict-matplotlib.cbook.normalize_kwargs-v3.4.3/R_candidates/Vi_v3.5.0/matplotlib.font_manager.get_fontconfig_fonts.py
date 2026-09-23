@_api.deprecated("3.5")
def get_fontconfig_fonts(fontext='ttf'):
    """List font filenames known to `fc-list` having the given extension."""
    fontext = ['.' + ext for ext in get_fontext_synonyms(fontext)]
    return [str(path) for path in _get_fontconfig_fonts()
            if path.suffix.lower() in fontext]
