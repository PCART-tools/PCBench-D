def _gamma_grad(sample, a, *, log_space):
  samples = jnp.reshape(sample, -1)
  alphas = jnp.reshape(a, -1)
  if log_space:
    # d[log(sample)] = d[sample] / sample
    # This requires computing exp(log_sample), which may be zero due to float roundoff.
    # In this case, correct it to smallest representable float.
    samples = lax.exp(samples)
    zero = lax_internal._const(sample, 0)
    tiny = lax.full_like(samples, jnp.finfo(samples.dtype).tiny)
    samples = lax.select(lax.eq(samples, zero), tiny, samples)
    gamma_grad = lambda alpha, sample: lax.random_gamma_grad(alpha, sample) / sample
  else:
    gamma_grad = lax.random_gamma_grad
  if xla_bridge.get_backend().platform == 'cpu':
    grads = lax.map(lambda args: gamma_grad(*args), (alphas, samples))
  else:
    grads = vmap(gamma_grad)(alphas, samples)
  return grads.reshape(np.shape(a))
