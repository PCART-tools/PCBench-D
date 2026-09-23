  def process_primitive(self, primitive, tracers, params):
    if primitive in custom_staging_rules:
      return custom_staging_rules[primitive](self, *tracers, **params)
    return self.default_process_primitive(primitive, tracers, params)
