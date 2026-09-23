    def build(self, input_shape):
        for i in range(len(self.cutoffs)):
            d_emb_i = self.d_embed // (self.div_val ** i)
            self.emb_projs.append(
                self.add_weight(
                    shape=(d_emb_i, self.d_proj),
                    initializer=get_initializer(self.init_std),
                    trainable=True,
                    name="emb_projs_._{}".format(i),
                )
            )
        super().build(input_shape)
