@implements(osp_special.kl_div, module="scipy.special")
def kl_div(
    p: ArrayLike,
    q: ArrayLike,
) -> Array:
    p, q = promote_args_inexact("kl_div", p, q)
    zero = _lax_const(p, 0.0)
    both_gt_zero_mask = lax.bitwise_and(lax.gt(p, zero), lax.gt(q, zero))
    one_zero_mask = lax.bitwise_and(lax.eq(p, zero), lax.ge(q, zero))

    safe_p = jnp.where(both_gt_zero_mask, p, 1)
    safe_q = jnp.where(both_gt_zero_mask, q, 1)

    log_val = lax.sub(
        lax.add(
            lax.sub(_xlogx(safe_p), xlogy(safe_p, safe_q)),
            safe_q,
        ),
        safe_p,
    )
    result = jnp.where(
        both_gt_zero_mask, log_val, jnp.where(one_zero_mask, q, np.inf)
    )
    return result
