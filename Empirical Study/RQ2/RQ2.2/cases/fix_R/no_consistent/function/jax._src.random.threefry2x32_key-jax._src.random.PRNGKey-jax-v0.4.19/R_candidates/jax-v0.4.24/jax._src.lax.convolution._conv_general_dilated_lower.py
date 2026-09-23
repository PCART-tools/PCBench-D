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
  dnums = hlo.ConvDimensionNumbers.get(
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
  if len(padding) == 0:
    padding = np.zeros((0, 2), dtype=np.int64)
  window_reversal = mlir.dense_bool_array([False] * num_spatial_dims)
  if (not core.is_constant_shape(window_strides) or
      not core.is_constant_shape(lhs_dilation) or
      not core.is_constant_shape(rhs_dilation) or
      not core.is_constant_dim(feature_group_count) or
      not core.is_constant_dim(batch_group_count)):
    # TODO(https://github.com/openxla/stablehlo/issues/1268)
    raise NotImplementedError("Convolutions with non-static strides, dilation, feature_group_count, or batch_group_count")
  if all(core.is_constant_shape(p) for p in padding):
    return [
        hlo.convolution(
          mlir.aval_to_ir_type(aval_out),
          lhs,
          rhs,
          dimension_numbers=dnums,
          feature_group_count=mlir.i64_attr(feature_group_count),
          batch_group_count=mlir.i64_attr(batch_group_count),
          window_strides=mlir.dense_int_array_v6(window_strides),
          padding=mlir.dense_int_elements(padding),
          lhs_dilation=mlir.dense_int_array_v6(lhs_dilation),
          rhs_dilation=mlir.dense_int_array_v6(rhs_dilation),
          window_reversal=window_reversal,
          precision_config=lax.precision_attr(precision))
    ]
  else:
    # d_padding will be an array i32[N, 2] with pad_lo and pad_hi for each
    # spatial dimension.
    int2d = mlir.aval_to_ir_type(core.ShapedArray((1, 2), np.int32))
    def prep_one_pad(pad_lo_hi: tuple[core.DimSize, core.DimSize]):
      pad1 = mlir.eval_dynamic_shape_as_tensor(ctx, pad_lo_hi)  # i32[2]
      return hlo.ReshapeOp(int2d, pad1)
    d_padding = hlo.ConcatenateOp(list(map(prep_one_pad, padding)),
                                  mlir.i64_attr(0))
    return [
        hlo.dynamic_conv(
          mlir.aval_to_ir_type(aval_out),
          lhs,
          rhs,
          d_padding,
          dimension_numbers=dnums,
          feature_group_count=mlir.i64_attr(feature_group_count),
          batch_group_count=mlir.i64_attr(batch_group_count),
          window_strides=mlir.dense_int_array_v6(window_strides),
          lhs_dilation=mlir.dense_int_array_v6(lhs_dilation),
          rhs_dilation=mlir.dense_int_array_v6(rhs_dilation),
          window_reversal=window_reversal,
          precision_config=lax.precision_attr(precision))
    ]
