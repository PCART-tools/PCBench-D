    def _box_col_values(self, values, items):
        """ provide boxed values for a column """
        klass = _get_sliced_frame_result_type(values, self)
        return klass(values, index=self.index, name=items, fastpath=True)
