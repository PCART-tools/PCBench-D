def get_scheduler_lock(get=None, collection=None):
    """Get an instance of the appropriate lock for a certain situation based on
       scheduler used."""
    actual_get = effective_get(get, collection)

    if actual_get == multiprocessing.get:
        return mp.Manager().Lock()
    return SerializableLock()
