    def trigger(self, *args):
        from six.moves import tkinter_tkfiledialog, tkinter_messagebox
        filetypes = self.figure.canvas.get_supported_filetypes().copy()
        default_filetype = self.figure.canvas.get_default_filetype()

        # Tk doesn't provide a way to choose a default filetype,
        # so we just have to put it first
        default_filetype_name = filetypes.pop(default_filetype)
        sorted_filetypes = ([(default_filetype, default_filetype_name)]
                            + sorted(six.iteritems(filetypes)))
        tk_filetypes = [(name, '*.%s' % ext) for ext, name in sorted_filetypes]

        # adding a default extension seems to break the
        # asksaveasfilename dialog when you choose various save types
        # from the dropdown.  Passing in the empty string seems to
        # work - JDH!
        # defaultextension = self.figure.canvas.get_default_filetype()
        defaultextension = ''
        initialdir = os.path.expanduser(rcParams['savefig.directory'])
        initialfile = self.figure.canvas.get_default_filename()
        fname = tkinter_tkfiledialog.asksaveasfilename(
            master=self.figure.canvas.manager.window,
            title='Save the figure',
            filetypes=tk_filetypes,
            defaultextension=defaultextension,
            initialdir=initialdir,
            initialfile=initialfile,
            )

        if fname == "" or fname == ():
            return
        else:
            if initialdir == '':
                # explicitly missing key or empty str signals to use cwd
                rcParams['savefig.directory'] = initialdir
            else:
                # save dir for next time
                rcParams['savefig.directory'] = os.path.dirname(
                    six.text_type(fname))
            try:
                # This method will handle the delegation to the correct type
                self.figure.savefig(fname)
            except Exception as e:
                tkinter_messagebox.showerror("Error saving file", str(e))
