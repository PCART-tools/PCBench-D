def _memory_space_to_tpu_memspace(memory_space: TPUMemorySpace | None
                                  ) -> ir.Attribute:
  if memory_space is None:
    memory_space = VMEM
  return ir.Attribute.parse(f"#tpu.memory_space<{memory_space}>")
