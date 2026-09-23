def graph_def_to_event(step, graph_def):
    return Event(
        wall_time=step, step=step, graph_def=graph_def.SerializeToString())
