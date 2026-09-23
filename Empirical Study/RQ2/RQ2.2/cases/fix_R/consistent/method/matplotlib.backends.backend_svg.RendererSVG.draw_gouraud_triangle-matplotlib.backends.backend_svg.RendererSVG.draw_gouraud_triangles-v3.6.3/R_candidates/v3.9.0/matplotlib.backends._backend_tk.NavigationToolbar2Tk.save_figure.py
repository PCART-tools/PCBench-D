    def save_figure(self, *args):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        tk_filetypes = [
            (name, " ".join(f"*.{ext}" for ext in exts))
            for name, exts in sorted(filetypes.items())
        ]

        default_extension = self.canvas.get_default_filetype()
        default_filetype = self.canvas.get_supported_filetypes()[default_extension]
        filetype_variable = tk.StringVar(self.canvas.get_tk_widget(), default_filetype)

        # adding a default extension seems to break the
        # asksaveasfilename dialog when you choose various save types
        # from the dropdown.  Passing in the empty string seems to
        # work - JDH!
        # defaultextension = self.canvas.get_default_filetype()
        defaultextension = ''
        initialdir = os.path.expanduser(mpl.rcParams['savefig.directory'])
        # get_default_filename() contains the default extension. On some platforms,
        # choosing a different extension from the dropdown does not overwrite it,
        # so we need to remove it to make the dropdown functional.
        initialfile = pathlib.Path(self.canvas.get_default_filename()).stem
        fname = tkinter.filedialog.asksaveasfilename(
            master=self.canvas.get_tk_widget().master,
            title='Save the figure',
            filetypes=tk_filetypes,
            defaultextension=defaultextension,
            initialdir=initialdir,
            initialfile=initialfile,
            typevariable=filetype_variable
            )

        if fname in ["", ()]:
            return
        # Save dir for next time, unless empty str (i.e., use cwd).
        if initialdir != "":
            mpl.rcParams['savefig.directory'] = (
                os.path.dirname(str(fname)))

        # If the filename contains an extension, let savefig() infer the file
        # format from that. If it does not, use the selected dropdown option.
        if pathlib.Path(fname).suffix[1:] != "":
            extension = None
        else:
            extension = filetypes[filetype_variable.get()][0]

        try:
            self.canvas.figure.savefig(fname, format=extension)
        except Exception as e:
            tkinter.messagebox.showerror("Error saving file", str(e))
