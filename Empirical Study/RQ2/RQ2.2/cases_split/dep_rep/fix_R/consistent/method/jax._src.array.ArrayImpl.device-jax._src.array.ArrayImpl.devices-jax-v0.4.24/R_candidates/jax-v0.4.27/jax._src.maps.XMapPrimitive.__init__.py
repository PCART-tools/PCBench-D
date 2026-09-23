  def __init__(self):
    super().__init__('xmap')
    self.def_impl(xmap_impl)
    self.def_custom_bind(self.bind)
