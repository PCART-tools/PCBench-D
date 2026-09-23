    def __unicode__(self):
        formatter = self._formatter_func
        summary = str(self.__class__) + '\n'

        n = len(self)
        if n == 0:
            pass
        elif n == 1:
            first = formatter(self[0])
            summary += '[%s]\n' % first
        elif n == 2:
            first = formatter(self[0])
            last = formatter(self[-1])
            summary += '[%s, %s]\n' % (first, last)
        else:
            first = formatter(self[0])
            last = formatter(self[-1])
            summary += '[%s, ..., %s]\n' % (first, last)

        summary += self._format_footer()
        return summary
