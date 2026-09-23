def remat_partial_eval_custom_params_updater(*args):
  *_, params_known, params_staged = args
  return params_known, dict(params_staged, differentiated=True)
