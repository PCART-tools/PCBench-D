    def __call__(self, x, pos=None):
        # docstring inherited
        if len(self.locs) == 0:
            return ''
        else:
            return f'{x:.12}'
