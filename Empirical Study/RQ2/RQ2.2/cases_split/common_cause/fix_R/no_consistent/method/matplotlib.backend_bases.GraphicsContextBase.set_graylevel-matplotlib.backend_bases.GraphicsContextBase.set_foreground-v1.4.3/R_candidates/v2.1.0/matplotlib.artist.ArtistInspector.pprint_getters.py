    def pprint_getters(self):
        """
        Return the getters and actual values as list of strings.
        """

        lines = []
        for name, val in sorted(six.iteritems(self.properties())):
            if getattr(val, 'shape', ()) != () and len(val) > 6:
                s = str(val[:6]) + '...'
            else:
                s = str(val)
            s = s.replace('\n', ' ')
            if len(s) > 50:
                s = s[:50] + '...'
            name = self.aliased_name(name)
            lines.append('    %s = %s' % (name, s))
        return lines
