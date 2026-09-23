def _primal_tangent_shapes_match(primal, tangent):
  if type(tangent) is not Zero:
    primal_aval = raise_to_shaped(get_aval(primal), weak_type=False)
    tangent_aval = raise_to_shaped(get_aval(tangent), weak_type=False)
    assert core.symbolic_equal_shape(primal_aval.shape, tangent_aval.shape)
    expected_tangent_dtype = core.primal_dtype_to_tangent_dtype(primal_aval.dtype)
    assert expected_tangent_dtype == tangent_aval.dtype, (expected_tangent_dtype, tangent_aval.dtype)
