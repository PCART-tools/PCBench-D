  def readline(self):
    with output.use_tags(["stdin"]):
      user_input = input() + "\n"
    output.clear(output_tags=["stdin"])
    return user_input
