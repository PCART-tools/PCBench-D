def get_array_mapping(
    axis_resources: Union[ParsedPartitionSpec, _AUTOAxisResource, _UnspecifiedValue]
) -> pxla.ArrayMappingOrAutoOrUnspecified:
  # TODO(yashkatariya): Use `TypeGuard` on `is_auto` when it is supported.
  # Don't use `is_auto` here to satisfy pytype and mypy.
  if isinstance(axis_resources, (_AUTOAxisResource, _UnspecifiedValue)):
    return axis_resources
  return OrderedDict((axis, i)
                     for i, axes in enumerate(axis_resources)
                     if axes is not None for axis in axes)
