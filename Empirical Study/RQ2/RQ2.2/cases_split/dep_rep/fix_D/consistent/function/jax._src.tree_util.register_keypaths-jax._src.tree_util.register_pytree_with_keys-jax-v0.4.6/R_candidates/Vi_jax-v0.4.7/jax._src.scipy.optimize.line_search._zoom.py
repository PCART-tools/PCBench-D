def _zoom(restricted_func_and_grad, wolfe_one, wolfe_two, a_lo, phi_lo,
          dphi_lo, a_hi, phi_hi, dphi_hi, g_0, pass_through):
  """
  Implementation of zoom. Algorithm 3.6 from Wright and Nocedal, 'Numerical
  Optimization', 1999, pg. 59-61. Tries cubic, quadratic, and bisection methods
  of zooming.
  """
  state = _ZoomState(
      done=False,
      failed=False,
      j=0,
      a_lo=a_lo,
      phi_lo=phi_lo,
      dphi_lo=dphi_lo,
      a_hi=a_hi,
      phi_hi=phi_hi,
      dphi_hi=dphi_hi,
      a_rec=(a_lo + a_hi) / 2.,
      phi_rec=(phi_lo + phi_hi) / 2.,
      a_star=1.,
      phi_star=phi_lo,
      dphi_star=dphi_lo,
      g_star=g_0,
      nfev=0,
      ngev=0,
  )
  delta1 = 0.2
  delta2 = 0.1

  def body(state):
    # Body of zoom algorithm. We use boolean arithmetic to avoid using jax.cond
    # so that it works on GPU/TPU.
    dalpha = (state.a_hi - state.a_lo)
    a = jnp.minimum(state.a_hi, state.a_lo)
    b = jnp.maximum(state.a_hi, state.a_lo)
    cchk = delta1 * dalpha
    qchk = delta2 * dalpha

    # This will cause the line search to stop, and since the Wolfe conditions
    # are not satisfied the minimization should stop too.
    threshold = jnp.where((jnp.finfo(dalpha).bits < 64), 1e-5, 1e-10)
    state = state._replace(failed=state.failed | (dalpha <= threshold))

    # Cubmin is sometimes nan, though in this case the bounds check will fail.
    a_j_cubic = _cubicmin(state.a_lo, state.phi_lo, state.dphi_lo, state.a_hi,
                          state.phi_hi, state.a_rec, state.phi_rec)
    use_cubic = (state.j > 0) & (a_j_cubic > a + cchk) & (a_j_cubic < b - cchk)
    a_j_quad = _quadmin(state.a_lo, state.phi_lo, state.dphi_lo, state.a_hi, state.phi_hi)
    use_quad = (~use_cubic) & (a_j_quad > a + qchk) & (a_j_quad < b - qchk)
    a_j_bisection = (state.a_lo + state.a_hi) / 2.
    use_bisection = (~use_cubic) & (~use_quad)

    a_j = jnp.where(use_cubic, a_j_cubic, state.a_rec)
    a_j = jnp.where(use_quad, a_j_quad, a_j)
    a_j = jnp.where(use_bisection, a_j_bisection, a_j)

    # TODO(jakevdp): should we use some sort of fixed-point approach here instead?
    phi_j, dphi_j, g_j = restricted_func_and_grad(a_j)
    phi_j = phi_j.astype(state.phi_lo.dtype)
    dphi_j = dphi_j.astype(state.dphi_lo.dtype)
    g_j = g_j.astype(state.g_star.dtype)
    state = state._replace(nfev=state.nfev + 1,
                           ngev=state.ngev + 1)

    hi_to_j = wolfe_one(a_j, phi_j) | (phi_j >= state.phi_lo)
    star_to_j = wolfe_two(dphi_j) & (~hi_to_j)
    hi_to_lo = (dphi_j * (state.a_hi - state.a_lo) >= 0.) & (~hi_to_j) & (~star_to_j)
    lo_to_j = (~hi_to_j) & (~star_to_j)

    state = state._replace(
        **_binary_replace(
            hi_to_j,
            state._asdict(),
            dict(
                a_hi=a_j,
                phi_hi=phi_j,
                dphi_hi=dphi_j,
                a_rec=state.a_hi,
                phi_rec=state.phi_hi,
            ),
        ),
    )

    # for termination
    state = state._replace(
        done=star_to_j | state.done,
        **_binary_replace(
            star_to_j,
            state._asdict(),
            dict(
                a_star=a_j,
                phi_star=phi_j,
                dphi_star=dphi_j,
                g_star=g_j,
            )
        ),
    )
    state = state._replace(
        **_binary_replace(
            hi_to_lo,
            state._asdict(),
            dict(
                a_hi=state.a_lo,
                phi_hi=state.phi_lo,
                dphi_hi=state.dphi_lo,
                a_rec=state.a_hi,
                phi_rec=state.phi_hi,
            ),
        ),
    )
    state = state._replace(
        **_binary_replace(
            lo_to_j,
            state._asdict(),
            dict(
                a_lo=a_j,
                phi_lo=phi_j,
                dphi_lo=dphi_j,
                a_rec=state.a_lo,
                phi_rec=state.phi_lo,
            ),
        ),
    )
    state = state._replace(j=state.j + 1)
    # Choose higher cutoff for maxiter than Scipy as Jax takes longer to find
    # the same value - possibly floating point issues?
    state = state._replace(failed= state.failed | (state.j >= 30))
    return state

  state = lax.while_loop(lambda state: (~state.done) & (~pass_through) & (~state.failed),
                         body,
                         state)

  return state
