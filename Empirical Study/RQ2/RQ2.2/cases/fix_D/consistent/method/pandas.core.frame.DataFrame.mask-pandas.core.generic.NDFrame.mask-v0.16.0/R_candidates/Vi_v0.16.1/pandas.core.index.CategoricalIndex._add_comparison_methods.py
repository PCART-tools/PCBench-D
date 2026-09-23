    @classmethod
    def _add_comparison_methods(cls):
        """ add in comparison methods """

        def _make_compare(op):

            def _evaluate_compare(self, other):

                # if we have a Categorical type, then must have the same categories
                if isinstance(other, CategoricalIndex):
                    other = other.values
                elif isinstance(other, Index):
                    other = self._create_categorical(self, other.values, categories=self.categories, ordered=self.ordered)

                if isinstance(other, ABCCategorical):
                    if not (self.values.is_dtype_equal(other) and len(self.values) == len(other)):
                        raise TypeError("categorical index comparisions must have the same categories and ordered attributes")

                return getattr(self.values, op)(other)

            return _evaluate_compare

        cls.__eq__ = _make_compare('__eq__')
        cls.__ne__ = _make_compare('__ne__')
        cls.__lt__ = _make_compare('__lt__')
        cls.__gt__ = _make_compare('__gt__')
        cls.__le__ = _make_compare('__le__')
        cls.__ge__ = _make_compare('__ge__')
