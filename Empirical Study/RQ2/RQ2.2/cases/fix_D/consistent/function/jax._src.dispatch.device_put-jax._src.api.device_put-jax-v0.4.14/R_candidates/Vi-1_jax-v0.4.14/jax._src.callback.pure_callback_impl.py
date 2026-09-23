def pure_callback_impl(*args, result_avals, callback: Callable[..., Any],
                       vectorized: bool):
  del vectorized, result_avals
  return callback(*args)
