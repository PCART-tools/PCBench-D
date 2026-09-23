def io_callback_impl(*args, result_avals, callback: Callable[..., Any],
                     ordered: bool):
  del result_avals, ordered
  return callback(*args)
