def _resolve_wsc_args(axis_resources, shardings):
  if not _is_unspecified(axis_resources) and not _is_unspecified(shardings):
    raise ValueError(
        'Setting both axis_resources and shardings is not '
        'allowed. axis_resources is deprecated. Please use shardings.')
  if _is_unspecified(axis_resources) and _is_unspecified(shardings):
    raise ValueError(
        'Not specifying shardings to `with_sharding_constraint` is not allowed. '
        'Please specify the shardings argument with a concrete sharding. Note '
        'that axis_resources is deprecated, so use the shardings argument.')

  if not _is_unspecified(axis_resources):
    final_shardings = axis_resources
  else:
    final_shardings = shardings
  return final_shardings
