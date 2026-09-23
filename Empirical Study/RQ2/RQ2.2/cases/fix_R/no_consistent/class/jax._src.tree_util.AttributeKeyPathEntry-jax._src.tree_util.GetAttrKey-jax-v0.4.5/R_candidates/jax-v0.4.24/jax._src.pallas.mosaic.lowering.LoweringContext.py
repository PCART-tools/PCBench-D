@dataclasses.dataclass
class LoweringContext:
  ir_context: ir.Context
  grid_indices: Sequence[ir.Value] | None
  block_shapes: list[tuple[int | pl_core.Mapped, ...]]
  name_stack: source_info_util.NameStack
  mesh_context: MeshContext | None
  replace = dataclasses.replace
  traceback_caches: mlir.TracebackCaches
