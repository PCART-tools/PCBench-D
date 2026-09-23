@pure_callback_p.def_abstract_eval
def pure_callback_abstract_eval(*avals, callback: Callable[..., Any],
                                result_avals, vectorized: bool):
  del avals, callback, vectorized
  return result_avals
