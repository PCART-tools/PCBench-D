def random_fold_in(keys, msgs):
  return random_fold_in_p.bind(keys, jnp.asarray(msgs))
