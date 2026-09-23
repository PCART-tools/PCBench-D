    def __init__(self, tokenizer: PreTrainedTokenizer, file_dir: str, block_size: int):
        assert os.path.isdir(file_dir)
        logger.info(f"Creating features from dataset file folder at {file_dir}")
        self.examples = []
        # TODO: randomness could apply a random seed, ex. rng = random.Random(random_seed)
        # file path looks like ./dataset/wiki_1, ./dataset/wiki_2
        for file_name in os.listdir(file_dir):
            file_path = os.path.join(file_dir, file_name)
            assert os.path.isfile(file_path)
            article_open = False
            with open(file_path, encoding="utf-8") as f:
                original_lines = f.readlines()
                article_lines = []
                for line in original_lines:
                    if "<doc id=" in line:
                        article_open = True
                    elif "</doc>" in line:
                        article_open = False
                        document = [
                            tokenizer.convert_tokens_to_ids(tokenizer.tokenize(line))
                            for line in article_lines[1:]
                            if (len(line) > 0 and not line.isspace())
                        ]

                        examples = self.create_examples_from_document(document, block_size, tokenizer)
                        self.examples.extend(examples)
                        article_lines = []
                    else:
                        if article_open:
                            article_lines.append(line)

        logger.info("Dataset parse finished.")
