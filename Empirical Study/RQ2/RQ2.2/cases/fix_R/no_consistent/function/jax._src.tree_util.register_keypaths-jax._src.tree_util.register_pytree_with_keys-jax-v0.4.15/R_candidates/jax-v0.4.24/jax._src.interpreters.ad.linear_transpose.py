def linear_transpose(transpose_rule, cotangent, *args, **kwargs):
  return Zero if type(cotangent) is Zero else transpose_rule(cotangent, **kwargs)
