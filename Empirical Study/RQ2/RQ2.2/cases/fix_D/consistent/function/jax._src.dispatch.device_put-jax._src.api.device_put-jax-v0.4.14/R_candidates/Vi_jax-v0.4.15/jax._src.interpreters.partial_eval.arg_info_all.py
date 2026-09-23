def arg_info_all(dbg: DebugInfo) -> list[tuple[str, KeyPath]] | None:
  ba = None if dbg.in_tree is None else sig_info(dbg)
  if ba is None: return None
  return [(name, key_path) for name, dummy_arg in ba.arguments.items()
          for key_path, _ in generate_key_paths(dummy_arg)]
