  def do_where(self, _):
    """w(here)
    Prints a stack trace with the most recent frame on the bottom.
    'bt' is an alias for this command.
    """
    self.print_backtrace()
