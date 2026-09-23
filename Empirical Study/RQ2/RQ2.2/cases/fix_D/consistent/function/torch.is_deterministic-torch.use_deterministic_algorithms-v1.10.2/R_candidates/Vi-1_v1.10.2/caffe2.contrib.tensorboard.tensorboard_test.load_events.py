def load_events(filename):
    try:
        # tensorboard>=1.14.0
        from tensorboard.backend.event_processing import event_file_loader
        loader = event_file_loader.EventFileLoader(filename)
        return list(loader.Load())
    except ImportError:
        import tensorflow as tf
        return list(tf.train.summary_iterator(filename))
