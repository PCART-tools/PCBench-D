    @staticmethod
    def _select_native_charmap(font):
        # Select the native charmap. (we can't directly identify it but it's
        # typically an Adobe charmap).
        for charmap_code in [
                1094992451,  # ADOBE_CUSTOM.
                1094995778,  # ADOBE_STANDARD.
        ]:
            try:
                font.select_charmap(charmap_code)
            except (ValueError, RuntimeError):
                pass
            else:
                break
        else:
            _log.warning("No supported encoding in font (%s).", font.fname)
