  def evaluate(self, expr):
    env = {}
    curr_frame = self.frames[self.frame_index]
    env.update(curr_frame.globals)
    env.update(curr_frame.locals)
    return eval(expr, {}, env)
