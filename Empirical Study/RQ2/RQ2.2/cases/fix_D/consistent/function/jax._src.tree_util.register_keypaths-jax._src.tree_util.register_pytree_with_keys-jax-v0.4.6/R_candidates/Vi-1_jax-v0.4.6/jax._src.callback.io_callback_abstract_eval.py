@io_callback_p.def_effectful_abstract_eval
def io_callback_abstract_eval(*avals, callback: Callable[..., Any],
                              result_avals, ordered: bool):
  del avals, callback
  effect = _OrderedIOEffect if ordered else _IOEffect
  return result_avals, {effect}
