def host_ids(
    backend: Optional[Union[str, xla_client.Client]] = None
) -> list[int]:
  warnings.warn(
      "jax.host_ids has been deprecated; please use range(jax.process_count()) "
      "instead. jax.host_ids will eventually be removed; please update your "
      "code.")
  return list(range(process_count(backend)))
