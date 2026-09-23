  def get_locals(self):
    current_frame = self.current_frame()
    return "\n".join(
        f"{key} = {value}"
        for key, value in sorted(current_frame.locals.items()))
