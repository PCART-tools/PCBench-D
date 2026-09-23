    def __init__(self, n_token, d_embed, d_proj, cutoffs, div_val=1, init_std=0.02, sample_softmax=False, **kwargs):
        super().__init__(**kwargs)

        self.n_token = n_token
        self.d_embed = d_embed
        self.init_std = init_std

        self.cutoffs = cutoffs + [n_token]
        self.div_val = div_val
        self.d_proj = d_proj

        self.emb_scale = d_proj ** 0.5

        self.cutoff_ends = [0] + self.cutoffs

        self.emb_layers = []
        self.emb_projs = []
        if div_val == 1:
            raise NotImplementedError  # Removed these to avoid maintaining dead code - They are not used in our pretrained checkpoint
        else:
            for i in range(len(self.cutoffs)):
                l_idx, r_idx = self.cutoff_ends[i], self.cutoff_ends[i + 1]
                d_emb_i = d_embed // (div_val ** i)
                self.emb_layers.append(
                    tf.keras.layers.Embedding(
                        r_idx - l_idx,
                        d_emb_i,
                        embeddings_initializer=get_initializer(init_std),
                        name="emb_layers_._{}".format(i),
                    )
                )
