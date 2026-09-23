def _serialize_ir(m: ir.Module) -> bytes:
  output = io.BytesIO()
  m.operation.write_bytecode(file=output)
  return output.getvalue()
