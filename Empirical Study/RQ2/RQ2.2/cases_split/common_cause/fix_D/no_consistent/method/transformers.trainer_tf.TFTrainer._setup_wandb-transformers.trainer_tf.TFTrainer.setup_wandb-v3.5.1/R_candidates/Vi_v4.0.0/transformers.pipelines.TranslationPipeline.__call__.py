    def __call__(
        self, *args, return_tensors=False, return_text=True, clean_up_tokenization_spaces=False, **generate_kwargs
    ):
        r"""
        Translate the text(s) given as inputs.

        Args:
            args (:obj:`str` or :obj:`List[str]`):
                Texts to be translated.
            return_tensors (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not to include the tensors of predictions (as token indices) in the outputs.
            return_text (:obj:`bool`, `optional`, defaults to :obj:`True`):
                Whether or not to include the decoded texts in the outputs.
            clean_up_tokenization_spaces (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not to clean up the potential extra spaces in the text output.
            generate_kwargs:
                Additional keyword arguments to pass along to the generate method of the model (see the generate method
                corresponding to your framework `here <./model.html#generative-models>`__).

        Return:
            A list or a list of list of :obj:`dict`: Each result comes as a dictionary with the following keys:

            - **translation_text** (:obj:`str`, present when ``return_text=True``) -- The translation.
            - **translation_token_ids** (:obj:`torch.Tensor` or :obj:`tf.Tensor`, present when ``return_tensors=True``)
              -- The token ids of the translation.
        """
        assert return_tensors or return_text, "You must specify return_tensors=True or return_text=True"

        prefix = self.model.config.prefix if self.model.config.prefix is not None else ""

        if isinstance(args[0], list):
            assert (
                self.tokenizer.pad_token_id is not None
            ), "Please make sure that the tokenizer has a pad_token_id when using a batch input"
            args = ([prefix + text for text in args[0]],)
            padding = True

        elif isinstance(args[0], str):
            args = (prefix + args[0],)
            padding = False
        else:
            raise ValueError(
                " `documents[0]`: {} have the wrong format. The should be either of type `str` or type `list`".format(
                    args[0]
                )
            )

        with self.device_placement():
            inputs = self._parse_and_tokenize(*args, padding=padding)

            if self.framework == "pt":
                inputs = self.ensure_tensor_on_device(**inputs)
                input_length = inputs["input_ids"].shape[-1]

            elif self.framework == "tf":
                input_length = tf.shape(inputs["input_ids"])[-1].numpy()

            max_length = generate_kwargs.get("max_length", self.model.config.max_length)
            if input_length > 0.9 * max_length:
                logger.warning(
                    "Your input_length: {} is bigger than 0.9 * max_length: {}. You might consider increasing your max_length manually, e.g. translator('...', max_length=400)".format(
                        input_length, max_length
                    )
                )

            translations = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                **generate_kwargs,
            )
            results = []
            for translation in translations:
                record = {}
                if return_tensors:
                    record["translation_token_ids"] = translation
                if return_text:
                    record["translation_text"] = self.tokenizer.decode(
                        translation,
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                    )
                results.append(record)
            return results
