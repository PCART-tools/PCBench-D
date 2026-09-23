    def write_th(self, s, indent=0, tags=None):
        if (self.fmt.col_space is not None
                and self.fmt.col_space > 0):
            tags = (tags or "")
            tags += 'style="min-width: %s;"' % self.fmt.col_space

        return self._write_cell(s, kind='th', indent=indent, tags=tags)
