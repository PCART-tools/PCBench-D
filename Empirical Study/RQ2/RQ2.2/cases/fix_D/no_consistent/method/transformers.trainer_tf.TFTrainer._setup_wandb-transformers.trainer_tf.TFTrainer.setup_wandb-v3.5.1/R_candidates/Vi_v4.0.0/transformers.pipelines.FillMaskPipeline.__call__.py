    def __call__(self, *args, targets=None, top_k: Optional[int] = None, **kwargs):
        """
        Fill the masked token in the text(s) given as inputs.

        Args:
            args (:obj:`str` or :obj:`List[str]`):
                One or several texts (or one list of prompts) with masked tokens.
            targets (:obj:`str` or :obj:`List[str]`, `optional`):
                When passed, the model will return the scores for the passed token or tokens rather than the top k
                predictions in the entire vocabulary. If the provided targets are not in the model vocab, they will be
                tokenized and the first resulting token will be used (with a warning).
            top_k (:obj:`int`, `optional`):
                When passed, overrides the number of predictions to return.

        Return:
            A list or a list of list of :obj:`dict`: Each result comes as list of dictionaries with the following keys:

            - **sequence** (:obj:`str`) -- The corresponding input with the mask token prediction.
            - **score** (:obj:`float`) -- The corresponding probability.
            - **token** (:obj:`int`) -- The predicted token id (to replace the masked one).
            - **token** (:obj:`str`) -- The predicted token (to replace the masked one).
        """
        inputs = self._parse_and_tokenize(*args, **kwargs)
        outputs = self._forward(inputs, return_tensors=True)

        results = []
        batch_size = outputs.shape[0] if self.framework == "tf" else outputs.size(0)

        if targets is not None:
            if len(targets) == 0 or len(targets[0]) == 0:
                raise ValueError("At least one target must be provided when passed.")
            if isinstance(targets, str):
                targets = [targets]

            targets_proc = []
            for target in targets:
                target_enc = self.tokenizer.tokenize(target)
                if len(target_enc) > 1 or target_enc[0] == self.tokenizer.unk_token:
                    logger.warning(
                        "The specified target token `{}` does not exist in the model vocabulary. Replacing with `{}`.".format(
                            target, target_enc[0]
                        )
                    )
                targets_proc.append(target_enc[0])
            target_inds = np.array(self.tokenizer.convert_tokens_to_ids(targets_proc))

        for i in range(batch_size):
            input_ids = inputs["input_ids"][i]
            result = []

            if self.framework == "tf":
                masked_index = tf.where(input_ids == self.tokenizer.mask_token_id).numpy()

                # Fill mask pipeline supports only one ${mask_token} per sample
                self.ensure_exactly_one_mask_token(masked_index)

                logits = outputs[i, masked_index.item(), :]
                probs = tf.nn.softmax(logits)
                if targets is None:
                    topk = tf.math.top_k(probs, k=top_k if top_k is not None else self.top_k)
                    values, predictions = topk.values.numpy(), topk.indices.numpy()
                else:
                    values = tf.gather_nd(probs, tf.reshape(target_inds, (-1, 1)))
                    sort_inds = tf.reverse(tf.argsort(values), [0])
                    values = tf.gather_nd(values, tf.reshape(sort_inds, (-1, 1))).numpy()
                    predictions = target_inds[sort_inds.numpy()]
            else:
                masked_index = torch.nonzero(input_ids == self.tokenizer.mask_token_id, as_tuple=False)

                # Fill mask pipeline supports only one ${mask_token} per sample
                self.ensure_exactly_one_mask_token(masked_index.numpy())

                logits = outputs[i, masked_index.item(), :]
                probs = logits.softmax(dim=0)
                if targets is None:
                    values, predictions = probs.topk(top_k if top_k is not None else self.top_k)
                else:
                    values = probs[..., target_inds]
                    sort_inds = list(reversed(values.argsort(dim=-1)))
                    values = values[..., sort_inds]
                    predictions = target_inds[sort_inds]

            for v, p in zip(values.tolist(), predictions.tolist()):
                tokens = input_ids.numpy()
                tokens[masked_index] = p
                # Filter padding out:
                tokens = tokens[np.where(tokens != self.tokenizer.pad_token_id)]
                result.append(
                    {
                        "sequence": self.tokenizer.decode(tokens),
                        "score": v,
                        "token": p,
                        "token_str": self.tokenizer.convert_ids_to_tokens(p),
                    }
                )

            # Append
            results += [result]

        if len(results) == 1:
            return results[0]
        return results
