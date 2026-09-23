  def do_list(self, _):
    """l(ist)
    List source code for the current file.
    """
    self.print_context(num_lines=5)
