    @add_start_docstrings_to_model_forward(XLM_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=XLMForQuestionAnsweringOutput, config_class=_CONFIG_FOR_DOC)
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        langs=None,
        token_type_ids=None,
        position_ids=None,
        lengths=None,
        cache=None,
        head_mask=None,
        inputs_embeds=None,
        start_positions=None,
        end_positions=None,
        is_impossible=None,
        cls_index=None,
        p_mask=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        r"""
        start_positions (:obj:`torch.LongTensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for position (index) of the start of the labelled span for computing the token classification loss.
            Positions are clamped to the length of the sequence (:obj:`sequence_length`). Position outside of the
            sequence are not taken into account for computing the loss.
        end_positions (:obj:`torch.LongTensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for position (index) of the end of the labelled span for computing the token classification loss.
            Positions are clamped to the length of the sequence (:obj:`sequence_length`). Position outside of the
            sequence are not taken into account for computing the loss.
        is_impossible (``torch.LongTensor`` of shape ``(batch_size,)``, `optional`):
            Labels whether a question has an answer or no answer (SQuAD 2.0)
        cls_index (``torch.LongTensor`` of shape ``(batch_size,)``, `optional`):
            Labels for position (index) of the classification token to use as input for computing plausibility of the
            answer.
        p_mask (``torch.FloatTensor`` of shape ``(batch_size, sequence_length)``, `optional`):
            Optional mask of tokens which can't be in answers (e.g. [CLS], [PAD], ...). 1.0 means token should be
            masked. 0.0 mean token is not masked.

        Returns:

        Example::

            >>> from transformers import XLMTokenizer, XLMForQuestionAnswering
            >>> import torch

            >>> tokenizer = XLMTokenizer.from_pretrained('xlm-mlm-en-2048')
            >>> model = XLMForQuestionAnswering.from_pretrained('xlm-mlm-en-2048', return_dict=True)

            >>> input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute", add_special_tokens=True)).unsqueeze(0)  # Batch size 1
            >>> start_positions = torch.tensor([1])
            >>> end_positions = torch.tensor([3])

            >>> outputs = model(input_ids, start_positions=start_positions, end_positions=end_positions)
            >>> loss = outputs.loss
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        transformer_outputs = self.transformer(
            input_ids,
            attention_mask=attention_mask,
            langs=langs,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            lengths=lengths,
            cache=cache,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        output = transformer_outputs[0]

        outputs = self.qa_outputs(
            output,
            start_positions=start_positions,
            end_positions=end_positions,
            cls_index=cls_index,
            is_impossible=is_impossible,
            p_mask=p_mask,
            return_dict=return_dict,
        )

        if not return_dict:
            return outputs + transformer_outputs[1:]

        return XLMForQuestionAnsweringOutput(
            loss=outputs.loss,
            start_top_log_probs=outputs.start_top_log_probs,
            start_top_index=outputs.start_top_index,
            end_top_log_probs=outputs.end_top_log_probs,
            end_top_index=outputs.end_top_index,
            cls_logits=outputs.cls_logits,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
