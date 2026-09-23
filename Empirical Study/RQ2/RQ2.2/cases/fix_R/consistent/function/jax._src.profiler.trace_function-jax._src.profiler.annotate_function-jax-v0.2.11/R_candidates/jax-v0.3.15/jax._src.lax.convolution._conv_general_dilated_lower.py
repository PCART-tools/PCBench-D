def _conv_general_dilated_lower(
    ctx, lhs, rhs, *, window_strides, padding,
    lhs_dilation, rhs_dilation, dimension_numbers, feature_group_count,
    batch_group_count, precision, preferred_element_type,
    expand_complex_convolutions=False, **unused_kwargs):
  lhs_aval, rhs_aval = ctx.avals_in
  aval_out, = ctx.avals_out
  assert isinstance(dimension_numbers, ConvDimensionNumbers)
  dtype = lhs_aval.dtype
  if expand_complex_convolutions and np.issubdtype(dtype, np.complexfloating):
    if preferred_element_type is not None:
      # Convert complex dtype to types used for real and imaginary parts
      assert np.issubdtype(preferred_element_type, np.complexfloating)
      preferred_element_type = _real_dtype(preferred_element_type)
    complex_conv = mlir.lower_fun(
      partial(
        _complex_mul,
        partial(conv_general_dilated, window_strides=window_strides,
                padding=padding, lhs_dilation=lhs_dilation,
                rhs_dilation=rhs_dilation, dimension_numbers=dimension_numbers,
                feature_group_count=feature_group_count,
                batch_group_count=batch_group_count, precision=precision,
                preferred_element_type=preferred_element_type)),
      multiple_results=False)
    return complex_conv(ctx, lhs, rhs)

  lhs_spec, rhs_spec, out_spec = dimension_numbers
  dnums = mhlo.ConvDimensionNumbers.get(
    input_batch_dimension=lhs_spec[0],
    input_feature_dimension=lhs_spec[1],
    input_spatial_dimensions=list(lhs_spec[2:]),
    kernel_output_feature_dimension=rhs_spec[0],
    kernel_input_feature_dimension=rhs_spec[1],
    kernel_spatial_dimensions=list(rhs_spec[2:]),
    output_batch_dimension=out_spec[0],
    output_feature_dimension=out_spec[1],
    output_spatial_dimensions=list(out_spec[2:]))
  num_spatial_dims = len(rhs_spec) - 2
  window_reversal = mlir.dense_bool_elements([False] * num_spatial_dims)
  if jax._src.lib.mlir_api_version < 24:
    op = mhlo.ConvOp
  else:
    op = mhlo.ConvolutionOp
  return [
      op(mlir.aval_to_ir_type(aval_out),
         lhs,
         rhs,
         dimension_numbers=dnums,
         feature_group_count=mlir.i64_attr(feature_group_count),
         batch_group_count=mlir.i64_attr(batch_group_count),
         window_strides=mlir.dense_int_elements(window_strides),
         padding=mlir.dense_int_elements(padding),
         lhs_dilation=mlir.dense_int_elements(lhs_dilation),
         rhs_dilation=mlir.dense_int_elements(rhs_dilation),
         window_reversal=window_reversal,
         precision_config=lax.precision_attr(precision)).result
  ]
