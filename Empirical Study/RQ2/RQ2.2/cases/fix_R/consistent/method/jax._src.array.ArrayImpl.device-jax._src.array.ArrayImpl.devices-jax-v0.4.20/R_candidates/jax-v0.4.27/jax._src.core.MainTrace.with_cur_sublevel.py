  def with_cur_sublevel(self):
    return self.trace_type(self, cur_sublevel(), **self.payload)
