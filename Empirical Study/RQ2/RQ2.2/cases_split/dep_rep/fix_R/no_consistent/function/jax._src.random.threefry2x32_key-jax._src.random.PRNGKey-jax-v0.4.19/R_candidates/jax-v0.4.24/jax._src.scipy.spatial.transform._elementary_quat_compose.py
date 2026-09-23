@functools.partial(jnp.vectorize, signature=('(m),(m),(),()->(n)'))
def _elementary_quat_compose(angles: jax.Array, axes: jax.Array, intrinsic: bool, degrees: bool) -> jax.Array:
  angles = jnp.where(degrees, jnp.deg2rad(angles), angles)
  result = _make_elementary_quat(axes[0], angles[0])
  for idx in range(1, len(axes)):
    quat = _make_elementary_quat(axes[idx], angles[idx])
    result = jnp.where(intrinsic, _compose_quat(result, quat), _compose_quat(quat, result))
  return result
