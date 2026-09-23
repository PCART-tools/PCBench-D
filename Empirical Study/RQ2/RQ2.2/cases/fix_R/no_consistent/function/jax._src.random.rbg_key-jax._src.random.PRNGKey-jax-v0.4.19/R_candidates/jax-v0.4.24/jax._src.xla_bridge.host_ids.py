def host_ids(
    backend: str | xla_client.Client | None = None
) -> list[int]:
  warnings.warn(
      "jax.host_ids has been deprecated; please use range(jax.process_count()) "
      "instead. jax.host_ids will eventually be removed; please update your "
      "code.")
  return list(range(process_count(backend)))
