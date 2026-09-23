def _validate_schedule(
    actions: dict[int, list[Optional[_Action]]],
    pp_group_size: int,
    num_stages: int,
    num_microbatches: int,
) -> dict[int, int]:
    assert len(actions) == pp_group_size, (
        f"Schedule has incorrect number of ranks - expected {pp_group_size}, actual {len(actions)}"
    )
    for rank in range(pp_group_size):
        assert rank in actions, f"Schedule is missing actions for rank {rank}"

    # We will count all the actions per stage and ensure they happen in a valid order
    # (e.g. F before (B, I) before W for a given microbatch)
    stage_actions: dict[int, dict[_ComputationType, set]] = {
        stage_id: {
            F: set(),
            B: set(),
            I: set(),
            W: set(),
        }
        for stage_id in range(num_stages)
    }
    stage_index_to_rank_mapping = {}
    for rank in actions:
        for action in actions[rank]:
            if action is None:
                continue
            assert isinstance(action, _Action), (
                f"Got an invalid action: {action}, expected instance of _Action"
            )
            s_id = action.stage_index
            ctype = action.computation_type
            mb_id = action.microbatch_index
            if ctype == F:
                stage_actions[s_id][F].add(mb_id)
            elif ctype == B:
                assert mb_id in stage_actions[s_id][F], (
                    f"Running Full Backward for stage {s_id}, microbatch {mb_id} without first running Forward"
                )
                stage_actions[s_id][B].add(mb_id)
            elif ctype == I:
                assert mb_id in stage_actions[s_id][F], (
                    f"Running Backward Input for stage {s_id}, microbatch {mb_id} without first running Forward"
                )
                stage_actions[s_id][I].add(mb_id)
            elif ctype == W:
                assert mb_id in stage_actions[s_id][I], (
                    f"Running Backward Weight for stage {s_id}, microbatch {mb_id} without first running Backward Input"
                )
                stage_actions[s_id][W].add(mb_id)
            if s_id not in stage_index_to_rank_mapping:
                stage_index_to_rank_mapping[s_id] = rank
            else:
                existing_rank = stage_index_to_rank_mapping[s_id]
                assert rank == existing_rank, (
                    f"Stage {s_id} is assigned to both rank {rank} and rank {existing_rank}"
                )

    for s_id in stage_actions:
        f_mb = len(stage_actions[s_id][F])
        b_mb = len(stage_actions[s_id][B])
        i_mb = len(stage_actions[s_id][I])
        w_mb = len(stage_actions[s_id][W])

        assert f_mb == num_microbatches, (
            f"Got {f_mb} {F} microbatches for stage {s_id}, expected {num_microbatches}"
        )

        assert b_mb + (i_mb + w_mb) // 2 == num_microbatches, (
            f"Invalid backward microbatches for stage {s_id}: expected {num_microbatches} total backwards, \
            but got B={b_mb}, I={i_mb}, W={w_mb}"
        )
    return stage_index_to_rank_mapping
