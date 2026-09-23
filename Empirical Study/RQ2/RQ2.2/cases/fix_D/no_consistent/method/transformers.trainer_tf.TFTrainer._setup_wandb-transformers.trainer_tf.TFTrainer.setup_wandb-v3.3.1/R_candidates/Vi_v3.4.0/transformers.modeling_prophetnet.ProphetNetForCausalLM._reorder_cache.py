    @staticmethod
    def _reorder_cache(past, beam_idx):
        # this function reorders the cache for beam search
        def _reorder_cache(cache_dict, beam_idx):
            for k, key_value_states in cache_dict.items():
                if key_value_states is not None:
                    cache_dict[k] = key_value_states.index_select(0, beam_idx)
            return cache_dict

        reordered_past = []
        for layer_past in past:
            # get the correct batch idx from decoder layer's batch dim for cross and self-attn
            layer_past_new = {
                attn_key: _reorder_cache(attn_cache, beam_idx) for attn_key, attn_cache in layer_past.items()
            }
            reordered_past.append(layer_past_new)
        return reordered_past
