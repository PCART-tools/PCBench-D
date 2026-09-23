    def __init__(self, data=None):
        """
        Create mapping between unique categorical values and integer ids.

        Parameters
        ----------
        data: iterable
              sequence of string values
        """
        self._mapping = OrderedDict()
        self._counter = itertools.count()
        if data is not None:
            self.update(data)
