    def get_width_from_char_name(self, name):
        """Get the width of the character from a type1 character name."""
        return self._metrics_by_name[name].width
