def cpu_time_total(autograd_prof):
    return sum([event.cpu_time_total for event in autograd_prof.function_events])
