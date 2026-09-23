    def nonzero(self):
        if self.fill_value == 0:
            return (self.sp_index.to_int_index().indices,)
        else:
            return (self.sp_index.to_int_index().indices[self.sp_values != 0],)
