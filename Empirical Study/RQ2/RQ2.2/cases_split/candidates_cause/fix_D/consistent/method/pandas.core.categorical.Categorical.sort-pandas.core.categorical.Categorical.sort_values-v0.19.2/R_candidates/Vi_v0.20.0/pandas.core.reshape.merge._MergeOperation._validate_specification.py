    def _validate_specification(self):
        # Hm, any way to make this logic less complicated??
        if self.on is None and self.left_on is None and self.right_on is None:

            if self.left_index and self.right_index:
                self.left_on, self.right_on = (), ()
            elif self.left_index:
                if self.right_on is None:
                    raise MergeError('Must pass right_on or right_index=True')
            elif self.right_index:
                if self.left_on is None:
                    raise MergeError('Must pass left_on or left_index=True')
            else:
                # use the common columns
                common_cols = self.left.columns.intersection(
                    self.right.columns)
                if len(common_cols) == 0:
                    raise MergeError('No common columns to perform merge on')
                if not common_cols.is_unique:
                    raise MergeError("Data columns not unique: %s"
                                     % repr(common_cols))
                self.left_on = self.right_on = common_cols
        elif self.on is not None:
            if self.left_on is not None or self.right_on is not None:
                raise MergeError('Can only pass argument "on" OR "left_on" '
                                 'and "right_on", not a combination of both.')
            self.left_on = self.right_on = self.on
        elif self.left_on is not None:
            n = len(self.left_on)
            if self.right_index:
                if len(self.left_on) != self.right.index.nlevels:
                    raise ValueError('len(left_on) must equal the number '
                                     'of levels in the index of "right"')
                self.right_on = [None] * n
        elif self.right_on is not None:
            n = len(self.right_on)
            if self.left_index:
                if len(self.right_on) != self.left.index.nlevels:
                    raise ValueError('len(right_on) must equal the number '
                                     'of levels in the index of "left"')
                self.left_on = [None] * n
        if len(self.right_on) != len(self.left_on):
            raise ValueError("len(right_on) must equal len(left_on)")
