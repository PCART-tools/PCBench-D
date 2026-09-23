def _resolve_axis_resources_and_shardings_arg(
    in_shardings, out_shardings, in_axis_resources, out_axis_resources):
  if not _is_unspecified(in_shardings) and not _is_unspecified(in_axis_resources):
    raise ValueError(
        'Setting both in_shardings and in_axis_resources is not '
        'allowed. in_axis_resources is deprecated. Please use in_shardings.')
  if not _is_unspecified(out_shardings) and not _is_unspecified(out_axis_resources):
    raise ValueError(
        'Setting both out_shardings and out_axis_resources is not '
        'allowed. out_axis_resources is deprecated. Please use out_shardings.')

  if not _is_unspecified(in_axis_resources):
    final_in_shardings = in_axis_resources
  else:
    final_in_shardings = in_shardings

  if not _is_unspecified(out_axis_resources):
    final_out_shardings = out_axis_resources
  else:
    final_out_shardings = out_shardings
  return final_in_shardings, final_out_shardings
