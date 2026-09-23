    @add_start_docstrings_to_callable(LXMERT_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFLxmertForPreTrainingOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs=None,
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
        masked_lm_labels (``tf.Tensor`` of shape ``(batch_size, sequence_length)``, `optional`):
            Labels for computing the masked language modeling loss.
            Indices should be in ``[-100, 0, ..., config.vocab_size]`` (see ``input_ids`` docstring)
            Tokens with indices set to ``-100`` are ignored (masked), the loss is only computed for the tokens with labels
            in ``[0, ..., config.vocab_size]``
        obj_labels: (``Dict[Str: Tuple[tf.Tensor, tf.Tensor]]``, `optional`, defaults to :obj: `None`):
            each key is named after each one of the visual losses and each element of the tuple is of the shape
            ``(batch_size, num_features)`` and ``(batch_size, num_features, visual_feature_dim)``
            for each the label id and the label score respectively
        matched_label (``tf.Tensor`` of shape ``(batch_size,)``, `optional`):
            Labels for computing the whether or not the text input matches the image (classification) loss. Input
            should be a sequence pair (see :obj:`input_ids` docstring)
            Indices should be in ``[0, 1]``:

            - 0 indicates that the sentence does not match the image,
            - 1 indicates that the sentence does match the image.
        ans: (``Torch.Tensor`` of shape ``(batch_size)``, `optional`, defaults to :obj: `None`):
            a one hot representation hof the correct answer `optional`

        Returns:
        """
        if isinstance(inputs, (tuple, list)):
            masked_lm_labels = inputs[7] if len(inputs) > 7 else masked_lm_labels
            obj_labels = inputs[8] if len(inputs) > 8 else obj_labels
            matched_label = inputs[9] if len(inputs) > 9 else matched_label
            ans = inputs[10] if len(inputs) > 10 else ans
            if len(inputs) > 10:
                inputs = inputs[:10]
        elif isinstance(inputs, (dict, BatchEncoding)):
            masked_lm_labels = inputs.pop("masked_lm_labels", masked_lm_labels)
            obj_labels = inputs.pop("obj_labels", obj_labels)
            matched_label = inputs.pop("matched_label", matched_label)
            ans = inputs.pop("ans", ans)

        lxmert_output = self.lxmert(
            inputs,
            visual_feats=visual_feats,
            visual_pos=visual_pos,
            attention_mask=attention_mask,
            visual_attention_mask=visual_attention_mask,
            token_type_ids=token_type_ids,
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
            else tf.constant(0.0)
        )
        losses = ()
        if masked_lm_labels is not None and self.task_mask_lm:
            masked_lm_loss = self.loss_fcts["ce"](
                tf.reshape(masked_lm_labels, [-1]),
                tf.reshape(lang_prediction_scores, [-1, self.config.vocab_size]),
            )
            total_loss += masked_lm_loss
            losses += (masked_lm_loss,)
        if matched_label is not None and self.task_matched:
            matched_loss = self.loss_fcts["ce"](
                tf.reshape(matched_label, [-1]),
                tf.reshape(cross_relationship_score, [-1, 2]),
            )
            total_loss += matched_loss
            losses += (matched_loss,)
        if obj_labels is not None and self.task_obj_predict:
            total_visn_loss = 0.0
            visn_prediction_scores_dict = self.obj_predict_head(visual_output)
            for key, key_info in self.visual_losses.items():
                label, mask_conf = obj_labels[key]
                output_dim = key_info["num"]
                loss_fct_name = key_info["loss"]
                label_shape = key_info["shape"]
                weight = self.visual_loss_normalizer
                visn_loss_fct = self.loss_fcts[loss_fct_name]
                visn_prediction_scores = visn_prediction_scores_dict[key]
                visn_loss = visn_loss_fct(
                    tf.reshape(label, label_shape),
                    tf.reshape(visn_prediction_scores, [-1, output_dim]),
                )

                if visn_loss.ndim > 1:  # Regression Losses
                    visn_loss = tf.reduce_mean(visn_loss)
                visn_loss = tf.reduce_mean(visn_loss * tf.cast(tf.reshape(mask_conf, [-1]), visn_loss.dtype)) * weight
                total_visn_loss += visn_loss
                losses += (visn_loss,)
            total_loss += total_visn_loss
        if ans is not None and self.task_qa:
            answer_loss = self.loss_fcts["ce"](
                tf.reshape(ans, [-1]), tf.reshape(answer_score, [-1, self.num_qa_labels])
            )
            # exclude "*2" here to match the effect of QA losses.
            # Previous: (loss *0) for 6 epochs, (loss *2) for 6 epochs.   (Used 10 instead of 6 in EMNLP paper)
            # Now     : (loss *1) for 12 epochs
            #
            # * 2       # Multiply by 2 because > half of the data will not have label
            total_loss += answer_loss
            losses += (answer_loss,)
        # return total_loss, tf.stack(losses)[tf.new_axis, ...], answer_score.detach()

        if not return_dict:
            output = (
                lang_prediction_scores,
                cross_relationship_score,
                answer_score,
            ) + lxmert_output[3:]
            return ((total_loss,) + output) if total_loss is not None else output

        return TFLxmertForPreTrainingOutput(
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
