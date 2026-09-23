def initialize_master_xpu_model_params(model, weights_file, opts, reset_epoch):
    log.info("Initializing model params from file: {}".format(weights_file))
    with open(weights_file, 'r') as fopen:
        blobs = pickle.load(fopen)
    if 'blobs' in blobs:
        blobs = blobs['blobs']

    start_epoch = 0
    best_metric = float('-inf')
    if 'epoch' in blobs:
        log.info('epoch {} is found in model file'.format(blobs['epoch']))
        if not reset_epoch:
            start_epoch = blobs['epoch']
        else:
            log.info('Reset epoch')
    else:
        log.info('no epoch is found in model file')
    lr = opts['model_param']['base_learning_rate']
    if 'lr' in blobs:
        lr = blobs['lr']
    if 'best_metric' in blobs and not reset_epoch:
        best_metric = blobs['best_metric']

    if model is not None:
        log.info('initialize model parameters using weights file: {}'.format(
            weights_file
        ))
        ws_blobs = workspace.Blobs()
        unscoped_blob_names = OrderedDict()
        for blob in model.GetAllParams():
            unscoped_blob_names[unscope_name(str(blob))] = True
        root_xpu_id = opts['distributed']['first_xpu_id']
        device = opts['distributed']['device']
        caffe2_pb2_DEVICE =\
            caffe2_pb2.CUDA if opts['distributed']['device'] == 'gpu'\
            else caffe2_pb2.CPU
        with core.NameScope('{}_{}'.format(device, root_xpu_id)):
            with core.DeviceScope(core.DeviceOption(caffe2_pb2_DEVICE, 0)):
                for unscoped_blob_name in unscoped_blob_names.keys():
                    scoped_blob_name = scoped_name(unscoped_blob_name)
                    if unscoped_blob_name not in blobs:
                        log.info('{:s} not found'.format(unscoped_blob_name))
                        continue
                    log.info(
                        '{:s} loaded from weights file into: {:s}'.format(
                            unscoped_blob_name, scoped_blob_name
                        )
                    )
                    if scoped_blob_name in ws_blobs:
                        ws_blob = workspace.FetchBlob(scoped_blob_name)
                        if not ws_blob.shape == blobs[unscoped_blob_name].shape:
                            log.info(
                                ('Workspace blob {} with shape {} does '
                                    'not match weights file shape {}').format(
                                            unscoped_blob_name, ws_blob.shape,
                                            blobs[unscoped_blob_name].shape)
                            )
                        else:
                            workspace.FeedBlob(
                                scoped_blob_name,
                                blobs[unscoped_blob_name].astype(
                                    np.float32, copy=False))
    else:
        log.info('Skip initializing model parameters from file: {}'.format(
            weights_file
        ))
    log.info('Complete initialize_master_xpu_model_params')
    return start_epoch, lr, best_metric
