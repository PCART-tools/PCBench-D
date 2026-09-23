    @classmethod
    def _add_comparison_methods(cls):
        """ add in comparison methods """

        def _make_compare(op):
            opname = "__{op}__".format(op=op.__name__)

            def _evaluate_compare(self, other):

                # if we have a Categorical type, then must have the same
                # categories
                if isinstance(other, CategoricalIndex):
                    other = other._values
                elif isinstance(other, Index):
                    other = self._create_categorical(other._values, dtype=self.dtype)

                if isinstance(other, (ABCCategorical, np.ndarray, ABCSeries)):
                    if len(self.values) != len(other):
                        raise ValueError("Lengths must match to compare")

                if isinstance(other, ABCCategorical):
                    if not self.values.is_dtype_equal(other):
                        raise TypeError(
                            "categorical index comparisons must "
                            "have the same categories and ordered "
                            "attributes"
                        )

                result = op(self.values, other)
                if isinstance(result, ABCSeries):
                    # Dispatch to pd.Categorical returned NotImplemented
                    # and we got a Series back; down-cast to ndarray
                    result = result.values
                return result

            return compat.set_function_name(_evaluate_compare, opname, cls)

        cls.__eq__ = _make_compare(operator.eq)
        cls.__ne__ = _make_compare(operator.ne)
        cls.__lt__ = _make_compare(operator.lt)
        cls.__gt__ = _make_compare(operator.gt)
        cls.__le__ = _make_compare(operator.le)
        cls.__ge__ = _make_compare(operator.ge)
