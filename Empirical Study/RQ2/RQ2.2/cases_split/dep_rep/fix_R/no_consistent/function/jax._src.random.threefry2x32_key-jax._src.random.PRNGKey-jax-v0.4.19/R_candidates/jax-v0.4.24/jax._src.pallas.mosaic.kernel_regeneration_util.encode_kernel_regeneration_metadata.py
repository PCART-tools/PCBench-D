def encode_kernel_regeneration_metadata(
    metadata: dict[str, Any]
) -> dict[str, bytes]:
  """Serializes the given kernel regeneration metadata.

  This function hides the serialization details from the end user.

  Args:
    metadata: dictionary with user-defined data to be serialized in the backend
      config.

  Returns:
    A dict that can be directly passed to pallas_call as a 'mosaic_params'
    argument.

  Raises:
    TypeError: when the input metadata is not serializable in json format.
  """
  serialized_metadata = bytes(json.dumps(metadata), encoding="utf-8")
  return dict(kernel_regeneration_metadata=serialized_metadata)
