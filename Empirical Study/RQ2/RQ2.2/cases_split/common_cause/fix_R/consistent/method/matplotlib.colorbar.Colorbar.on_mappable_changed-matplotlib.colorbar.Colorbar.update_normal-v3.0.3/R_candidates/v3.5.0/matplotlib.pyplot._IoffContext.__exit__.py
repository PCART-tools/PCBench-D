    def __exit__(self, exc_type, exc_value, traceback):
        if self.wasinteractive:
            matplotlib.interactive(True)
            install_repl_displayhook()
        else:
            matplotlib.interactive(False)
            uninstall_repl_displayhook()
