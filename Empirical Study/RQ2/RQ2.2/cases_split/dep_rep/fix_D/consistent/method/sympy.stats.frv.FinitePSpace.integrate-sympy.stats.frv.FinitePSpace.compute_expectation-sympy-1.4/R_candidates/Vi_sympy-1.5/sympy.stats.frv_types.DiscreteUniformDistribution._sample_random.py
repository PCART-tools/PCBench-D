    def _sample_random(self, size):
        x = Symbol('x')
        return ArrayComprehensionMap(lambda: self.args[random.randint(0, len(self.args)-1)], (x, 0, size)).doit()
