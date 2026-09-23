    def get_active_linestyle(self):
        'get the active lineinestyle'
        ind = self.cbox_linestyles.get_active()
        ls = self.linestyles[ind]
        return ls
