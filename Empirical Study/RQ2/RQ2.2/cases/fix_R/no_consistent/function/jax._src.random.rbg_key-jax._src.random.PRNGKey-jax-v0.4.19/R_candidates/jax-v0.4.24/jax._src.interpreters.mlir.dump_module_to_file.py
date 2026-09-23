def dump_module_to_file(module: ir.Module, stage_name: str) -> str | None:
  """Dumps the `module` IR to a file.

  Dumps the module if JAX_DUMP_IR_TO is defined.

  Args:
    module: The module to dump
    stage_name: A name to distinguish different stages of a module, will be
      appended to the `module.name`.

  Returns:
    The name of the file containing the dump if JAX_DUMP_IR_TO is defined and
    the module was dumped, `None` otherwise.
  """
  out_dir_name = _JAX_DUMP_IR_TO.value
  if not out_dir_name:
    return None
  if out_dir_name == "sponge":
    out_dir_name = os.environ.get("TEST_UNDECLARED_OUTPUTS_DIR", "")
    if not out_dir_name:
      raise ValueError("JAX_DUMP_IR_TO='sponge' but "
                       "TEST_UNDECLARED_OUTPUTS_DIR is not defined")

  id = next(_ir_dump_counter)
  sym_name = module.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  name = f"jax_ir{id}_{_make_string_safe_for_filename(module_name)}_{stage_name}.mlir"

  out_dir = path.Path(out_dir_name)
  out_dir.mkdir(parents=True, exist_ok=True)
  full_path = out_dir / name
  full_path.write_text(module_to_string(module))
  return name
