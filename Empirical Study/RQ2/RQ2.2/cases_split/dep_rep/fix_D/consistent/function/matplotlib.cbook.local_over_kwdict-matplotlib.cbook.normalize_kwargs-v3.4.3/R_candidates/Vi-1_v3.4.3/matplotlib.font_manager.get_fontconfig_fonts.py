def get_fontconfig_fonts(fontext='ttf'):
    """List font filenames known to `fc-list` having the given extension."""
    fontext = ['.' + ext for ext in get_fontext_synonyms(fontext)]
    return [fname for fname in _call_fc_list()
            if Path(fname).suffix.lower() in fontext]
