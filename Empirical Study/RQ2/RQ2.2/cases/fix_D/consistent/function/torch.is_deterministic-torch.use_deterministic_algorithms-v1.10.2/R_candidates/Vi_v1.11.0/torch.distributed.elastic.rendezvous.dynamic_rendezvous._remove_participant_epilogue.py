def _remove_participant_epilogue(state: _RendezvousState, settings: RendezvousSettings) -> None:
    if state.complete:
        # If we do not have any participants left, move to the next round.
        if not state.participants:
            state.complete = False

            state.round += 1
    else:
        if len(state.participants) < settings.min_nodes:
            state.deadline = None
