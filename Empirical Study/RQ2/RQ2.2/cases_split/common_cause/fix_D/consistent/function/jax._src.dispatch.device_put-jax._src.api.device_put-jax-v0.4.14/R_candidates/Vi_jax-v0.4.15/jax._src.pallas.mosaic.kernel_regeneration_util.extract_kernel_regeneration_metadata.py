def extract_kernel_regeneration_metadata(op: ir.Operation) -> dict[str, Any]:
  """Extract kernel regeneration metadata from the given Operation.

  This function hides the serialization details from the end user.

  Args:
    op: the tpu custom_call mlir Operation that contains the kernel metadata.

  Returns:
    The decoded metadata in the form of a dict. This corresponds to the dict
    in input to the 'encode' function.
  """
  backend_config = ir.StringAttr(op.opview.backend_config).value
  backend_config_json = json.loads(backend_config)
  kernel_regeneration_metadata = backend_config_json["custom_call_config"][
      "kernel_regeneration_metadata"
  ]
  return json.loads(base64.b64decode(kernel_regeneration_metadata))
