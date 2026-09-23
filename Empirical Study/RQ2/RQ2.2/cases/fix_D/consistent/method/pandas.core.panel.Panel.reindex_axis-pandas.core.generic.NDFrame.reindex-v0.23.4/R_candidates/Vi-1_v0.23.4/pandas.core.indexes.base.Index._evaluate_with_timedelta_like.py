    def _evaluate_with_timedelta_like(self, other, op):
        # Timedelta knows how to operate with np.array, so dispatch to that
        # operation and then wrap the results
        other = Timedelta(other)
        values = self.values

        with np.errstate(all='ignore'):
            result = op(values, other)

        attrs = self._get_attributes_dict()
        attrs = self._maybe_update_attributes(attrs)
        if op == divmod:
            return Index(result[0], **attrs), Index(result[1], **attrs)
        return Index(result, **attrs)
