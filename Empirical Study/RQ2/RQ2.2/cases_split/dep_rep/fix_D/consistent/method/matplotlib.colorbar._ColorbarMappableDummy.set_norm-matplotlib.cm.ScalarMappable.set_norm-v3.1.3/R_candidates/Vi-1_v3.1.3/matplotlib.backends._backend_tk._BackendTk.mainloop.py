    @staticmethod
    def mainloop():
        managers = Gcf.get_all_fig_managers()
        if managers:
            managers[0].window.mainloop()
