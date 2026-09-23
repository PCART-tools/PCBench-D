def _pjit_explicit_sharding(in_shardings, out_shardings, device,
                            backend) -> bool:
  in_shardings_flat, _ = tree_flatten(in_shardings)
  out_shardings_flat, _ = tree_flatten(out_shardings)
  return (device is not None or
          backend is not None or
          any(not is_unspecified(i) for i in in_shardings_flat) or
          any(not is_unspecified(i) for i in out_shardings_flat))
