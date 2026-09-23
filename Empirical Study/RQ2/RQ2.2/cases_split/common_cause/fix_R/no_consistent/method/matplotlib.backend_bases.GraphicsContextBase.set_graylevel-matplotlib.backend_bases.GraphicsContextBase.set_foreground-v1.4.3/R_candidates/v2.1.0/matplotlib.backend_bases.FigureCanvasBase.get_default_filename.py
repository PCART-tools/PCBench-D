    def get_default_filename(self):
        """
        Return a string, which includes extension, suitable for use as
        a default filename.
        """
        default_basename = self.get_window_title() or 'image'
        default_basename = default_basename.replace(' ', '_')
        default_filetype = self.get_default_filetype()
        default_filename = default_basename + '.' + default_filetype

        save_dir = os.path.expanduser(rcParams['savefig.directory'])

        # ensure non-existing filename in save dir
        i = 1
        while os.path.isfile(os.path.join(save_dir, default_filename)):
            # attach numerical count to basename
            default_filename = '{0}-{1}.{2}'.format(default_basename, i, default_filetype)
            i += 1

        return default_filename
