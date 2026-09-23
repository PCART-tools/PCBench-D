    def merge_used_characters(self, other):
        for stat_key, (realpath, charset) in six.iteritems(other):
            used_characters = self.file.used_characters.setdefault(
                stat_key, (realpath, set()))
            used_characters[1].update(charset)
