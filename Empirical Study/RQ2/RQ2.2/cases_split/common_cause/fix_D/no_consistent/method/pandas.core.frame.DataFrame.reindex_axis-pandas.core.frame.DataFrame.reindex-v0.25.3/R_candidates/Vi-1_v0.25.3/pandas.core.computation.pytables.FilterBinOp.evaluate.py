    def evaluate(self):

        if not self.is_valid:
            raise ValueError("query term is not valid [{slf}]".format(slf=self))

        rhs = self.conform(self.rhs)
        values = [TermValue(v, v, self.kind).value for v in rhs]

        if self.is_in_table:

            # if too many values to create the expression, use a filter instead
            if self.op in ["==", "!="] and len(values) > self._max_selectors:

                filter_op = self.generate_filter_op()
                self.filter = (self.lhs, filter_op, pd.Index(values))

                return self
            return None

        # equality conditions
        if self.op in ["==", "!="]:

            filter_op = self.generate_filter_op()
            self.filter = (self.lhs, filter_op, pd.Index(values))

        else:
            raise TypeError(
                "passing a filterable condition to a non-table "
                "indexer [{slf}]".format(slf=self)
            )

        return self
