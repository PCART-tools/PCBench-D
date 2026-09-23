    def create_examples_from_document(self, document, block_size, tokenizer, short_seq_prob=0.1):
        """Creates examples for a single document."""

        # Account for special tokens
        max_num_tokens = block_size - tokenizer.num_special_tokens_to_add(pair=True)

        # We *usually* want to fill up the entire sequence since we are padding
        # to `block_size` anyways, so short sequences are generally wasted
        # computation. However, we *sometimes*
        # (i.e., short_seq_prob == 0.1 == 10% of the time) want to use shorter
        # sequences to minimize the mismatch between pre-training and fine-tuning.
        # The `target_seq_length` is just a rough target however, whereas
        # `block_size` is a hard limit.
        target_seq_length = max_num_tokens
        if random.random() < short_seq_prob:
            target_seq_length = random.randint(2, max_num_tokens)

        # We DON'T just concatenate all of the tokens from a document into a long
        # sequence and choose an arbitrary split point because this would make the
        # next sentence prediction task too easy. Instead, we split the input into
        # segments "A" and "B" based on the actual "sentences" provided by the user
        # input.
        examples = []
        current_chunk = []  # a buffer stored current working segments
        current_length = 0
        i = 0
        while i < len(document):
            segment = document[i]  # get a segment
            if not segment:
                i += 1
                continue
            current_chunk.append(segment)  # add a segment to current chunk
            current_length += len(segment)  # overall token length
            # if current length goes to the target length or reaches the end of file, start building token a and b
            if i == len(document) - 1 or current_length >= target_seq_length:
                if current_chunk:
                    # `a_end` is how many segments from `current_chunk` go into the `A` (first) sentence.
                    a_end = 1
                    # if current chunk has more than 2 sentences, pick part of it `A` (first) sentence
                    if len(current_chunk) >= 2:
                        a_end = random.randint(1, len(current_chunk) - 1)
                    # token a
                    tokens_a = []
                    for j in range(a_end):
                        tokens_a.extend(current_chunk[j])

                    # token b
                    tokens_b = []
                    for j in range(a_end, len(current_chunk)):
                        tokens_b.extend(current_chunk[j])

                    if len(tokens_a) == 0 or len(tokens_b) == 0:
                        continue

                    # switch tokens_a and tokens_b randomly
                    if random.random() < 0.5:
                        is_next = False
                        tokens_a, tokens_b = tokens_b, tokens_a
                    else:
                        is_next = True

                    def truncate_seq_pair(tokens_a, tokens_b, max_num_tokens):
                        """Truncates a pair of sequences to a maximum sequence length."""
                        while True:
                            total_length = len(tokens_a) + len(tokens_b)
                            if total_length <= max_num_tokens:
                                break
                            trunc_tokens = tokens_a if len(tokens_a) > len(tokens_b) else tokens_b
                            assert len(trunc_tokens) >= 1
                            # We want to sometimes truncate from the front and sometimes from the
                            # back to add more randomness and avoid biases.
                            if random.random() < 0.5:
                                del trunc_tokens[0]
                            else:
                                trunc_tokens.pop()

                    truncate_seq_pair(tokens_a, tokens_b, max_num_tokens)
                    assert len(tokens_a) >= 1
                    assert len(tokens_b) >= 1

                    # add special tokens
                    input_ids = tokenizer.build_inputs_with_special_tokens(tokens_a, tokens_b)
                    # add token type ids, 0 for sentence a, 1 for sentence b
                    token_type_ids = tokenizer.create_token_type_ids_from_sequences(tokens_a, tokens_b)

                    example = {
                        "input_ids": torch.tensor(input_ids, dtype=torch.long),
                        "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
                        "sentence_order_label": torch.tensor(0 if is_next else 1, dtype=torch.long),
                    }
                    examples.append(example)
                current_chunk = []  # clear current chunk
                current_length = 0  # reset current text length
            i += 1  # go to next line
        return examples
