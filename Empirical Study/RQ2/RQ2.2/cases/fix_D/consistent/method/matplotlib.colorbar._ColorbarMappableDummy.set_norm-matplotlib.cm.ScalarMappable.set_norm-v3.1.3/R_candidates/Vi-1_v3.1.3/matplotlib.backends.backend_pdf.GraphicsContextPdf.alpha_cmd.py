    def alpha_cmd(self, alpha, forced, effective_alphas):
        name = self.file.alphaState(effective_alphas)
        return [name, Op.setgstate]
