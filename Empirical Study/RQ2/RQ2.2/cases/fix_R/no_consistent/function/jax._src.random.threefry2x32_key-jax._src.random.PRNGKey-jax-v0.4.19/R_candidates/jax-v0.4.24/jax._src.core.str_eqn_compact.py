def str_eqn_compact(primitive_name: str, params: dict) -> str:
  "Compact equation to string conversion used in HLO metadata."
  kvs = " ".join(f"{k}={v}" for k, v in params.items()
                 if _compact_eqn_should_include(k, v))
  return f"{primitive_name}[{kvs}]" if len(kvs) > 0 else primitive_name
