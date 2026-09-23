def inspect_sharding_infer_sharding_from_operands(arg_shapes, arg_shardings,
                                                  shape, backend_string):
  del arg_shapes, shape, backend_string
  return arg_shardings[0]
