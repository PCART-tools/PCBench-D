    def save_figure(self, *args):
        # Fetch the required filename and file type.
        filetypes, exts, filter_index = self.canvas._get_imagesave_wildcards()
        default_file = self.canvas.get_default_filename()
        dlg = wx.FileDialog(self._parent, "Save to file", "", default_file,
                            filetypes,
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        dlg.SetFilterIndex(filter_index)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
            DEBUG_MSG(
                'Save file dir:%s name:%s' %
                (dirname, filename), 3, self)
            format = exts[dlg.GetFilterIndex()]
            basename, ext = os.path.splitext(filename)
            if ext.startswith('.'):
                ext = ext[1:]
            if ext in ('svg', 'pdf', 'ps', 'eps', 'png') and format != ext:
                # looks like they forgot to set the image type drop
                # down, going with the extension.
                warnings.warn(
                    'extension %s did not match the selected '
                    'image type %s; going with %s' %
                    (ext, format, ext), stacklevel=0)
                format = ext
            try:
                self.canvas.figure.savefig(
                    os.path.join(dirname, filename), format=format)
            except Exception as e:
                error_msg_wx(str(e))
