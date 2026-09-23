def _logical_op(np_op, bitwise_op):
  @_wraps(np_op, update_doc=False, module='numpy')
  @partial(jit, inline=True)
  def op(*args):
    zero = lambda x: lax.full_like(x, shape=(), fill_value=0)
    args = (x if dtypes.issubdtype(dtypes.dtype(x), np.bool_) else lax.ne(x, zero(x))
            for x in args)
    return bitwise_op(*_promote_args(np_op.__name__, *args))
  return op
