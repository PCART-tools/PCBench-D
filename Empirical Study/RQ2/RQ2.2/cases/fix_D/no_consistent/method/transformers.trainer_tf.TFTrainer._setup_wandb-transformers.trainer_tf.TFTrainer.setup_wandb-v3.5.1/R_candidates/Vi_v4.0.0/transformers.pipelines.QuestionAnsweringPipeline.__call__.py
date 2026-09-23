    def __call__(self, *args, **kwargs):
        """
        Answer the question(s) given as inputs by using the context(s).

        Args:
            args (:class:`~transformers.SquadExample` or a list of :class:`~transformers.SquadExample`):
                One or several :class:`~transformers.SquadExample` containing the question and context.
            X (:class:`~transformers.SquadExample` or a list of :class:`~transformers.SquadExample`, `optional`):
                One or several :class:`~transformers.SquadExample` containing the question and context (will be treated
                the same way as if passed as the first positional argument).
            data (:class:`~transformers.SquadExample` or a list of :class:`~transformers.SquadExample`, `optional`):
                One or several :class:`~transformers.SquadExample` containing the question and context (will be treated
                the same way as if passed as the first positional argument).
            question (:obj:`str` or :obj:`List[str]`):
                One or several question(s) (must be used in conjunction with the :obj:`context` argument).
            context (:obj:`str` or :obj:`List[str]`):
                One or several context(s) associated with the question(s) (must be used in conjunction with the
                :obj:`question` argument).
            topk (:obj:`int`, `optional`, defaults to 1):
                The number of answers to return (will be chosen by order of likelihood).
            doc_stride (:obj:`int`, `optional`, defaults to 128):
                If the context is too long to fit with the question for the model, it will be split in several chunks
                with some overlap. This argument controls the size of that overlap.
            max_answer_len (:obj:`int`, `optional`, defaults to 15):
                The maximum length of predicted answers (e.g., only answers with a shorter length are considered).
            max_seq_len (:obj:`int`, `optional`, defaults to 384):
                The maximum length of the total sentence (context + question) after tokenization. The context will be
                split in several chunks (using :obj:`doc_stride`) if needed.
            max_question_len (:obj:`int`, `optional`, defaults to 64):
                The maximum length of the question after tokenization. It will be truncated if needed.
            handle_impossible_answer (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not we accept impossible as an answer.

        Return:
            A :obj:`dict` or a list of :obj:`dict`: Each result comes as a dictionary with the following keys:

            - **score** (:obj:`float`) -- The probability associated to the answer.
            - **start** (:obj:`int`) -- The start index of the answer (in the tokenized version of the input).
            - **end** (:obj:`int`) -- The end index of the answer (in the tokenized version of the input).
            - **answer** (:obj:`str`) -- The answer to the question.
        """
        # Set defaults values
        kwargs.setdefault("padding", "longest")
        kwargs.setdefault("topk", 1)
        kwargs.setdefault("doc_stride", 128)
        kwargs.setdefault("max_answer_len", 15)
        kwargs.setdefault("max_seq_len", 384)
        kwargs.setdefault("max_question_len", 64)
        kwargs.setdefault("handle_impossible_answer", False)

        if kwargs["topk"] < 1:
            raise ValueError("topk parameter should be >= 1 (got {})".format(kwargs["topk"]))

        if kwargs["max_answer_len"] < 1:
            raise ValueError("max_answer_len parameter should be >= 1 (got {})".format(kwargs["max_answer_len"]))

        # Convert inputs to features
        examples = self._args_parser(*args, **kwargs)
        if not self.tokenizer.is_fast:
            features_list = [
                squad_convert_examples_to_features(
                    examples=[example],
                    tokenizer=self.tokenizer,
                    max_seq_length=kwargs["max_seq_len"],
                    doc_stride=kwargs["doc_stride"],
                    max_query_length=kwargs["max_question_len"],
                    padding_strategy=PaddingStrategy.MAX_LENGTH.value,
                    is_training=False,
                    tqdm_enabled=False,
                )
                for example in examples
            ]
        else:
            features_list = []
            for example in examples:
                # Define the side we want to truncate / pad and the text/pair sorting
                question_first = bool(self.tokenizer.padding_side == "right")

                encoded_inputs = self.tokenizer(
                    text=example.question_text if question_first else example.context_text,
                    text_pair=example.context_text if question_first else example.question_text,
                    padding=kwargs["padding"],
                    truncation="only_second" if question_first else "only_first",
                    max_length=kwargs["max_seq_len"],
                    stride=kwargs["doc_stride"],
                    return_tensors="np",
                    return_token_type_ids=True,
                    return_overflowing_tokens=True,
                    return_offsets_mapping=True,
                    return_special_tokens_mask=True,
                )

                # When the input is too long, it's converted in a batch of inputs with overflowing tokens
                # and a stride of overlap between the inputs. If a batch of inputs is given, a special output
                # "overflow_to_sample_mapping" indicate which member of the encoded batch belong to which original batch sample.
                # Here we tokenize examples one-by-one so we don't need to use "overflow_to_sample_mapping".
                # "num_span" is the number of output samples generated from the overflowing tokens.
                num_spans = len(encoded_inputs["input_ids"])

                # p_mask: mask with 1 for token than cannot be in the answer (0 for token which can be in an answer)
                # We put 0 on the tokens from the context and 1 everywhere else (question and special tokens)
                p_mask = np.asarray(
                    [
                        [tok != 1 if question_first else 0 for tok in encoded_inputs.sequence_ids(span_id)]
                        for span_id in range(num_spans)
                    ]
                )

                # keep the cls_token unmasked (some models use it to indicate unanswerable questions)
                if self.tokenizer.cls_token_id:
                    cls_index = np.nonzero(encoded_inputs["input_ids"] == self.tokenizer.cls_token_id)
                    p_mask[cls_index] = 0

                features = []
                for span_idx in range(num_spans):
                    features.append(
                        SquadFeatures(
                            input_ids=encoded_inputs["input_ids"][span_idx],
                            attention_mask=encoded_inputs["attention_mask"][span_idx],
                            token_type_ids=encoded_inputs["token_type_ids"][span_idx],
                            p_mask=p_mask[span_idx].tolist(),
                            encoding=encoded_inputs[span_idx],
                            # We don't use the rest of the values - and actually
                            # for Fast tokenizer we could totally avoid using SquadFeatures and SquadExample
                            cls_index=None,
                            token_to_orig_map={},
                            example_index=0,
                            unique_id=0,
                            paragraph_len=0,
                            token_is_max_context=0,
                            tokens=[],
                            start_position=0,
                            end_position=0,
                            is_impossible=False,
                            qas_id=None,
                        )
                    )
                features_list.append(features)

        all_answers = []
        for features, example in zip(features_list, examples):
            model_input_names = self.tokenizer.model_input_names + ["input_ids"]
            fw_args = {k: [feature.__dict__[k] for feature in features] for k in model_input_names}

            # Manage tensor allocation on correct device
            with self.device_placement():
                if self.framework == "tf":
                    fw_args = {k: tf.constant(v) for (k, v) in fw_args.items()}
                    start, end = self.model(fw_args)[:2]
                    start, end = start.numpy(), end.numpy()
                else:
                    with torch.no_grad():
                        # Retrieve the score for the context tokens only (removing question tokens)
                        fw_args = {k: torch.tensor(v, device=self.device) for (k, v) in fw_args.items()}
                        start, end = self.model(**fw_args)[:2]
                        start, end = start.cpu().numpy(), end.cpu().numpy()

            min_null_score = 1000000  # large and positive
            answers = []
            for (feature, start_, end_) in zip(features, start, end):
                # Ensure padded tokens & question tokens cannot belong to the set of candidate answers.
                undesired_tokens = np.abs(np.array(feature.p_mask) - 1) & feature.attention_mask

                # Generate mask
                undesired_tokens_mask = undesired_tokens == 0.0

                # Make sure non-context indexes in the tensor cannot contribute to the softmax
                start_ = np.where(undesired_tokens_mask, -10000.0, start_)
                end_ = np.where(undesired_tokens_mask, -10000.0, end_)

                # Normalize logits and spans to retrieve the answer
                start_ = np.exp(start_ - np.log(np.sum(np.exp(start_), axis=-1, keepdims=True)))
                end_ = np.exp(end_ - np.log(np.sum(np.exp(end_), axis=-1, keepdims=True)))

                if kwargs["handle_impossible_answer"]:
                    min_null_score = min(min_null_score, (start_[0] * end_[0]).item())

                # Mask CLS
                start_[0] = end_[0] = 0.0

                starts, ends, scores = self.decode(start_, end_, kwargs["topk"], kwargs["max_answer_len"])
                if not self.tokenizer.is_fast:
                    char_to_word = np.array(example.char_to_word_offset)

                    # Convert the answer (tokens) back to the original text
                    # Score: score from the model
                    # Start: Index of the first character of the answer in the context string
                    # End: Index of the character following the last character of the answer in the context string
                    # Answer: Plain text of the answer
                    answers += [
                        {
                            "score": score.item(),
                            "start": np.where(char_to_word == feature.token_to_orig_map[s])[0][0].item(),
                            "end": np.where(char_to_word == feature.token_to_orig_map[e])[0][-1].item(),
                            "answer": " ".join(
                                example.doc_tokens[feature.token_to_orig_map[s] : feature.token_to_orig_map[e] + 1]
                            ),
                        }
                        for s, e, score in zip(starts, ends, scores)
                    ]
                else:
                    # Convert the answer (tokens) back to the original text
                    # Score: score from the model
                    # Start: Index of the first character of the answer in the context string
                    # End: Index of the character following the last character of the answer in the context string
                    # Answer: Plain text of the answer
                    question_first = bool(self.tokenizer.padding_side == "right")
                    enc = feature.encoding

                    # Sometimes the max probability token is in the middle of a word so:
                    # - we start by finding the right word containing the token with `token_to_word`
                    # - then we convert this word in a character span with `word_to_chars`
                    answers += [
                        {
                            "score": score.item(),
                            "start": enc.word_to_chars(
                                enc.token_to_word(s), sequence_index=1 if question_first else 0
                            )[0],
                            "end": enc.word_to_chars(enc.token_to_word(e), sequence_index=1 if question_first else 0)[
                                1
                            ],
                            "answer": example.context_text[
                                enc.word_to_chars(enc.token_to_word(s), sequence_index=1 if question_first else 0)[
                                    0
                                ] : enc.word_to_chars(enc.token_to_word(e), sequence_index=1 if question_first else 0)[
                                    1
                                ]
                            ],
                        }
                        for s, e, score in zip(starts, ends, scores)
                    ]

            if kwargs["handle_impossible_answer"]:
                answers.append({"score": min_null_score, "start": 0, "end": 0, "answer": ""})

            answers = sorted(answers, key=lambda x: x["score"], reverse=True)[: kwargs["topk"]]
            all_answers += answers

        if len(all_answers) == 1:
            return all_answers[0]
        return all_answers
