    @staticmethod
    def _get_global_attn_probs(attn_probs, max_num_global_attn_indices):
        # pad attn_probs to max length with 0.0 since global attn did not attend there
        attn_probs = tf.concat(
            [
                attn_probs[:, :, :, :max_num_global_attn_indices],
                tf.zeros_like(attn_probs)[:, :, :, max_num_global_attn_indices:],
            ],
            axis=-1,
        )
        return attn_probs
