    @staticmethod
    def mainloop():
        if Gtk.main_level() == 0:
            Gtk.main()
