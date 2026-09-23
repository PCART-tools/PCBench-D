    def get_filechooser(self):
        fc = FileChooserDialog(
            title='Save the figure',
            parent=self.figure.canvas.manager.window,
            path=os.path.expanduser(rcParams['savefig.directory']),
            filetypes=self.figure.canvas.get_supported_filetypes(),
            default_filetype=self.figure.canvas.get_default_filetype())
        fc.set_current_name(self.figure.canvas.get_default_filename())
        return fc
