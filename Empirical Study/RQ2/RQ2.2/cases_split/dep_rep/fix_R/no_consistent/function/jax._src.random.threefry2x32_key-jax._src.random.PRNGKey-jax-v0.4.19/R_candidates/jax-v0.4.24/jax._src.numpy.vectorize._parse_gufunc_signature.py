def _parse_gufunc_signature(
    signature: str,
) -> tuple[list[CoreDims], list[CoreDims]]:
  """Parse string signatures for a generalized universal function.

  Args:
    signature: generalized universal function signature, e.g.,
      ``(m,n),(n,p)->(m,p)`` for ``jnp.matmul``.

  Returns:
    Input and output core dimensions parsed from the signature.
  """
  if not re.match(_SIGNATURE, signature):
    raise ValueError(
        f'not a valid gufunc signature: {signature}')
  args, retvals = ([tuple(re.findall(_DIMENSION_NAME, arg))
                   for arg in re.findall(_ARGUMENT, arg_list)]
                   for arg_list in signature.split('->'))
  return args, retvals
