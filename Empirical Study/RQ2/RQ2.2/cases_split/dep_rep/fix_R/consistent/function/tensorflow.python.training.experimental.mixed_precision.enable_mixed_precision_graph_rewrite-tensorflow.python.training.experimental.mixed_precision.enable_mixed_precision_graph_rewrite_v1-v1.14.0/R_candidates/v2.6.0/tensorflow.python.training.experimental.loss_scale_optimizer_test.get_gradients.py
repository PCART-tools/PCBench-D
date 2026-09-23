def get_gradients(opt, loss, params):
  grads_and_vars = opt.compute_gradients(loss, params)
  grads, _ = zip(*grads_and_vars)
  return grads
