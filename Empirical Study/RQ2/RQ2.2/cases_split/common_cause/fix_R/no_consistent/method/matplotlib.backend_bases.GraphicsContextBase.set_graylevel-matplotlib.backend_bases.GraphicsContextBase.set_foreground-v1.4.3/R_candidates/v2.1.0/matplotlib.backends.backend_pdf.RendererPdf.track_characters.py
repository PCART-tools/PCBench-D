    def track_characters(self, font, s):
        """Keeps track of which characters are required from
        each font."""
        if isinstance(font, six.string_types):
            fname = font
        else:
            fname = font.fname
        realpath, stat_key = get_realpath_and_stat(fname)
        used_characters = self.file.used_characters.setdefault(
            stat_key, (realpath, set()))
        used_characters[1].update([ord(x) for x in s])
