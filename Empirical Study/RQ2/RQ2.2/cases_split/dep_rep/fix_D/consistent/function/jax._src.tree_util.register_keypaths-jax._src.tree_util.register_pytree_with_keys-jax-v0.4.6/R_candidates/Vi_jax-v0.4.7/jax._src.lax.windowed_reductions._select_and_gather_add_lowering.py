def _select_and_gather_add_lowering(
    ctx: mlir.LoweringRuleContext,
    tangents, operand, *, select_prim,
    window_dimensions, window_strides, padding, base_dilation, window_dilation,
    max_bits=64):
  _, operand_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  dtype = operand_aval.dtype
  etype = mlir.dtype_to_ir_type(dtype)
  nbits = dtypes.finfo(dtype).bits

  assert nbits <= max_bits
  double_word_reduction = nbits * 2 <= max_bits

  const = lambda dtype, x: mlir.ir_constant(np.array(x, dtype=dtype),
                                            canonicalize_types=False)

  def _broadcast_scalar_const(x, aval_out):
    return mlir.broadcast_in_dim(ctx, const(aval_out.dtype, x),
                                 aval_out,
                                 broadcast_dimensions=())

  if double_word_reduction:
    # TODO(b/73062247): XLA doesn't yet implement ReduceWindow on tuples, so
    # we implement a pair-wise ReduceWindow by packing two k-bit values into
    # 2k-bit unsigned integer using bit tricks.
    word_dtype = lax._UINT_DTYPES[nbits]
    double_word_dtype = lax._UINT_DTYPES[nbits * 2]
    word_type = mlir.dtype_to_ir_type(word_dtype)  # type: ignore
    double_word_type = mlir.dtype_to_ir_type(double_word_dtype)  # type: ignore
    # Packs two values into a double_word_type.
    def pack(a, b, ab_aval):
      word_type_ab_aval = ab_aval.update(dtype=word_dtype)
      double_word_type_ab_aval = ab_aval.update(dtype=double_word_dtype)
      a = hlo.BitcastConvertOp(mlir.aval_to_ir_type(word_type_ab_aval), a)
      b = hlo.BitcastConvertOp(mlir.aval_to_ir_type(word_type_ab_aval), b)
      a = hlo.ConvertOp(mlir.aval_to_ir_type(double_word_type_ab_aval), a)
      b = hlo.ConvertOp(mlir.aval_to_ir_type(double_word_type_ab_aval), b)
      a = hlo.ShiftLeftOp(a,
                          _broadcast_scalar_const(nbits, double_word_type_ab_aval))
      return hlo.OrOp(a, b)

    # Unpacks the first element of a double_word_type.
    def fst(t):
      assert not ir.RankedTensorType(t.type).shape
      st = hlo.ShiftRightLogicalOp(t, const(double_word_dtype, nbits))
      return hlo.BitcastConvertOp(
          ir.RankedTensorType.get([], etype),
          hlo.ConvertOp(ir.RankedTensorType.get([], word_type), st)).result

    # Unpacks the second element of a double_word_type.
    def snd(t, t_aval):
      return hlo.BitcastConvertOp(
          mlir.aval_to_ir_type(t_aval.update(dtype=dtype)),
          hlo.ConvertOp(mlir.aval_to_ir_type(t_aval.update(dtype=word_dtype)), t)).result

  else:
    # The double-word trick above only works if we have a sufficiently large
    # type. As an alternative, we can pack two half words into a single word,
    # at the cost of precision.
    # TODO(b/73062247): add support for tuple reductions and remove this case.
    warnings.warn("Using reduced precision for gradient of reduce-window "
                  "min/max operator to work around missing XLA support for "
                  "pair-reductions. This is likely from a second or "
                  "higher derivative of a max-pooling operation.")
    r_nbits = nbits // 2
    # Drop/round the bottom mantissa bits.
    nexp = dtypes.finfo(dtype).nexp
    nmant = r_nbits - nexp - 1

    double_word_dtype = word_dtype = lax._UINT_DTYPES[nbits]
    double_word_type = word_type = mlir.dtype_to_ir_type(word_dtype)  # type: ignore

    # Packs two values into a double_word_type.
    def pack(a, b, ab_aval):
      word_type_ab_aval = ab_aval.update(dtype=word_dtype)
      a = hlo.ReducePrecisionOp(a, exponent_bits=mlir.i32_attr(nexp),
                                mantissa_bits=mlir.i32_attr(nmant))
      b = hlo.ReducePrecisionOp(b, exponent_bits=mlir.i32_attr(nexp),
                                mantissa_bits=mlir.i32_attr(nmant))
      a = hlo.BitcastConvertOp(mlir.aval_to_ir_type(word_type_ab_aval), a)
      b = hlo.BitcastConvertOp(mlir.aval_to_ir_type(word_type_ab_aval), b)
      b = hlo.ShiftRightLogicalOp(
          b, _broadcast_scalar_const(r_nbits, word_type_ab_aval))
      return hlo.OrOp(a, b)

    # Unpacks the first element of a double_word_type.
    def fst(t):
      assert not ir.RankedTensorType(t.type).shape
      st = hlo.AndOp(t, const(word_dtype, ((1 << r_nbits) - 1) << r_nbits))
      return hlo.BitcastConvertOp(ir.RankedTensorType.get([], etype),
                                  st).result

    # Unpacks the second element of a double_word_type.
    def snd(t, t_aval):
      return hlo.BitcastConvertOp(
          mlir.aval_to_ir_type(t_aval.update(dtype=dtype)),
          hlo.ShiftLeftOp(t, _broadcast_scalar_const(r_nbits, t_aval.update(dtype=word_dtype)))
          ).result

  assert select_prim is lax.ge_p or select_prim is lax.le_p, select_prim
  init = -np.inf if select_prim is lax.ge_p else np.inf
  double_word_out_aval = out_aval.update(dtype=double_word_dtype)
  rw = hlo.ReduceWindowOp(
      [mlir.aval_to_ir_type(double_word_out_aval)],
      pack(operand, tangents, operand_aval),
      pack(const(dtype, init), const(dtype, 0), core.ShapedArray((), dtype)),
      mlir.dense_int_elements(window_dimensions),
      window_strides=mlir.dense_int_elements(window_strides),
      base_dilations=mlir.dense_int_elements(base_dilation),
      window_dilations=mlir.dense_int_elements(window_dilation),
      padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                          shape=(len(padding), 2)))
  scalar_type = ir.RankedTensorType.get([], double_word_type)
  reducer = rw.regions[0].blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(reducer):
    x, y = reducer.arguments
    assert select_prim is lax.ge_p or select_prim is lax.le_p
    cmp_op = "GE" if select_prim is lax.ge_p else "LE"
    out = hlo.SelectOp(mlir.compare_hlo(fst(x), fst(y), cmp_op), x, y)
    hlo.ReturnOp(out)
  return [snd(rw.result, double_word_out_aval)]
