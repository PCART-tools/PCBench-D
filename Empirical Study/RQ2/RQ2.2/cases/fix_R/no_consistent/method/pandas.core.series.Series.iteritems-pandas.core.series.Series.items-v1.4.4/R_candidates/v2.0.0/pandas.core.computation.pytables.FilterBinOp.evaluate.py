    def evaluate(self):
        if not self.is_valid:
            raise ValueError(f"query term is not valid [{self}]")

        rhs = self.conform(self.rhs)
        values = list(rhs)

        if self.is_in_table:
            # if too many values to create the expression, use a filter instead
            if self.op in ["==", "!="] and len(values) > self._max_selectors:
                filter_op = self.generate_filter_op()
                self.filter = (self.lhs, filter_op, Index(values))

                return self
            return None

        # equality conditions
        if self.op in ["==", "!="]:
            filter_op = self.generate_filter_op()
            self.filter = (self.lhs, filter_op, Index(values))

        else:
            raise TypeError(
                f"passing a filterable condition to a non-table indexer [{self}]"
            )

        return self
