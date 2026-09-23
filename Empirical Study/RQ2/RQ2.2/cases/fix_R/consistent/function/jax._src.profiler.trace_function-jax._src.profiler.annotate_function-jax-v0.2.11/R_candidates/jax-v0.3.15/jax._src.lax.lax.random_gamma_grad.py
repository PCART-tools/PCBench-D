def random_gamma_grad(a: Array, x: Array) -> Array:
  r"""Elementwise derivative of samples from `Gamma(a, 1)`."""
  return random_gamma_grad_p.bind(a, x)
