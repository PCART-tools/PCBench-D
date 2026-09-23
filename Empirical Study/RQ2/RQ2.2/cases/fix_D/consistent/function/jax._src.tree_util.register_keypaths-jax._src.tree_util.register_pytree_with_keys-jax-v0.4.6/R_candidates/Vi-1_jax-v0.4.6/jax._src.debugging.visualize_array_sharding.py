def visualize_array_sharding(arr, **kwargs):
  """Visualizes an array's sharding."""
  if not config.jax_array:
    raise NotImplementedError("`visualize_array_sharding` not implemented.")
  def _visualize(sharding):
    return visualize_sharding(arr.shape, sharding, **kwargs)
  inspect_array_sharding(arr, callback=_visualize)
