def _check_resources_mismatch(in_axis_resources_flat, is_gda):
  if not is_gda and _is_from_gda(in_axis_resources_flat):
    raise ValueError('For a non-GDA input, the corresponding resource in '
                     'in_axis_resources cannot be `pjit.FROM_GDA`.')
