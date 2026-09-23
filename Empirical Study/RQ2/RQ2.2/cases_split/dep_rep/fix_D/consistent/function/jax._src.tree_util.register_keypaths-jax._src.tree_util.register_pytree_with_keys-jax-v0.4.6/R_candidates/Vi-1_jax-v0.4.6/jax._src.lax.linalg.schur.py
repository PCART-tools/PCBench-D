@_warn_on_positional_kwargs
def schur(x: ArrayLike, *,
          compute_schur_vectors: bool = True,
          sort_eig_vals: bool = False,
          select_callable: Optional[Callable[..., Any]] = None) -> Tuple[Array, Array]:
  return schur_p.bind(
      x,
      compute_schur_vectors=compute_schur_vectors,
      sort_eig_vals=sort_eig_vals,
      select_callable=select_callable)
