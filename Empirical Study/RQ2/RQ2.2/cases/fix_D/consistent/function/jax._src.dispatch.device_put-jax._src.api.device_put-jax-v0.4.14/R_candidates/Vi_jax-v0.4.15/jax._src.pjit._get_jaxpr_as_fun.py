@weakref_lru_cache
def _get_jaxpr_as_fun(jaxpr, in_shardings, out_shardings, resource_env,
                      donated_invars, name, keep_unused, inline):
  # The input jaxpr to `_get_jaxpr_as_fun` is under a weakref_lru_cache so
  # returning `core.jaxpr_as_fun(jaxpr)` directly creates a strong reference to
  # the jaxpr defeating the purpose of weakref_lru_cache. So return a function
  # that closes over a weakrefed jaxpr and gets called inside that function.
  # This way there won't be a strong reference to the jaxpr from the output
  # function.
  jaxpr = weakref.ref(jaxpr)
  return lambda *args: core.jaxpr_as_fun(jaxpr())(*args)  # pylint: disable=unnecessary-lambda
