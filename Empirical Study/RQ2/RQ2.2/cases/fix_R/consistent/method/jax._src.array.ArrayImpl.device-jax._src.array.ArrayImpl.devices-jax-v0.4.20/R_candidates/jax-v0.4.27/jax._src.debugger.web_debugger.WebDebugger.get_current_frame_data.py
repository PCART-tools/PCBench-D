  def get_current_frame_data(self):
    # Constructs the info needed for the web console to display info
    current_frame = self.current_frame()
    filename = current_frame.filename
    lines = current_frame.source
    current_line = None
    if current_frame.offset is not None:
      current_line = current_frame.offset + 1
    if _web_pdb_version() < (1, 4, 4):
      return {
        'filename': filename,
        'listing': '\n'.join(lines),
        'curr_line': current_line,
        'total_lines': len(lines),
        'breaklist': [],
      }
    return {
        'dirname': os.path.dirname(os.path.abspath(filename)) + os.path.sep,
        'filename': os.path.basename(filename),
        'file_listing': '\n'.join(lines),
        'current_line': current_line,
        'breakpoints': [],
        'globals': self.get_globals(),
        'locals': self.get_locals(),
    }
