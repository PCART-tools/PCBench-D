def enqueuer(coordinator, batch_feeder):
    while coordinator.is_active():
        batch_feeder._enqueue_batch(coordinator)
