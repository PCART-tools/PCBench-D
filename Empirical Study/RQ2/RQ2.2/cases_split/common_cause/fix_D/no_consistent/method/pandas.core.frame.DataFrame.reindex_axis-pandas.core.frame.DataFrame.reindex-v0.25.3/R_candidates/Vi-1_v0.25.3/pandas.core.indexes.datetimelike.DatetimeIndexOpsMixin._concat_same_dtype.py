    def _concat_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class.
        """
        attribs = self._get_attributes_dict()
        attribs["name"] = name
        # do not pass tz to set because tzlocal cannot be hashed
        if len({str(x.dtype) for x in to_concat}) != 1:
            raise ValueError("to_concat must have the same tz")

        new_data = type(self._values)._concat_same_type(to_concat).asi8

        # GH 3232: If the concat result is evenly spaced, we can retain the
        # original frequency
        is_diff_evenly_spaced = len(unique_deltas(new_data)) == 1
        if not is_period_dtype(self) and not is_diff_evenly_spaced:
            # reset freq
            attribs["freq"] = None

        return self._simple_new(new_data, **attribs)
