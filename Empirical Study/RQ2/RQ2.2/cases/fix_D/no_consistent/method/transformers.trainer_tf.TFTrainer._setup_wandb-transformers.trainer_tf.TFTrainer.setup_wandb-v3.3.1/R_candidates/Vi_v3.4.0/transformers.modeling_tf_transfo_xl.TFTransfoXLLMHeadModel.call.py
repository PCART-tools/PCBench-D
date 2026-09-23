    @add_start_docstrings_to_callable(TRANSFO_XL_INPUTS_DOCSTRING)
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="transfo-xl-wt103",
        output_type=TFTransfoXLLMHeadModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(
        self,
        inputs,
        mems=None,
        head_mask=None,
        inputs_embeds=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        labels=None,
        training=False,
    ):
        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            mems = inputs[1] if len(inputs) > 1 else mems
            head_mask = inputs[2] if len(inputs) > 2 else head_mask
            inputs_embeds = inputs[3] if len(inputs) > 3 else inputs_embeds
            output_attentions = inputs[4] if len(inputs) > 4 else output_attentions
            output_hidden_states = inputs[5] if len(inputs) > 5 else output_hidden_states
            return_dict = inputs[6] if len(inputs) > 6 else return_dict
            labels = inputs[7] if len(inputs) > 7 else labels
            assert len(inputs) <= 8, "Too many inputs."
        elif isinstance(inputs, (BatchEncoding, dict)):
            input_ids = inputs.get("input_ids")
            mems = inputs.get("mems", mems)
            head_mask = inputs.get("head_mask", head_mask)
            inputs_embeds = inputs.get("inputs_embeds", inputs_embeds)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
            return_dict = inputs.get("return_dict", return_dict)
            labels = inputs.get("labels", labels)
            assert len(inputs) <= 8, "Too many inputs."
        else:
            input_ids = inputs
        return_dict = return_dict if return_dict is not None else self.transformer.return_dict

        if input_ids is not None:
            bsz, tgt_len = shape_list(input_ids)[:2]
        else:
            bsz, tgt_len = shape_list(inputs_embeds)[:2]

        transformer_outputs = self.transformer(
            input_ids,
            mems,
            head_mask,
            inputs_embeds,
            output_attentions,
            output_hidden_states,
            return_dict,
            training=training,
        )

        last_hidden = transformer_outputs[0]
        pred_hid = last_hidden[:, -tgt_len:]

        softmax_output = self.crit(pred_hid, labels, training=training)

        if not return_dict:
            return (softmax_output,) + transformer_outputs[1:]

        return TFTransfoXLLMHeadModelOutput(
            prediction_scores=softmax_output,
            mems=transformer_outputs.mems,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
