def save_model_params(is_checkpoint, model, checkpoint_path, epoch, opts, best_metric):
    # best_metric=float('-inf')
    if checkpoint_path is None:
        return None

    try:
        save_model_params_blob(
            model, checkpoint_path, epoch, opts, best_metric
        )
    except Exception as e:
        log.warning('Exception from save_model_params {}'.format(str(e)))
    return checkpoint_path
