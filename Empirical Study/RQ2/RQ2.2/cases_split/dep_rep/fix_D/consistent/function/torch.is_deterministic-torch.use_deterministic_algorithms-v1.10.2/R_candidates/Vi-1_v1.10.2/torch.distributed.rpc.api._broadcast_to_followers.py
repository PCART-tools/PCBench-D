def _broadcast_to_followers(sequence_id, objects_map):
    with _all_gather_dict_lock:
        states = _all_gather_sequence_id_to_states[sequence_id]

    assert (
        not states.proceed_signal.is_set()
    ), "Termination signal sequence id {} got set twice.".format(sequence_id)
    states.gathered_objects = objects_map
    states.proceed_signal.set()
