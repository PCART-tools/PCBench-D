    def save_figure(self, *args):
        chooser = self.get_filechooser()
        fname, format = chooser.get_filename_from_user()
        chooser.destroy()
        if fname:
            startpath = os.path.expanduser(rcParams['savefig.directory'])
            # Save dir for next time, unless empty str (i.e., use cwd).
            if startpath != "":
                rcParams['savefig.directory'] = (
                    os.path.dirname(six.text_type(fname)))
            try:
                self.canvas.figure.savefig(fname, format=format)
            except Exception as e:
                error_msg_gtk(str(e), parent=self)
