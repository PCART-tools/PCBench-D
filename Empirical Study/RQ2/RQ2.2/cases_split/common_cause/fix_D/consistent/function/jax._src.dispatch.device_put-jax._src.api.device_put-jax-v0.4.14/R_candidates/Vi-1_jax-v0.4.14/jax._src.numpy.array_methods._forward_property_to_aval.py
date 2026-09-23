def _forward_property_to_aval(name):
  @property
  def prop(self):
    return getattr(self.aval, name).fget(self)
  return prop
