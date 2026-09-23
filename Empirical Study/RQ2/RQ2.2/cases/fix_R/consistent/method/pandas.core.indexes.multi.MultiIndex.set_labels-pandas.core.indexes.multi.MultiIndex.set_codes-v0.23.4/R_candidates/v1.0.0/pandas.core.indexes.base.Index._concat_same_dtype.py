    def _concat_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class.
        """
        # must be overridden in specific classes
        klasses = (
            ABCDatetimeIndex,
            ABCTimedeltaIndex,
            ABCPeriodIndex,
            ExtensionArray,
            ABCIntervalIndex,
        )
        to_concat = [
            x.astype(object) if isinstance(x, klasses) else x for x in to_concat
        ]

        self = to_concat[0]
        attribs = self._get_attributes_dict()
        attribs["name"] = name

        to_concat = [x._values if isinstance(x, Index) else x for x in to_concat]

        return self._shallow_copy_with_infer(np.concatenate(to_concat), **attribs)
