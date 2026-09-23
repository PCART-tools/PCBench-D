    def _cmp_method(self, other, op):
        """
        Wrapper used to dispatch comparison operations.
        """
        if self.is_(other):
            # fastpath
            if op in {operator.eq, operator.le, operator.ge}:
                arr = np.ones(len(self), dtype=bool)
                if self._can_hold_na and not isinstance(self, ABCMultiIndex):
                    # TODO: should set MultiIndex._can_hold_na = False?
                    arr[self.isna()] = False
                return arr
            elif op is operator.ne:
                arr = np.zeros(len(self), dtype=bool)
                if self._can_hold_na and not isinstance(self, ABCMultiIndex):
                    arr[self.isna()] = True
                return arr

        if isinstance(other, (np.ndarray, Index, ABCSeries, ExtensionArray)) and len(
            self
        ) != len(other):
            raise ValueError("Lengths must match to compare")

        if not isinstance(other, ABCMultiIndex):
            other = extract_array(other, extract_numpy=True)
        else:
            other = np.asarray(other)

        if is_object_dtype(self.dtype) and isinstance(other, ExtensionArray):
            # e.g. PeriodArray, Categorical
            with np.errstate(all="ignore"):
                result = op(self._values, other)

        elif isinstance(self._values, ExtensionArray):
            result = op(self._values, other)

        elif is_object_dtype(self.dtype) and not isinstance(self, ABCMultiIndex):
            # don't pass MultiIndex
            with np.errstate(all="ignore"):
                result = ops.comp_method_OBJECT_ARRAY(op, self._values, other)

        else:
            with np.errstate(all="ignore"):
                result = ops.comparison_op(self._values, other, op)

        return result
