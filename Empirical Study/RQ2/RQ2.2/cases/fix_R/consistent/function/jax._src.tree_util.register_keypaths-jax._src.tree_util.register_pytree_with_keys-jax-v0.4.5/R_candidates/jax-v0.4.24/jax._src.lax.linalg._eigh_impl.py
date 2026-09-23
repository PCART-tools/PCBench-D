def _eigh_impl(operand, *, lower, sort_eigenvalues, subset_by_index):
  v, w = dispatch.apply_primitive(
      eigh_p,
      operand,
      lower=lower,
      sort_eigenvalues=sort_eigenvalues,
      subset_by_index=subset_by_index,
  )
  return v, w
