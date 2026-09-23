    def _concat_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class
        """
        attribs = self._get_attributes_dict()
        attribs['name'] = name

        if not isinstance(self, ABCPeriodIndex):
            # reset freq
            attribs['freq'] = None

        if getattr(self, 'tz', None) is not None:
            return _concat._concat_datetimetz(to_concat, name)
        else:
            new_data = np.concatenate([c.asi8 for c in to_concat])
        return self._simple_new(new_data, **attribs)
