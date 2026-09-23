def device_put(x, device=None):
  from jax._src import api
  return api.device_put(x, device)
