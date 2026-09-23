def _select_and_gather_add_lowering(
    ctx, tangents, operand, *, select_prim,
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

  def _broadcast(x, dims):
    return mhlo.BroadcastOp(x, mlir.dense_int_elements(dims))

  if double_word_reduction:
    # TODO(b/73062247): XLA doesn't yet implement ReduceWindow on tuples, so
    # we implement a pair-wise ReduceWindow by packing two k-bit values into
    # 2k-bit unsigned integer using bit tricks.
    word_dtype = lax._UINT_DTYPES[nbits]
    double_word_dtype = lax._UINT_DTYPES[nbits * 2]
    word_type = mlir.dtype_to_ir_type(word_dtype)
    double_word_type = mlir.dtype_to_ir_type(double_word_dtype)

    # Packs two values into a tuple.
    def pack(a, b):
      a_dims = ir.RankedTensorType(a.type).shape
      b_dims = ir.RankedTensorType(b.type).shape
      a = mhlo.BitcastConvertOp(ir.RankedTensorType.get(a_dims, word_type), a)
      b = mhlo.BitcastConvertOp(ir.RankedTensorType.get(b_dims, word_type), b)
      a = mhlo.ConvertOp(ir.RankedTensorType.get(a_dims, double_word_type), a)
      b = mhlo.ConvertOp(ir.RankedTensorType.get(b_dims, double_word_type), b)
      a = mhlo.ShiftLeftOp(a,
                           _broadcast(const(double_word_dtype, nbits), a_dims))
      return mhlo.OrOp(a, b)

    # Unpacks the first element of a tuple.
    def fst(t):
      dims = ir.RankedTensorType(t.type).shape
      st = mhlo.ShiftRightLogicalOp(t, const(double_word_dtype, nbits))
      return mhlo.BitcastConvertOp(
          ir.RankedTensorType.get(dims, etype),
          mhlo.ConvertOp(ir.RankedTensorType.get(dims, word_type), st)).result

    # Unpacks the second element of a tuple.
    def snd(t):
      dims = ir.RankedTensorType(t.type).shape
      return mhlo.BitcastConvertOp(
          ir.RankedTensorType.get(dims, etype),
          mhlo.ConvertOp(ir.RankedTensorType.get(dims, word_type), t)).result

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
    double_word_type = word_type = mlir.dtype_to_ir_type(word_dtype)

    # Packs two values into a tuple.
    def pack(a, b):
      a_dims = ir.RankedTensorType(a.type).shape
      b_dims = ir.RankedTensorType(b.type).shape
      a = mhlo.ReducePrecisionOp(a, exponent_bits=mlir.i32_attr(nexp),
                                  mantissa_bits=mlir.i32_attr(nmant))
      b = mhlo.ReducePrecisionOp(b, exponent_bits=mlir.i32_attr(nexp),
                                  mantissa_bits=mlir.i32_attr(nmant))
      a = mhlo.BitcastConvertOp(ir.RankedTensorType.get(a_dims, word_type), a)
      b = mhlo.BitcastConvertOp(ir.RankedTensorType.get(b_dims, word_type), b)
      b = mhlo.ShiftRightLogicalOp(
          b, _broadcast(const(word_dtype, r_nbits), b_dims))
      return mhlo.OrOp(a, b)

    # Unpacks the first element of a tuple.
    def fst(t):
      st = mhlo.AndOp(t, const(word_dtype, ((1 << r_nbits) - 1) << r_nbits))
      return mhlo.BitcastConvertOp(ir.RankedTensorType.get([], etype),
                                   st).result

    # Unpacks the second element of a tuple.
    def snd(t):
      dims = ir.RankedTensorType(t.type).shape
      return mhlo.BitcastConvertOp(
          ir.RankedTensorType.get(dims, etype),
          mhlo.ShiftLeftOp(t, _broadcast(const(word_dtype, r_nbits), dims))
          ).result

  assert select_prim is lax.ge_p or select_prim is lax.le_p, select_prim
  init = -np.inf if select_prim is lax.ge_p else np.inf
  rw = mhlo.ReduceWindowOp(
      [ir.RankedTensorType.get(out_aval.shape, double_word_type)],
      pack(operand, tangents),
      pack(const(dtype, init), const(dtype, 0)),
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
    which = "GE" if select_prim is lax.ge_p else "LE"
    out = mhlo.SelectOp(mlir.compare_mhlo(fst(x), fst(y), which), x, y)
    mhlo.ReturnOp(out)
  return [snd(rw.result)]
