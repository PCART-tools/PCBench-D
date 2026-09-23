@implements(scipy.cluster.vq.vq, lax_description=_no_chkfinite_doc, skip_params=('check_finite',))
def vq(obs, code_book, check_finite=True):
    check_arraylike("scipy.cluster.vq.vq", obs, code_book)
    if obs.ndim != code_book.ndim:
        raise ValueError("Observation and code_book should have the same rank")
    obs, code_book = promote_dtypes_inexact(obs, code_book)
    if obs.ndim == 1:
        obs, code_book = obs[..., None], code_book[..., None]
    if obs.ndim != 2:
        raise ValueError("ndim different than 1 or 2 are not supported")

    # explicitly rank promotion
    dist = vmap(lambda ob: jnp.linalg.norm(ob[None] - code_book, axis=-1))(obs)
    code = jnp.argmin(dist, axis=-1)
    dist_min = vmap(operator.getitem)(dist, code)
    return code, dist_min
