    def __init__(self):
        self.wasinteractive = isinteractive()
        matplotlib.interactive(True)
        install_repl_displayhook()
