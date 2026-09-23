        def __delitem__(self, key):
            _api.warn_deprecated(
                '3.5',
                name=f'modification of the Axes.{self._prop_name}',
                obj_type='property',
                alternative='Artist.remove()')
            if isinstance(key, slice):
                for artist in self[key]:
                    artist.remove()
            else:
                self[key].remove()
