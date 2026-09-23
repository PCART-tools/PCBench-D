def linear_transpose2(transpose_rule, cotangent, *args, **kwargs):
  return Zero if type(cotangent) is Zero else transpose_rule(cotangent, *args, **kwargs)
