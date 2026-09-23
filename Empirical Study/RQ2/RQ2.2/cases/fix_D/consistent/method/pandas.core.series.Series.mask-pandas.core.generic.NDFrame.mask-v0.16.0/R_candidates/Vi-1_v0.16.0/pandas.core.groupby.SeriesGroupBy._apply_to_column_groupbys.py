    def _apply_to_column_groupbys(self, func):
        """ return a pass thru """
        return func(self)
