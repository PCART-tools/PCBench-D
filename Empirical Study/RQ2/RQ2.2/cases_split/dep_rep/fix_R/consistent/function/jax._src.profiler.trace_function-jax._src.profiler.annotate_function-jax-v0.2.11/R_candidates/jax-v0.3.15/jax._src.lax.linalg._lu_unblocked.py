def _lu_unblocked(a):
  """Unblocked LU decomposition, as a rolled loop."""
  m, n = a.shape
  def body(k, state):
    pivot, perm, a = state
    m_idx = jnp.arange(m)
    n_idx = jnp.arange(n)

    if jnp.issubdtype(a.dtype, jnp.complexfloating):
      t = a[:, k]
      magnitude = jnp.abs(jnp.real(t)) + jnp.abs(jnp.imag(t))
    else:
      magnitude = jnp.abs(a[:, k])
    i = jnp.argmax(jnp.where(m_idx >= k, magnitude, -jnp.inf))
    pivot = pivot.at[k].set(i)
    a = a.at[[k, i],].set(a[[i, k],])
    perm = perm.at[[i, k],].set(perm[[k, i],])

    # a[k+1:, k] /= a[k, k], adapted for loop-invariant shapes
    x = a[k, k]
    a = a.at[:, k].set(jnp.where(m_idx > k, a[:, k] / x, a[:, k]))

    # a[k+1:, k+1:] -= jnp.outer(a[k+1:, k], a[k, k+1:])
    a = a - jnp.where((m_idx[:, None] > k) & (n_idx > k),
                     jnp.outer(a[:, k], a[k, :]), jnp.array(0, dtype=a.dtype))
    return pivot, perm, a

  pivot = jnp.zeros((min(m, n),), dtype=jnp.int32)
  perm = jnp.arange(m, dtype=jnp.int32)
  if m == 0 and n == 0:
    # If the array is empty, the loop body never executes but tracing it to a
    # jaxpr fails because the indexing cannot succeed.
    return (pivot, perm, a)
  return lax.fori_loop(0, min(m, n), body, (pivot, perm, a))
