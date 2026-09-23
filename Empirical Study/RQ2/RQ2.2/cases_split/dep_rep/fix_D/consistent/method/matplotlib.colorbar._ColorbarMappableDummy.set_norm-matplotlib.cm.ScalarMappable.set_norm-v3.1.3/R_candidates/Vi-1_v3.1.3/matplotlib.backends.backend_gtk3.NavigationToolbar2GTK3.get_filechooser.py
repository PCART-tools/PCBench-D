    @cbook.deprecated("3.1")
    def get_filechooser(self):
        fc = FileChooserDialog(
            title='Save the figure',
            parent=self.win,
            path=os.path.expanduser(rcParams['savefig.directory']),
            filetypes=self.canvas.get_supported_filetypes(),
            default_filetype=self.canvas.get_default_filetype())
        fc.set_current_name(self.canvas.get_default_filename())
        return fc
