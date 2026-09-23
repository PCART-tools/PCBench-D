def save_model_params_blob(model, params_file, epoch, opts, best_metric):
    # best_metric=float('-inf')
    log.info("Saving model params...")
    root_xpu_id = opts['distributed']['first_xpu_id']
    device = opts['distributed']['device']
    save_params = [str(param) for param in
                   model.GetParams('{}_{}'.format(device, root_xpu_id))]
    save_computed_params = [str(param) for param in
                            model.GetComputedParams('{}_{}'
                            .format(device, root_xpu_id))]
    save_blobs = {}
    save_blobs['epoch'] = epoch
    save_blobs['best_metric'] = best_metric
    save_blobs['lr'] = \
        workspace.FetchBlob('{}_{}/lr'.format(device, root_xpu_id))
    for param in save_params + save_computed_params:
        scoped_blob_name = str(param)
        unscoped_blob_name = unscope_name(scoped_blob_name)
        if unscoped_blob_name not in save_blobs:
            save_blobs[unscoped_blob_name] = workspace.FetchBlob(
                scoped_blob_name)
            log.debug(
                '{:s} -> {:s}'.format(scoped_blob_name, unscoped_blob_name))
    log.info('to weights file {}'.format(params_file))
    try:
        with open(params_file, 'w') as fwrite:
            pickle.dump(dict(blobs=save_blobs), fwrite, pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        log.error('I/O error({0}): {1}'.format(e.errno, e.strerror))
