    def cvt_enum(self, value):
        # Using get will call hash(value), which can be expensive
        # for some types (e.g. Fraction). Since self.enum is rarely
        # used, it's usually better to test it first.
        return self.enum.get(value, value) if self.enum else value
