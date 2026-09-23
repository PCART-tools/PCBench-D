    def save_figure(self, *args):
        # Fetch the required filename and file type.
        filetypes, exts, filter_index = self.canvas._get_imagesave_wildcards()
        default_file = self.canvas.get_default_filename()
        dialog = wx.FileDialog(
            self.canvas.GetParent(), "Save to file",
            mpl.rcParams["savefig.directory"], default_file, filetypes,
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        dialog.SetFilterIndex(filter_index)
        if dialog.ShowModal() == wx.ID_OK:
            path = pathlib.Path(dialog.GetPath())
            _log.debug('%s - Save file path: %s', type(self), path)
            fmt = exts[dialog.GetFilterIndex()]
            ext = path.suffix[1:]
            if ext in self.canvas.get_supported_filetypes() and fmt != ext:
                # looks like they forgot to set the image type drop
                # down, going with the extension.
                _log.warning('extension %s did not match the selected '
                             'image type %s; going with %s',
                             ext, fmt, ext)
                fmt = ext
            # Save dir for next time, unless empty str (which means use cwd).
            if mpl.rcParams["savefig.directory"]:
                mpl.rcParams["savefig.directory"] = str(path.parent)
            try:
                self.canvas.figure.savefig(path, format=fmt)
                return path
            except Exception as e:
                dialog = wx.MessageDialog(
                    parent=self.canvas.GetParent(), message=str(e),
                    caption='Matplotlib error')
                dialog.ShowModal()
                dialog.Destroy()
