def get_profiling_event(postfix, profiler):
    event_list = (
        profiler.events()
        if isinstance(profiler, torch.profiler.profile)
        else profiler.function_events
    )
    return [event for event in event_list if event.name.endswith(postfix)]
