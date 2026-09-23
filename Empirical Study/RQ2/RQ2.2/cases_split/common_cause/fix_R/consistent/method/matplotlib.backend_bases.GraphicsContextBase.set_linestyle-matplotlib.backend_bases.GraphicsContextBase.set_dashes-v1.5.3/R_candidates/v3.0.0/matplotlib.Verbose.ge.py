    @cbook.deprecated("2.2", message=_verbose_msg)
    def ge(self, level):
        'return true if self.level is >= level'
        return self.vald[self.level] >= self.vald[level]
