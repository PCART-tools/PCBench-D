    def _concat_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class.
        """
        attribs = self._get_attributes_dict()
        attribs['name'] = name
        # do not pass tz to set because tzlocal cannot be hashed
        if len({str(x.dtype) for x in to_concat}) != 1:
            raise ValueError('to_concat must have the same tz')

        if not is_period_dtype(self):
            # reset freq
            attribs['freq'] = None

        new_data = type(self._values)._concat_same_type(to_concat).asi8
        return self._simple_new(new_data, **attribs)
