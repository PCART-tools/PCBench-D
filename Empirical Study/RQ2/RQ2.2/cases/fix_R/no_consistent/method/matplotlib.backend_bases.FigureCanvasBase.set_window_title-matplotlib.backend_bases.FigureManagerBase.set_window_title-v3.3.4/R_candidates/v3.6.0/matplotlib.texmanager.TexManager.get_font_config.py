    @_api.deprecated("3.6")
    def get_font_config(self):
        preamble, font_cmd = self._get_font_preamble_and_command()
        # Add a hash of the latex preamble to fontconfig so that the
        # correct png is selected for strings rendered with same font and dpi
        # even if the latex preamble changes within the session
        preambles = preamble + font_cmd + self.get_custom_preamble()
        return hashlib.md5(preambles.encode('utf-8')).hexdigest()
