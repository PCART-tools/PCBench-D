  def _current_truncated_name_stack(self):
    return source_info_util.current_name_stack()[len(self.name_stack):]
