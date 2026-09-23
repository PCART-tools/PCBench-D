    def track_characters(self, font, s):
        """Keeps track of which characters are required from
        each font."""
        realpath, stat_key = get_realpath_and_stat(font.fname)
        used_characters = self.used_characters.setdefault(
            stat_key, (realpath, set()))
        used_characters[1].update([ord(x) for x in s])
