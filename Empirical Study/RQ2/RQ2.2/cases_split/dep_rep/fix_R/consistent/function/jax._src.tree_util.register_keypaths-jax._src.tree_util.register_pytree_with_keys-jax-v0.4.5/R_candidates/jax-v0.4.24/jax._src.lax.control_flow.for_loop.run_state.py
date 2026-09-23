def run_state(f, init_state):
  @functools.wraps(f)
  def wrapped_body(_, *args):
    return f(*args)
  return for_loop(1, wrapped_body, init_state)
