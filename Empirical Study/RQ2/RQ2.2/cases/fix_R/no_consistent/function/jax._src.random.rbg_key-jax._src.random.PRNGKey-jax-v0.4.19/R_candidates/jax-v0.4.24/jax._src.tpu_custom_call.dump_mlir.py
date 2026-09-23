def dump_mlir(module: ir.Module, name: str):
  """A helper function to dump mosaic mlir module"""
  try:
    should_dump = FLAGS["xla_mosaic_dump_to"].value
  except KeyError:
    return
  if should_dump == "sponge":
    outdir = os.environ.get("TEST_UNDECLARED_OUTPUTS_DIR", None)
    if outdir:
      path = os.path.join(outdir, f"{time.time_ns()}-mosaic-dump-{name}.txt")
      with open(path, "w") as f:
        f.write(str(module))
