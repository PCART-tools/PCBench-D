def forward_attr(self_, name):
  if name.startswith('def') and type(self_.fun) in _custom_wrapper_types:
    return getattr(self_.fun, name)
  else:
    raise AttributeError
