    def __call__(
        self, *documents, return_tensors=False, return_text=True, clean_up_tokenization_spaces=False, **generate_kwargs
    ):
        r"""
        Summarize the text(s) given as inputs.

        Args:
            documents (`str` or :obj:`List[str]`):
                One or several articles (or one list of articles) to summarize.
            return_text (:obj:`bool`, `optional`, defaults to :obj:`True`):
                Whether or not to include the decoded texts in the outputs
            return_tensors (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not to include the tensors of predictions (as token indices) in the outputs.
            clean_up_tokenization_spaces (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not to clean up the potential extra spaces in the text output.
            generate_kwargs:
                Additional keyword arguments to pass along to the generate method of the model (see the generate method
                corresponding to your framework `here <./model.html#generative-models>`__).

        Return:
            A list or a list of list of :obj:`dict`: Each result comes as a dictionary with the following keys:

            - **summary_text** (:obj:`str`, present when ``return_text=True``) -- The summary of the corresponding
              input.
            - **summary_token_ids** (:obj:`torch.Tensor` or :obj:`tf.Tensor`, present when ``return_tensors=True``) --
              The token ids of the summary.
        """
        assert return_tensors or return_text, "You must specify return_tensors=True or return_text=True"
        assert len(documents) > 0, "Please provide a document to summarize"

        prefix = self.model.config.prefix if self.model.config.prefix is not None else ""

        if isinstance(documents[0], list):
            assert (
                self.tokenizer.pad_token_id is not None
            ), "Please make sure that the tokenizer has a pad_token_id when using a batch input"

            documents = ([prefix + document for document in documents[0]],)
            padding = True

        elif isinstance(documents[0], str):
            documents = (prefix + documents[0],)
            padding = False
        else:
            raise ValueError(
                " `documents[0]`: {} have the wrong format. The should be either of type `str` or type `list`".format(
                    documents[0]
                )
            )

        with self.device_placement():
            inputs = self._parse_and_tokenize(*documents, padding=padding)

            if self.framework == "pt":
                inputs = self.ensure_tensor_on_device(**inputs)
                input_length = inputs["input_ids"].shape[-1]
            elif self.framework == "tf":
                input_length = tf.shape(inputs["input_ids"])[-1].numpy()

            min_length = generate_kwargs.get("min_length", self.model.config.min_length)
            if input_length < min_length // 2:
                logger.warning(
                    "Your min_length is set to {}, but you input_length is only {}. You might consider decreasing min_length manually, e.g. summarizer('...', min_length=10)".format(
                        min_length, input_length
                    )
                )

            max_length = generate_kwargs.get("max_length", self.model.config.max_length)
            if input_length < max_length:
                logger.warning(
                    "Your max_length is set to {}, but you input_length is only {}. You might consider decreasing max_length manually, e.g. summarizer('...', max_length=50)".format(
                        max_length, input_length
                    )
                )

            summaries = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                **generate_kwargs,
            )

            results = []
            for summary in summaries:
                record = {}
                if return_tensors:
                    record["summary_token_ids"] = summary
                if return_text:
                    record["summary_text"] = self.tokenizer.decode(
                        summary,
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                    )
                results.append(record)
            return results
