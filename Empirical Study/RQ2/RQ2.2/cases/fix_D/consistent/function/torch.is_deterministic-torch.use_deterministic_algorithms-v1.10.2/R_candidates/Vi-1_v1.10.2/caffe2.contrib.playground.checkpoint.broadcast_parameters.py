def broadcast_parameters(opts, model, num_xpus, broadcast_computed_param=False):
    if num_xpus == 1:
        log.info("only 1 device. Skip parameter broadcast")
        return
    all_params = [model.GetParams()]
    if broadcast_computed_param:
        all_params.append(model.GetComputedParams())
    caffe2_pb2_DEVICE =\
        caffe2_pb2.CUDA if opts['distributed']['device'] == 'gpu'\
        else caffe2_pb2.CPU
    for params in all_params:
        assert len(params) % num_xpus == 0, \
            "Current model doesn't match device number when loading checkpoint"
        params_per_xpu = int(len(params) / num_xpus)
        for idx in range(params_per_xpu):
            blobs = [param for param in params[idx::params_per_xpu]]
            data = workspace.FetchBlob(blobs[0])
            log.info('Broadcasting {} to'.format(str(blobs[0])))
            for i, p in enumerate(blobs[1:]):
                log.info(' |-> {}'.format(str(p)))
                with core.DeviceScope(core.DeviceOption(caffe2_pb2_DEVICE, i+1)):
                    workspace.FeedBlob(p, data)
    log.info("Complete parameter broadcast")
