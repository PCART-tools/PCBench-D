    @add_start_docstrings_to_callable(LXMERT_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=LxmertForPreTrainingOutput, config_class=_CONFIG_FOR_DOC)
    def forward(
        self,
        input_ids=None,
        visual_feats=None,
        visual_pos=None,
        attention_mask=None,
        visual_attention_mask=None,
        token_type_ids=None,
        inputs_embeds=None,
        masked_lm_labels=None,
        obj_labels=None,
        matched_label=None,
        ans=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        r"""
        masked_lm_labels (``torch.LongTensor`` of shape ``(batch_size, sequence_length)``, `optional`):
            Labels for computing the masked language modeling loss.
            Indices should be in ``[-100, 0, ..., config.vocab_size]`` (see ``input_ids`` docstring)
            Tokens with indices set to ``-100`` are ignored (masked), the loss is only computed for the tokens with labels
            in ``[0, ..., config.vocab_size]``
        obj_labels: (``Dict[Str: Tuple[Torch.FloatTensor, Torch.FloatTensor]]``, `optional`):
            each key is named after each one of the visual losses and each element of the tuple is of the shape
            ``(batch_size, num_features)`` and ``(batch_size, num_features, visual_feature_dim)``
            for each the label id and the label score respectively
        matched_label (``torch.LongTensor`` of shape ``(batch_size,)``, `optional`):
            Labels for computing the whether or not the text input matches the image (classification) loss. Input should be a sequence pair (see :obj:`input_ids` docstring)
            Indices should be in ``[0, 1]``:

            - 0 indicates that the sentence does not match the image,
            - 1 indicates that the sentence does match the image.
        ans: (``Torch.Tensor`` of shape ``(batch_size)``, `optional`):
            a one hot representation hof the correct answer `optional`

        Returns:
        """

        device = input_ids.device if input_ids is not None else inputs_embeds.device
        lxmert_output = self.lxmert(
            input_ids=input_ids,
            visual_feats=visual_feats,
            visual_pos=visual_pos,
            token_type_ids=token_type_ids,
            attention_mask=attention_mask,
            visual_attention_mask=visual_attention_mask,
            inputs_embeds=inputs_embeds,
            output_hidden_states=output_hidden_states,
            output_attentions=output_attentions,
            return_dict=return_dict,
        )

        lang_output, visual_output, pooled_output = (
            lxmert_output[0],
            lxmert_output[1],
            lxmert_output[2],
        )
        lang_prediction_scores, cross_relationship_score = self.cls(lang_output, pooled_output)
        if self.task_qa:
            answer_score = self.answer_head(pooled_output)
        else:
            answer_score = pooled_output[0][0]

        total_loss = (
            None
            if (masked_lm_labels is None and matched_label is None and obj_labels is None and ans is None)
            else torch.tensor(0.0, device=device)
        )
        if masked_lm_labels is not None and self.task_mask_lm:
            masked_lm_loss = self.loss_fcts["ce"](
                lang_prediction_scores.view(-1, self.config.vocab_size),
                masked_lm_labels.view(-1),
            )
            total_loss += masked_lm_loss
        if matched_label is not None and self.task_matched:
            matched_loss = self.loss_fcts["ce"](cross_relationship_score.view(-1, 2), matched_label.view(-1))
            total_loss += matched_loss
        if obj_labels is not None and self.task_obj_predict:
            total_visual_loss = torch.tensor(0.0, device=input_ids.device)
            visual_prediction_scores_dict = self.obj_predict_head(visual_output)
            for key, key_info in self.visual_losses.items():
                label, mask_conf = obj_labels[key]
                output_dim = key_info["num"]
                loss_fct_name = key_info["loss"]
                label_shape = key_info["shape"]
                weight = self.visual_loss_normalizer
                visual_loss_fct = self.loss_fcts[loss_fct_name]
                visual_prediction_scores = visual_prediction_scores_dict[key]
                visual_loss = visual_loss_fct(
                    visual_prediction_scores.view(-1, output_dim),
                    label.view(*label_shape),
                )
                if visual_loss.dim() > 1:  # Regression Losses
                    visual_loss = visual_loss.mean(1)
                visual_loss = (visual_loss * mask_conf.view(-1)).mean() * weight
                total_visual_loss += visual_loss
            total_loss += total_visual_loss
        if ans is not None and self.task_qa:
            answer_loss = self.loss_fcts["ce"](answer_score.view(-1, self.num_qa_labels), ans.view(-1))
            total_loss += answer_loss

        if not return_dict:
            output = (
                lang_prediction_scores,
                cross_relationship_score,
                answer_score,
            ) + lxmert_output[3:]
            return ((total_loss,) + output) if total_loss is not None else output

        return LxmertForPreTrainingOutput(
            loss=total_loss,
            prediction_logits=lang_prediction_scores,
            cross_relationship_score=cross_relationship_score,
            question_answering_score=answer_score,
            language_hidden_states=lxmert_output.language_hidden_states,
            vision_hidden_states=lxmert_output.vision_hidden_states,
            language_attentions=lxmert_output.language_attentions,
            vision_attentions=lxmert_output.vision_attentions,
            cross_encoder_attentions=lxmert_output.cross_encoder_attentions,
        )
