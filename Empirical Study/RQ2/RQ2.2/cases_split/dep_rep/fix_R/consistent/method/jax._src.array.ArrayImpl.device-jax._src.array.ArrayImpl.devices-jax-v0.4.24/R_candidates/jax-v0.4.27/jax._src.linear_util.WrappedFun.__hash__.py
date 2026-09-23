  def __hash__(self):
    return hash((self.f, self.transforms, self.params, self.in_type,
                 self.debug_info))
