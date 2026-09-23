  def __repr__(self):
    def transform_to_str(x):
      i, (gen, args) = x
      return f"{i}   : {fun_name(gen)}   {fun_name(args)}"
    transformation_stack = map(transform_to_str, enumerate(self.transforms))
    return "Wrapped function:\n" + '\n'.join(transformation_stack) + '\nCore: ' + fun_name(self.f) + '\n'
