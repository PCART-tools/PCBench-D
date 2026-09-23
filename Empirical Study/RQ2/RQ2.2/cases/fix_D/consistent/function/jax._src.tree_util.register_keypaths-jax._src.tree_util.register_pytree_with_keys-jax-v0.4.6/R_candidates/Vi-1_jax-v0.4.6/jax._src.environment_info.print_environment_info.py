def print_environment_info(return_string: bool = False) -> Union[None, str]:
  """Returns a string containing local environment & JAX installation information.

  This is useful information to include when asking a question or filing a bug.

  Args:
    return_string (bool) : if True, return the string rather than printing to stdout.
  """
  # TODO(jakevdp): should we include other info, e.g. jax.config.values?
  python_version = sys.version.replace('\n', ' ')
  with np.printoptions(threshold=4, edgeitems=2):
    devices_short = str(np.array(jax.devices())).replace('\n', '')
  info = textwrap.dedent(f"""\
  jax:    {jax.__version__}
  jaxlib: {lib.version_str}
  numpy:  {np.__version__}
  python: {python_version}
  jax.devices ({jax.device_count()} total, {jax.local_device_count()} local): {devices_short}
  process_count: {jax.process_count()}""")
  nvidia_smi = try_nvidia_smi()
  if nvidia_smi:
    info += "\n\n$ nvidia-smi\n" + nvidia_smi
  if return_string:
    return info
  else:
    return print(info)
