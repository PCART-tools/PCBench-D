    def trigger(self, *args, **kwargs):
        chooser = self.get_filechooser()
        fname, format_ = chooser.get_filename_from_user()
        chooser.destroy()
        if fname:
            startpath = os.path.expanduser(rcParams['savefig.directory'])
            if startpath == '':
                # explicitly missing key or empty str signals to use cwd
                rcParams['savefig.directory'] = startpath
            else:
                # save dir for next time
                rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                self.figure.canvas.print_figure(fname, format=format_)
            except Exception as e:
                error_msg_gtk(str(e), parent=self)
