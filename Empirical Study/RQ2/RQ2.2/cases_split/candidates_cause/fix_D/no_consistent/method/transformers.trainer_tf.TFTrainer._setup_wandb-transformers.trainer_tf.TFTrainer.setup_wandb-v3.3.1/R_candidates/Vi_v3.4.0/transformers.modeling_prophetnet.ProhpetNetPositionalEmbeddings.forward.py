    def forward(self, inputs_shape, device, attention_mask=None, past_key_values=None, position_ids=None):
        assert (position_ids is None) or (
            self.padding_idx is None
        ), "If position_ids is pre-computed then padding_idx should not be set."

        if position_ids is None:
            if past_key_values is not None:
                # position_ids is the same for every token when decoding a single step
                # Without the int() cast, it doesn't work in some cases when exporting to ONNX
                prev_num_input_ids = past_key_values[0]["self"]["prev_key_states"].shape[2]
                num_input_ids = inputs_shape[1] + prev_num_input_ids
                position_ids = torch.ones((1, 1), dtype=torch.long, device=device) * (
                    int(self.padding_idx + num_input_ids)
                )
            else:
                if attention_mask is None:
                    attention_mask = torch.ones(inputs_shape, dtype=torch.long, device=device)

                # retrieve position_ids from input_ids / attention_mask
                position_ids = (
                    torch.cumsum(attention_mask, dim=1).type_as(attention_mask) * attention_mask
                ).long() + self.padding_idx

        return super().forward(position_ids), position_ids
