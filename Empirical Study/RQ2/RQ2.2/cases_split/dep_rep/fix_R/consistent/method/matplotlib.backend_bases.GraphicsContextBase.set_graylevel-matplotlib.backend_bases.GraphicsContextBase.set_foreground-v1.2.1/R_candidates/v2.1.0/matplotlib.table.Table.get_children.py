    def get_children(self):
        'Return the Artists contained by the table'
        return list(six.itervalues(self._cells))
