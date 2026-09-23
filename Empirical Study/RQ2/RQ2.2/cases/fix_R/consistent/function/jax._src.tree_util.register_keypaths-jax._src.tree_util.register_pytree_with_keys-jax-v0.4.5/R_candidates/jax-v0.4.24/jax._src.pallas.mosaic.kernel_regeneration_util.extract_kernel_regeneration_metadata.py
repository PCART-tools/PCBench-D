def extract_kernel_regeneration_metadata(op: ir.Operation) -> dict[str, Any]:
  """Extract kernel regeneration metadata from the given Operation.

  This function hides the serialization details from the end user.

  Args:
    op: the tpu custom_call mlir Operation that contains the kernel metadata.

  Returns:
    The decoded metadata in the form of a dict. This corresponds to the dict
    in input to the 'encode' function.
  """
  kernel_regeneration_metadata = ir.StringAttr(
      op.attributes["kernel_regeneration_metadata"]
  ).value
  return json.loads(base64.b64decode(kernel_regeneration_metadata))
