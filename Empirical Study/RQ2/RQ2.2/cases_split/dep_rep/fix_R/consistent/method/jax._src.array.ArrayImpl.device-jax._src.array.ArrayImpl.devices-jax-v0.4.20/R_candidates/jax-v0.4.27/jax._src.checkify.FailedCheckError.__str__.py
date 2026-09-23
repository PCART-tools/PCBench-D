  def __str__(self):
    return (self.fmt_string.format(*self.args, **self.kwargs)
            + ' (`check` failed)')
