@util._wraps(np.einsum_path)
def einsum_path(subscripts, *operands, optimize='greedy'):
  # using einsum_call=True here is an internal api for opt_einsum
  return opt_einsum.contract_path(subscripts, *operands, optimize=optimize)
