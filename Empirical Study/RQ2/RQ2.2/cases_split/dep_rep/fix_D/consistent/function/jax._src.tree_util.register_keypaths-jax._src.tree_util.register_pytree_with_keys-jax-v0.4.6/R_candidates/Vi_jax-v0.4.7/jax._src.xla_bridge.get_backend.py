@lru_cache(maxsize=None)  # don't use util.memoize because there is no X64 dependence.
def get_backend(
    platform: Union[None, str, xla_client.Client] = None
) -> xla_client.Client:
  return _get_backend_uncached(platform)
