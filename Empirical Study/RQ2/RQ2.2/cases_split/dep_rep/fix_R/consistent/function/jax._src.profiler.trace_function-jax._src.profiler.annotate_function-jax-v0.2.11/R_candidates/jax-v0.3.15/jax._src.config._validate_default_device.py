def _validate_default_device(val):
  if val is not None and not isinstance(val, xla_client.Device):
    # TODO(skyewm): this is a workaround for non-PJRT Device types. Remove when
    # all JAX backends use a single C++ device interface.
    if 'Device' in str(type(val)):
      logging.info(
          'Allowing non-`xla_client.Device` default device: %s, type: %s',
          repr(val), type(val))
      return
    raise ValueError('jax.default_device must be passed a Device object (e.g. '
                     f"`jax.devices('cpu')[0]`), got: {repr(val)}")
