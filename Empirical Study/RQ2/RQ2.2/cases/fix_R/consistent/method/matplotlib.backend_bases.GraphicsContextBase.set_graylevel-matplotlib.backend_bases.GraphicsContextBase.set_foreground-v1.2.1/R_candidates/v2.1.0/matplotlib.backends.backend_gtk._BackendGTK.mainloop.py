    @staticmethod
    def mainloop():
        if gtk.main_level() == 0:
            gtk.main()
