def _eigh_jvp_rule(primals, tangents, *, lower, sort_eigenvalues):
  # Derivative for eigh in the simplest case of distinct eigenvalues.
  # This is classic nondegenerate perurbation theory, but also see
  # https://people.maths.ox.ac.uk/gilesm/files/NA-08-01.pdf
  # The general solution treating the case of degenerate eigenvalues is
  # considerably more complicated. Ambitious readers may refer to the general
  # methods below or refer to degenerate perturbation theory in physics.
  # https://www.win.tue.nl/analysis/reports/rana06-33.pdf and
  # https://people.orie.cornell.edu/aslewis/publications/99-clarke.pdf
  a, = primals
  a_dot, = tangents

  v, w_real = eigh_p.bind(symmetrize(a), lower=lower,
                          sort_eigenvalues=sort_eigenvalues)

  # for complex numbers we need eigenvalues to be full dtype of v, a:
  w = w_real.astype(a.dtype)
  eye_n = jnp.eye(a.shape[-1], dtype=a.dtype)
  # carefully build reciprocal delta-eigenvalue matrix, avoiding NaNs.
  Fmat = ufuncs.reciprocal(eye_n + w[..., jnp.newaxis, :] - w[..., jnp.newaxis]) - eye_n
  # eigh impl doesn't support batch dims, but future-proof the grad.
  dot = partial(lax.dot if a.ndim == 2 else lax.batch_matmul,
                precision=lax.Precision.HIGHEST)
  vdag_adot_v = dot(dot(_H(v), a_dot), v)
  dv = dot(v, ufuncs.multiply(Fmat, vdag_adot_v))
  dw = ufuncs.real(jnp.diagonal(vdag_adot_v, axis1=-2, axis2=-1))
  return (v, w_real), (dv, dw)
