  def bind(self, *args, **params):
    top_trace = find_top_trace(args)
    axis_main = max((axis_frame(a).main_trace for a in used_axis_names(self, params)),
                    default=None, key=lambda t: getattr(t, 'level', -1))
    top_trace = (top_trace if not axis_main or axis_main.level < top_trace.level
                 else axis_main.with_cur_sublevel())
    return self.bind_with_trace(top_trace, args, params)
