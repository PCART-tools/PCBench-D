def _to_resource_axes(axes_specs: Sequence[AxisNamePos],
                      axis_resources: Dict[AxisName, Tuple[ResourceAxisName, ...]]):
  """
  Convert in/out_axes parameters ranging over logical dimensions to
  ones that range over resource dimensions.

  Note that values no longer have to be distinct, as multiple resource
  axes can tile a single positional axes. This is why the result is
  an OrderedDict with an implicit major-to-minor ordering.
  """
  return tuple(OrderedDict((resource_axis, pos_axis)
                           for logical_axis, pos_axis in axes.items()
                           for resource_axis in axis_resources[logical_axis])
               for axes in axes_specs)
