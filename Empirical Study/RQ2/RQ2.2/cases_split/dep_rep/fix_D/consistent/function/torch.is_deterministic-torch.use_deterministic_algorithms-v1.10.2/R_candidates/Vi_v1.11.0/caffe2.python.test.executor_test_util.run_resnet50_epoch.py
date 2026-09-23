def run_resnet50_epoch(train_model, batch_size, epoch_size, skip_first_n_iter=0):
    epoch_iters = int(epoch_size / batch_size)
    prefix = "{}_{}".format(
        train_model._device_prefix,
        train_model._devices[0])
    train_time = 0.0
    train_examples = 0
    for i in range(epoch_iters):
        timeout = 600.0 if i == 0 else 60.0
        with timeout_guard.CompleteInTimeOrDie(timeout):
            t1 = time.time()
            workspace.RunNet(train_model.net.Proto().name)
            t2 = time.time()
            dt = t2 - t1
            if i >= skip_first_n_iter:
                train_time += dt
                train_examples += batch_size

        fmt = "Finished iteration {}/{} ({:.2f} images/sec)"
        print(fmt.format(i + 1, epoch_iters, batch_size / dt))

    accuracy = workspace.FetchBlob(prefix + '/accuracy')
    loss = workspace.FetchBlob(prefix + '/loss')

    assert loss < 40, "Exploded gradients"

    return (
        train_examples,
        train_time,
        accuracy, loss)
