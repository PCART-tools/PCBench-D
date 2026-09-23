    def __init__(self, labels, levels=None, name=None):
        if levels is None:
            if name is None:
                name = getattr(labels, 'name', None)
            try:
                labels, levels = factorize(labels, sort=True)
            except TypeError:
                labels, levels = factorize(labels, sort=False)

        self.labels = labels
        self.levels = levels
        self.name = name
