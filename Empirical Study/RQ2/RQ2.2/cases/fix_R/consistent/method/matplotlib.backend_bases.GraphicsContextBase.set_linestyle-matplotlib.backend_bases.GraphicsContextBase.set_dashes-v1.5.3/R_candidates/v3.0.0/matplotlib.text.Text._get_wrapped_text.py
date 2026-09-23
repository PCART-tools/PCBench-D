    def _get_wrapped_text(self):
        """
        Return a copy of the text with new lines added, so that
        the text is wrapped relative to the parent figure.
        """
        # Not fit to handle breaking up latex syntax correctly, so
        # ignore latex for now.
        if self.get_usetex():
            return self.get_text()

        # Build the line incrementally, for a more accurate measure of length
        line_width = self._get_wrap_line_width()
        wrapped_str = ""
        line = ""

        for word in self.get_text().split(' '):
            # New lines in the user's test need to force a split, so that it's
            # not using the longest current line width in the line being built
            sub_words = word.split('\n')
            for i in range(len(sub_words)):
                current_width = self._get_rendered_text_width(
                    line + ' ' + sub_words[i])

                # Split long lines, and each newline found in the current word
                if current_width > line_width or i > 0:
                    wrapped_str += line + '\n'
                    line = ""

                if line == "":
                    line = sub_words[i]
                else:
                    line += ' ' + sub_words[i]

        return wrapped_str + line
