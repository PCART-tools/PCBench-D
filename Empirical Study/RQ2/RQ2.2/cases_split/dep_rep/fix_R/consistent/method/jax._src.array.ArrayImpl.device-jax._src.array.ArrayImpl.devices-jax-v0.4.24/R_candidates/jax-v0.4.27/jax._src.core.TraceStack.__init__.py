  def __init__(self):
    eval_trace = MainTrace(0, EvalTrace)
    self.stack = [eval_trace]
    self.dynamic = eval_trace
