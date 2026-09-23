def host_count(backend: str | xla_client.Client | None = None) -> int:
  warnings.warn(
      "jax.host_count has been renamed to jax.process_count. This alias "
      "will eventually be removed; please update your code.")
  return process_count(backend)
