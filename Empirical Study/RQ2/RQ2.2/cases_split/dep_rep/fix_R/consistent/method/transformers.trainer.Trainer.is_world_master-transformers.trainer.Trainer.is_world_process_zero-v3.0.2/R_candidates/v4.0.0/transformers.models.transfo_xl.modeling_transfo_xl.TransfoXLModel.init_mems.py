    def init_mems(self, bsz):
        if self.mem_len > 0:
            mems = []
            param = next(self.parameters())
            for i in range(self.n_layer):
                empty = torch.zeros(self.mem_len, bsz, self.config.d_model, dtype=param.dtype, device=param.device)
                mems.append(empty)

            return mems
        else:
            return None
