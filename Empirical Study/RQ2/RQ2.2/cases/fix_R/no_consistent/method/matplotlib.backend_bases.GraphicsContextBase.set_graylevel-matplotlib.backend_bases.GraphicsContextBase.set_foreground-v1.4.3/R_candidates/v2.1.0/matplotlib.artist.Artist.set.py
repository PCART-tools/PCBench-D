    def set(self, **kwargs):
        """A property batch setter. Pass *kwargs* to set properties.
        """
        props = OrderedDict(
            sorted(kwargs.items(), reverse=True,
                   key=lambda x: (self._prop_order.get(x[0], 0), x[0])))

        return self.update(props)
