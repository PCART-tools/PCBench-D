    def _repr_footer(self):
        levheader = 'Levels (%d): ' % len(self.levels)
        # TODO: should max_line_width respect a setting?
        levstring = np.array_repr(self.levels, max_line_width=60)
        indent = ' ' * (levstring.find('[') + len(levheader) + 1)
        lines = levstring.split('\n')
        levstring = '\n'.join([lines[0]] +
                              [indent + x.lstrip() for x in lines[1:]])

        namestr = "Name: %s, " % self.name if self.name is not None else ""
        return u('%s\n%sLength: %d' % (levheader + levstring, namestr,
                                       len(self)))
