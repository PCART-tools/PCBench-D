def get_hinting_flag():
    mapping = {
        'default': LOAD_DEFAULT,
        'no_autohint': LOAD_NO_AUTOHINT,
        'force_autohint': LOAD_FORCE_AUTOHINT,
        'no_hinting': LOAD_NO_HINTING,
        True: LOAD_FORCE_AUTOHINT,
        False: LOAD_NO_HINTING,
        'either': LOAD_DEFAULT,
        'native': LOAD_NO_AUTOHINT,
        'auto': LOAD_FORCE_AUTOHINT,
        'none': LOAD_NO_HINTING,
    }
    return mapping[mpl.rcParams['text.hinting']]
