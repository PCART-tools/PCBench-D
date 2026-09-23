    def trigger(self, *args):
        image = os.path.join(matplotlib.rcParams['datapath'],
                             'images', 'matplotlib.png')
        parent = self.canvas.manager.window
        dia = SubplotToolQt(self.figure, parent)
        dia.setWindowIcon(QtGui.QIcon(image))
        dia.exec_()
