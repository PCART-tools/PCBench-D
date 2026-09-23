def RunEpoch(
    args,
    epoch,
    train_model,
    test_model,
    total_batch_size,
    num_shards,
    expname,
    explog,
):
    '''
    Run one epoch of the trainer.
    TODO: add checkpointing here.
    '''
    # TODO: add loading from checkpoint
    log.info("Starting epoch {}/{}".format(epoch, args.num_epochs))
    epoch_iters = int(args.epoch_size / total_batch_size / num_shards)
    test_epoch_iters = int(args.test_epoch_size / total_batch_size / num_shards)
    for i in range(epoch_iters):
        # This timeout is required (temporarily) since CUDA-NCCL
        # operators might deadlock when synchronizing between GPUs.
        timeout = args.first_iter_timeout if i == 0 else args.timeout
        with timeout_guard.CompleteInTimeOrDie(timeout):
            t1 = time.time()
            workspace.RunNet(train_model.net.Proto().name)
            t2 = time.time()
            dt = t2 - t1

        fmt = "Finished iteration {}/{} of epoch {} ({:.2f} images/sec)"
        log.info(fmt.format(i + 1, epoch_iters, epoch, total_batch_size / dt))
        prefix = "{}_{}".format(
            train_model._device_prefix,
            train_model._devices[0])
        accuracy = workspace.FetchBlob(prefix + '/accuracy')
        loss = workspace.FetchBlob(prefix + '/loss')
        train_fmt = "Training loss: {}, accuracy: {}"
        log.info(train_fmt.format(loss, accuracy))

    num_images = epoch * epoch_iters * total_batch_size
    prefix = "{}_{}".format(train_model._device_prefix, train_model._devices[0])
    accuracy = workspace.FetchBlob(prefix + '/accuracy')
    loss = workspace.FetchBlob(prefix + '/loss')
    learning_rate = workspace.FetchBlob(
        data_parallel_model.GetLearningRateBlobNames(train_model)[0]
    )
    test_accuracy = 0
    test_accuracy_top5 = 0
    if test_model is not None:
        # Run 100 iters of testing
        ntests = 0
        for _ in range(test_epoch_iters):
            workspace.RunNet(test_model.net.Proto().name)
            for g in test_model._devices:
                test_accuracy += np.asscalar(workspace.FetchBlob(
                    "{}_{}".format(test_model._device_prefix, g) + '/accuracy'
                ))
                test_accuracy_top5 += np.asscalar(workspace.FetchBlob(
                    "{}_{}".format(test_model._device_prefix, g) + '/accuracy_top5'
                ))
                ntests += 1
        test_accuracy /= ntests
        test_accuracy_top5 /= ntests
    else:
        test_accuracy = (-1)
        test_accuracy_top5 = (-1)

    explog.log(
        input_count=num_images,
        batch_count=(i + epoch * epoch_iters),
        additional_values={
            'accuracy': accuracy,
            'loss': loss,
            'learning_rate': learning_rate,
            'epoch': epoch,
            'top1_test_accuracy': test_accuracy,
            'top5_test_accuracy': test_accuracy_top5,
        }
    )
    assert loss < 40, "Exploded gradients :("

    # TODO: add checkpointing
    return epoch + 1
