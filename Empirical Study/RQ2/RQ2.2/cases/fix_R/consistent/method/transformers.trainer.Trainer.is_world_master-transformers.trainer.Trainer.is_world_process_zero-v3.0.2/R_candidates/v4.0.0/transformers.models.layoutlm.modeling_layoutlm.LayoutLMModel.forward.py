    @add_start_docstrings_to_model_forward(LAYOUTLM_INPUTS_DOCSTRING.format("(batch_size, sequence_length)"))
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="layoutlm-base-uncased",
        output_type=BaseModelOutputWithPoolingAndCrossAttentions,
        config_class=_CONFIG_FOR_DOC,
    )
    def forward(
        self,
        input_ids=None,
        bbox=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        """
        input_ids (torch.LongTensor of shape (batch_size, sequence_length)):
            Indices of input sequence tokens in the vocabulary.
        attention_mask (torch.FloatTensor of shape (batch_size, sequence_length), optional):
            Mask to avoid performing attention on padding token indices. Mask values selected in [0, 1]: 1 for tokens
            that are NOT MASKED, 0 for MASKED tokens.
        token_type_ids (torch.LongTensor of shape (batch_size, sequence_length), optional):
            Segment token indices to indicate first and second portions of the inputs. Indices are selected in [0, 1]:
            0 corresponds to a sentence A token, 1 corresponds to a sentence B token
        position_ids (torch.LongTensor of shape (batch_size, sequence_length), optional):
            Indices of positions of each input sequence tokens in the position embeddings. Selected in the range [0,
            config.max_position_embeddings - 1].
        head_mask (torch.FloatTensor of shape (num_heads,) or (num_layers, num_heads), optional):
            Mask to nullify selected heads of the self-attention modules. Mask values selected in [0, 1]: 1 indicates
            the head is not masked, 0 indicates the head is masked.
        inputs_embeds (torch.FloatTensor of shape (batch_size, sequence_length, hidden_size), optional):
            Optionally, instead of passing input_ids you can choose to directly pass an embedded representation. This
            is useful if you want more control over how to convert input_ids indices into associated vectors than the
            model’s internal embedding lookup matrix.
        output_attentions (bool, optional):
            If set to True, the attentions tensors of all attention layers are returned.
        output_hidden_states (bool, optional):
            If set to True, the hidden states of all layers are returned.
        return_dict (bool, optional):
            If set to True, the model will return a ModelOutput instead of a plain tuple.
        """
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:
            input_shape = input_ids.size()
        elif inputs_embeds is not None:
            input_shape = inputs_embeds.size()[:-1]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        device = input_ids.device if input_ids is not None else inputs_embeds.device

        if attention_mask is None:
            attention_mask = torch.ones(input_shape, device=device)
        if token_type_ids is None:
            token_type_ids = torch.zeros(input_shape, dtype=torch.long, device=device)

        if bbox is None:
            bbox = torch.zeros(tuple(list(input_shape) + [4]), dtype=torch.long, device=device)

        extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)

        extended_attention_mask = extended_attention_mask.to(dtype=self.dtype)
        extended_attention_mask = (1.0 - extended_attention_mask) * -10000.0

        if head_mask is not None:
            if head_mask.dim() == 1:
                head_mask = head_mask.unsqueeze(0).unsqueeze(0).unsqueeze(-1).unsqueeze(-1)
                head_mask = head_mask.expand(self.config.num_hidden_layers, -1, -1, -1, -1)
            elif head_mask.dim() == 2:
                head_mask = head_mask.unsqueeze(1).unsqueeze(-1).unsqueeze(-1)
            head_mask = head_mask.to(dtype=next(self.parameters()).dtype)
        else:
            head_mask = [None] * self.config.num_hidden_layers

        embedding_output = self.embeddings(
            input_ids=input_ids,
            bbox=bbox,
            position_ids=position_ids,
            token_type_ids=token_type_ids,
            inputs_embeds=inputs_embeds,
        )
        encoder_outputs = self.encoder(
            embedding_output,
            extended_attention_mask,
            head_mask=head_mask,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        sequence_output = encoder_outputs[0]
        pooled_output = self.pooler(sequence_output)

        if not return_dict:
            return (sequence_output, pooled_output) + encoder_outputs[1:]

        return BaseModelOutputWithPoolingAndCrossAttentions(
            last_hidden_state=sequence_output,
            pooler_output=pooled_output,
            hidden_states=encoder_outputs.hidden_states,
            attentions=encoder_outputs.attentions,
            cross_attentions=encoder_outputs.cross_attentions,
        )
