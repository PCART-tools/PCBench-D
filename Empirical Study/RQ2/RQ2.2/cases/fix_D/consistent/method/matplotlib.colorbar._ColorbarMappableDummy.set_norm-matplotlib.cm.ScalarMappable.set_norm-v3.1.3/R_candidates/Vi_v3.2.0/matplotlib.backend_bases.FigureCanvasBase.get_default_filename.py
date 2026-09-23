    def get_default_filename(self):
        """
        Return a string, which includes extension, suitable for use as
        a default filename.
        """
        default_basename = self.get_window_title() or 'image'
        default_basename = default_basename.replace(' ', '_')
        default_filetype = self.get_default_filetype()
        default_filename = default_basename + '.' + default_filetype
        return default_filename
