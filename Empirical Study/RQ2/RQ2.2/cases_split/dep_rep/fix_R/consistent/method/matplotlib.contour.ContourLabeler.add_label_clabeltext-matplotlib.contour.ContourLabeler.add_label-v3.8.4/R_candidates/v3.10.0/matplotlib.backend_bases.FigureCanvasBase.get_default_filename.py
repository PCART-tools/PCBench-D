    def get_default_filename(self):
        """
        Return a suitable default filename, including the extension.
        """
        default_basename = (
            self.manager.get_window_title()
            if self.manager is not None
            else ''
        )
        default_basename = default_basename or 'image'
        # Characters to be avoided in a NT path:
        # https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#naming_conventions
        # plus ' '
        removed_chars = r'<>:"/\|?*\0 '
        default_basename = default_basename.translate(
            {ord(c): "_" for c in removed_chars})
        default_filetype = self.get_default_filetype()
        return f'{default_basename}.{default_filetype}'
