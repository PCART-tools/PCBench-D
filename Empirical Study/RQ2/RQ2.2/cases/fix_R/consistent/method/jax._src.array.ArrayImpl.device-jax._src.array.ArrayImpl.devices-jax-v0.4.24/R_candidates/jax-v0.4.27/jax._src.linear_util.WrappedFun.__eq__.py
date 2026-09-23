  def __eq__(self, other):
    return (self.f == other.f and self.transforms == other.transforms and
            self.params == other.params and self.in_type == other.in_type and
            self.debug_info == other.debug_info)
