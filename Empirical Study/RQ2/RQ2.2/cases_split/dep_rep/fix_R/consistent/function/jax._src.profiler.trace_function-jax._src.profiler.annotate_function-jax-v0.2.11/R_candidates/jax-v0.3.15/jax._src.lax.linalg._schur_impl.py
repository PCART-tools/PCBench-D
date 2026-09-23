def _schur_impl(operand, *, compute_schur_vectors, sort_eig_vals,
                select_callable):
  return xla.apply_primitive(
      schur_p,
      operand,
      compute_schur_vectors=compute_schur_vectors,
      sort_eig_vals=sort_eig_vals,
      select_callable=select_callable)
