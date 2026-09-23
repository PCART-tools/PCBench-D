    @staticmethod
    def _validate_steps(steps):
        if not np.iterable(steps):
            raise ValueError('steps argument must be a sequence of numbers '
                             'from 1 to 10')
        steps = np.asarray(steps)
        if np.any(np.diff(steps) <= 0):
            raise ValueError('steps argument must be uniformly increasing')
        if steps[-1] > 10 or steps[0] < 1:
            warnings.warn('Steps argument should be a sequence of numbers\n'
                          'increasing from 1 to 10, inclusive. Behavior with\n'
                          'values outside this range is undefined, and will\n'
                          'raise a ValueError in future versions of mpl.')
        if steps[0] != 1:
            steps = np.hstack((1, steps))
        if steps[-1] != 10:
            steps = np.hstack((steps, 10))
        return steps
