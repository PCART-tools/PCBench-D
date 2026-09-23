    def __exit__(self, exc_type, exc_value, traceback):
        if not self.wasinteractive:
            matplotlib.interactive(False)
            uninstall_repl_displayhook()
        else:
            matplotlib.interactive(True)
            install_repl_displayhook()
