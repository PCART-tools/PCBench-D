@_warn_on_positional_kwargs
def schur(x, *,
          compute_schur_vectors=True,
          sort_eig_vals=False,
          select_callable=None):
  return schur_p.bind(
      x,
      compute_schur_vectors=compute_schur_vectors,
      sort_eig_vals=sort_eig_vals,
      select_callable=select_callable)
