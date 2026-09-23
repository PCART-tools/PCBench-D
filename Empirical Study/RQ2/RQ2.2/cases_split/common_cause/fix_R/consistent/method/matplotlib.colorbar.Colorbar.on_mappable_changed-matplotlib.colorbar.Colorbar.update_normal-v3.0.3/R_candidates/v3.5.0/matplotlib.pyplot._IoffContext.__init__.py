    def __init__(self):
        self.wasinteractive = isinteractive()
        matplotlib.interactive(False)
        uninstall_repl_displayhook()
