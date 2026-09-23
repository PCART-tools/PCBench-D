  def print_context(self, num_lines=2):
    curr_frame = self.frames[self.frame_index]
    context = []
    context.append(f'> {curr_frame.filename}({curr_frame.lineno})')
    for i, line in enumerate(curr_frame.source):
      assert curr_frame.offset is not None
      if (curr_frame.offset - 1 - num_lines <= i <=
          curr_frame.offset + num_lines):
        if i == curr_frame.offset:
          context.append(f'->  {line}')
        else:
          context.append(f'    {line}')
    print("\n".join(context), file=self.stdout)
