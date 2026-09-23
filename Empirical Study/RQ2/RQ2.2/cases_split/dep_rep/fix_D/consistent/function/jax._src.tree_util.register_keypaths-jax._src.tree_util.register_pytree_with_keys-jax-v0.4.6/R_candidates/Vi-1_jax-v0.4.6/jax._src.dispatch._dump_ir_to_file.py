def _dump_ir_to_file(name: str, ir: str):
  id = next(_ir_dump_counter)
  name = f"jax_ir{id}_{_make_string_safe_for_filename(name)}.mlir"
  name = path.Path(FLAGS.jax_dump_ir_to) / name
  name.write_text(ir)
