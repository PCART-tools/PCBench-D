    @final
    def intersection(self, other, sort=False):
        """
        Form the intersection of two Index objects.

        This returns a new Index with elements common to the index and `other`.

        Parameters
        ----------
        other : Index or array-like
        sort : False or None, default False
            Whether to sort the resulting index.

            * False : do not sort the result.
            * None : sort the result, except when `self` and `other` are equal
              or when the values cannot be compared.

        Returns
        -------
        intersection : Index

        Examples
        --------
        >>> idx1 = pd.Index([1, 2, 3, 4])
        >>> idx2 = pd.Index([3, 4, 5, 6])
        >>> idx1.intersection(idx2)
        Int64Index([3, 4], dtype='int64')
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_name = self._convert_can_do_setop(other)

        if self.equals(other):
            if self.has_duplicates:
                return self.unique()._get_reconciled_name_object(other)
            return self._get_reconciled_name_object(other)

        if len(self) == 0 or len(other) == 0:
            # fastpath; we need to be careful about having commutativity

            if self._is_multi or other._is_multi:
                # _convert_can_do_setop ensures that we have both or neither
                # We retain self.levels
                return self[:0].rename(result_name)

            dtype = self._find_common_type_compat(other)
            if is_dtype_equal(self.dtype, dtype):
                # Slicing allows us to retain DTI/TDI.freq, RangeIndex

                # Note: self[:0] vs other[:0] affects
                #  1) which index's `freq` we get in DTI/TDI cases
                #     This may be a historical artifact, i.e. no documented
                #     reason for this choice.
                #  2) The `step` we get in RangeIndex cases
                if len(self) == 0:
                    return self[:0].rename(result_name)
                else:
                    return other[:0].rename(result_name)

            return Index([], dtype=dtype, name=result_name)

        elif not self._should_compare(other):
            # We can infer that the intersection is empty.
            if isinstance(self, ABCMultiIndex):
                return self[:0].rename(result_name)
            return Index([], name=result_name)

        elif not is_dtype_equal(self.dtype, other.dtype):
            dtype = self._find_common_type_compat(other)
            this = self.astype(dtype, copy=False)
            other = other.astype(dtype, copy=False)
            return this.intersection(other, sort=sort)

        result = self._intersection(other, sort=sort)
        return self._wrap_intersection_result(other, result)
