    @_api.deprecated(
        '3.10',
        message=('Since Matplotlib 3.10 indicate_inset_[zoom] returns a single '
                 'InsetIndicator artist with a rectangle property and a connectors '
                 'property.  From 3.12 it will no longer be possible to unpack the '
                 'return value into two elements.'))
    def __getitem__(self, key):
        return [self._rectangle, self.connectors][key]
