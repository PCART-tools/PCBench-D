    def evaluate(self):

        if not self.is_valid:
            raise ValueError("query term is not valid [{slf}]"
                             .format(slf=self))

        # convert values if we are in the table
        if not self.is_in_table:
            return None

        rhs = self.conform(self.rhs)
        values = [self.convert_value(v) for v in rhs]

        # equality conditions
        if self.op in ['==', '!=']:

            # too many values to create the expression?
            if len(values) <= self._max_selectors:
                vs = [self.generate(v) for v in values]
                self.condition = "({cond})".format(cond=' | '.join(vs))

            # use a filter after reading
            else:
                return None
        else:
            self.condition = self.generate(values[0])

        return self
