def runShardedTrainLoop(opts, myTrainFun):
    start_epoch = 0
    pretrained_model = opts['model_param']['pretrained_model']
    if pretrained_model != '' and os.path.exists(pretrained_model):
        # Only want to get start_epoch.
        start_epoch, prev_checkpointed_lr, best_metric = \
            checkpoint.initialize_params_from_file(
                model=None,
                weights_file=pretrained_model,
                num_xpus=1,
                opts=opts,
                broadcast_computed_param=True,
                reset_epoch=opts['model_param']['reset_epoch'],
            )
    log.info('start epoch: {}'.format(start_epoch))
    pretrained_model = None if pretrained_model == '' else pretrained_model
    ret = None

    pretrained_model = ""
    shard_results = []

    for epoch in range(start_epoch,
                       opts['epoch_iter']['num_epochs'],
                       opts['epoch_iter']['num_epochs_per_flow_schedule']):
        # must support checkpoint or the multiple schedule will always
        # start from initial state
        checkpoint_model = None if epoch == start_epoch else ret['model']
        pretrained_model = None if epoch > start_epoch else pretrained_model
        shard_results = []
        # with LexicalContext('epoch{}_gang'.format(epoch),gang_schedule=False):
        for shard_id in range(opts['distributed']['num_shards']):
            opts['temp_var']['shard_id'] = shard_id
            opts['temp_var']['pretrained_model'] = pretrained_model
            opts['temp_var']['checkpoint_model'] = checkpoint_model
            opts['temp_var']['epoch'] = epoch
            opts['temp_var']['start_epoch'] = start_epoch
            shard_ret = myTrainFun(opts)
            shard_results.append(shard_ret)

        ret = None
        # always only take shard_0 return
        for shard_ret in shard_results:
            if shard_ret is not None:
                ret = shard_ret
                opts['temp_var']['metrics_output'] = ret['metrics']
                break
        log.info('ret is: {}'.format(str(ret)))

    return ret
