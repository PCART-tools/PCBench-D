    @add_start_docstrings_to_model_forward(XLNET_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=XLNetLMHeadModelOutput, config_class=_CONFIG_FOR_DOC)
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        mems=None,
        perm_mask=None,
        target_mapping=None,
        token_type_ids=None,
        input_mask=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        use_mems=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        **kwargs,  # delete when `use_cache` is removed in XLNetModel
    ):
        r"""
        labels (:obj:`torch.LongTensor` of shape :obj:`(batch_size, num_predict)`, `optional`):
            Labels for masked language modeling. :obj:`num_predict` corresponds to :obj:`target_mapping.shape[1]`. If
            :obj:`target_mapping` is :obj`None`, then :obj:`num_predict` corresponds to :obj:`sequence_length`.

            The labels should correspond to the masked input words that should be predicted and depends on
            :obj:`target_mapping`. Note in order to perform standard auto-regressive language modeling a `<mask>` token
            has to be added to the :obj:`input_ids` (see the :obj:`prepare_inputs_for_generation` function and examples
            below)

            Indices are selected in ``[-100, 0, ..., config.vocab_size]`` All labels set to ``-100`` are ignored, the
            loss is only computed for labels in ``[0, ..., config.vocab_size]``

        Return:

        Examples::

            >>> from transformers import XLNetTokenizer, XLNetLMHeadModel
            >>> import torch

            >>> tokenizer = XLNetTokenizer.from_pretrained('xlnet-large-cased')
            >>> model = XLNetLMHeadModel.from_pretrained('xlnet-large-cased')

            >>> # We show how to setup inputs to predict a next token using a bi-directional context.
            >>> input_ids = torch.tensor(tokenizer.encode("Hello, my dog is very <mask>", add_special_tokens=False)).unsqueeze(0)  # We will predict the masked token
            >>> perm_mask = torch.zeros((1, input_ids.shape[1], input_ids.shape[1]), dtype=torch.float)
            >>> perm_mask[:, :, -1] = 1.0  # Previous tokens don't see last token
            >>> target_mapping = torch.zeros((1, 1, input_ids.shape[1]), dtype=torch.float)  # Shape [1, 1, seq_length] => let's predict one token
            >>> target_mapping[0, 0, -1] = 1.0  # Our first (and only) prediction will be the last token of the sequence (the masked token)

            >>> outputs = model(input_ids, perm_mask=perm_mask, target_mapping=target_mapping)
            >>> next_token_logits = outputs[0]  # Output has shape [target_mapping.size(0), target_mapping.size(1), config.vocab_size]

            >>> # The same way can the XLNetLMHeadModel be used to be trained by standard auto-regressive language modeling.
            >>> input_ids = torch.tensor(tokenizer.encode("Hello, my dog is very <mask>", add_special_tokens=False)).unsqueeze(0)  # We will predict the masked token
            >>> labels = torch.tensor(tokenizer.encode("cute", add_special_tokens=False)).unsqueeze(0)
            >>> assert labels.shape[0] == 1, 'only one word will be predicted'
            >>> perm_mask = torch.zeros((1, input_ids.shape[1], input_ids.shape[1]), dtype=torch.float)
            >>> perm_mask[:, :, -1] = 1.0  # Previous tokens don't see last token as is done in standard auto-regressive lm training
            >>> target_mapping = torch.zeros((1, 1, input_ids.shape[1]), dtype=torch.float)  # Shape [1, 1, seq_length] => let's predict one token
            >>> target_mapping[0, 0, -1] = 1.0  # Our first (and only) prediction will be the last token of the sequence (the masked token)

            >>> outputs = model(input_ids, perm_mask=perm_mask, target_mapping=target_mapping, labels=labels)
            >>> loss = outputs.loss
            >>> next_token_logits = outputs.logits  # Logits have shape [target_mapping.size(0), target_mapping.size(1), config.vocab_size]
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        transformer_outputs = self.transformer(
            input_ids,
            attention_mask=attention_mask,
            mems=mems,
            perm_mask=perm_mask,
            target_mapping=target_mapping,
            token_type_ids=token_type_ids,
            input_mask=input_mask,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            use_mems=use_mems,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            **kwargs,
        )

        logits = self.lm_loss(transformer_outputs[0])

        loss = None
        if labels is not None:
            # Flatten the tokens
            loss_fct = CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, logits.size(-1)), labels.view(-1))

        if not return_dict:
            output = (logits,) + transformer_outputs[1:]
            return ((loss,) + output) if loss is not None else output

        return XLNetLMHeadModelOutput(
            loss=loss,
            logits=logits,
            mems=transformer_outputs.mems,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
