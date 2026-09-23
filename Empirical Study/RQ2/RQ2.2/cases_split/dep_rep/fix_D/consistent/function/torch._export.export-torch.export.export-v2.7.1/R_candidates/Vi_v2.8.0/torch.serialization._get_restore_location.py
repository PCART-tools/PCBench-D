def _get_restore_location(map_location):
    if map_location is None:
        restore_location = default_restore_location
    elif isinstance(map_location, dict):

        def restore_location(storage, location):
            location = map_location.get(location, location)
            return default_restore_location(storage, location)

    elif isinstance(map_location, (str, bytes)):

        def restore_location(storage, location):
            return default_restore_location(storage, map_location)

    elif isinstance(map_location, torch.device):

        def restore_location(storage, location):
            return default_restore_location(storage, str(map_location))

    else:

        def restore_location(storage, location):
            result = map_location(storage, location)
            if result is None:
                result = default_restore_location(storage, location)
            return result

    return restore_location
