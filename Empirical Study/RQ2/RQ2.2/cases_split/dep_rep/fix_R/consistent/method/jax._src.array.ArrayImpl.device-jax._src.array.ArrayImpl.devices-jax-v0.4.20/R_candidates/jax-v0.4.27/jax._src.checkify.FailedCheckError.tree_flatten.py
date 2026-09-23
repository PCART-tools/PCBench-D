  def tree_flatten(self):
    return ((self.args, self.kwargs),  # leaves
            (self.traceback_info, self.fmt_string))  # treedef
