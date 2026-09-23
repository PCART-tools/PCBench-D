  def print_backtrace(self):
    backtrace = []
    backtrace.append('Traceback:')
    for frame in self.frames[::-1]:
      backtrace.append(f'  File "{frame.filename}", line {frame.lineno}')
      if frame.offset is None:
        backtrace.append('    <no source>')
      else:
        line = frame.source[frame.offset]
        backtrace.append(f'    {line.strip()}')
    print("\n".join(backtrace), file=self.stdout)
