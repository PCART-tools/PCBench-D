def _get_layouts_from_executable(
    xla_executable, in_layouts, out_layouts, num_ordered_effects
) -> tuple[Sequence[SpecifiedLayout | None], Sequence[SpecifiedLayout | None]]:
  try:
    in_layouts_xla = xla_executable.get_parameter_layouts()
    out_layouts_xla = xla_executable.get_output_layouts()
  except:
    return (None,) * len(in_layouts), (None,) * len(out_layouts)

  if num_ordered_effects > 0:
    in_layouts_xla = in_layouts_xla[num_ordered_effects:]
    out_layouts_xla = out_layouts_xla[num_ordered_effects:]

  new_in_layouts = []
  for x, i in safe_zip(in_layouts_xla, in_layouts):
    x = SpecifiedLayout(x)
    if isinstance(i, SpecifiedLayout):
      if i != x:
        raise AssertionError(
            f"Unexpected XLA layout override: (XLA) {x} != {i} (User sharding)")
      new_in_layouts.append(i)
    else:
      new_in_layouts.append(x)

  new_out_layouts = []
  for x, o in safe_zip(out_layouts_xla, out_layouts):
    x = SpecifiedLayout(x)
    if isinstance(o, SpecifiedLayout):
      if o != x:
        raise AssertionError(
            f"Unexpected XLA layout override: (XLA) {x} != {o} (User sharding)")
      new_out_layouts.append(o)
    else:
      new_out_layouts.append(x)

  assert all(isinstance(i, SpecifiedLayout) for i in new_in_layouts)
  assert all(isinstance(o, SpecifiedLayout) for o in new_out_layouts)
  return new_in_layouts, new_out_layouts  # type: ignore
