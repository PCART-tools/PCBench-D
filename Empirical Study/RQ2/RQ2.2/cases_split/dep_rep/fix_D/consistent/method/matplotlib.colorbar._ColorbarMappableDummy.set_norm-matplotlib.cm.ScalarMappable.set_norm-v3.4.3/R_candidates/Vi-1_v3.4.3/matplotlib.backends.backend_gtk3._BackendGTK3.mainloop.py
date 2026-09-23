    @staticmethod
    def mainloop():
        if Gtk.main_level() == 0:
            cbook._setup_new_guiapp()
            Gtk.main()
