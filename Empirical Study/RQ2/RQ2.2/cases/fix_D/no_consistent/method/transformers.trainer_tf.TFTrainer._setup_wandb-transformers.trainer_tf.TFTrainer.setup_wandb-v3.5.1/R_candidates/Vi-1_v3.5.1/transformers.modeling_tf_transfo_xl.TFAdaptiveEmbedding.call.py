    def call(self, inp):
        if self.div_val == 1:
            raise NotImplementedError  # Removed these to avoid maintaining dead code - They are not used in our pretrained checkpoint
        else:
            inp_flat = tf.reshape(inp, (-1,))
            emb_flat = tf.zeros([shape_list(inp_flat)[0], self.d_proj])
            for i in range(len(self.cutoffs)):
                l_idx, r_idx = self.cutoff_ends[i], self.cutoff_ends[i + 1]

                mask_i = (inp_flat >= l_idx) & (inp_flat < r_idx)

                inp_i = tf.boolean_mask(inp_flat, mask_i) - l_idx
                emb_i = self.emb_layers[i](inp_i)
                emb_i = tf.einsum("id,de->ie", emb_i, self.emb_projs[i])

                mask_idx = tf.cast(tf.where(mask_i), dtype=tf.int64)
                emb_flat += tf.scatter_nd(mask_idx, emb_i, tf.cast(shape_list(emb_flat), dtype=tf.int64))

            embed_shape = shape_list(inp) + [self.d_proj]
            embed = tf.reshape(emb_flat, embed_shape)

        embed *= self.emb_scale

        return embed
