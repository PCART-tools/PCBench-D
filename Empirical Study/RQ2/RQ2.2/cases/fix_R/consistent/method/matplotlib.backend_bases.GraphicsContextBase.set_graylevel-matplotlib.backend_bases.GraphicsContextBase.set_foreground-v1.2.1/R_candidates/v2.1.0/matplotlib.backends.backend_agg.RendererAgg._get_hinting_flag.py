    def _get_hinting_flag(self):
        if rcParams['text.hinting']:
            return LOAD_FORCE_AUTOHINT
        else:
            return LOAD_NO_HINTING
