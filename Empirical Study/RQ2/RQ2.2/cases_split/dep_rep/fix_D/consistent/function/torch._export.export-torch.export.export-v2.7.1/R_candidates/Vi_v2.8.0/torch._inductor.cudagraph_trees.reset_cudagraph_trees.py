def reset_cudagraph_trees() -> None:
    "Clear all cudagraph trees"
    # see shutdown below for why this is necessary
    container_dict = get_obj(local, "tree_manager_containers")
    locks_dict = get_obj(local, "tree_manager_locks")
    for device, lock in locks_dict.items():
        with lock:
            container = container_dict.get(device)
            if not container or not container.tree_manager:
                continue

            container.tree_manager.shutdown()

    _set_cached_tensors_enabled(False)
    container_dict.clear()

    MarkStepBox.mark_step_counter = 0
