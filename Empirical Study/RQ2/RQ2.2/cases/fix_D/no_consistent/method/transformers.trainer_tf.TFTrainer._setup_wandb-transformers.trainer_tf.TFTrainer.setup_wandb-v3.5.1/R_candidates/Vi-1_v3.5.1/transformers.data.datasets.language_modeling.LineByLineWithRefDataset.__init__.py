    def __init__(self, tokenizer: PreTrainedTokenizer, file_path: str, block_size: int, ref_path: str):
        warnings.warn(
            DEPRECATION_WARNING.format(
                "https://github.com/huggingface/transformers/blob/master/examples/language-modeling/run_mlm_wwm.py"
            ),
            FutureWarning,
        )
        assert os.path.isfile(file_path), f"Input file path {file_path} not found"
        assert os.path.isfile(ref_path), f"Ref file path {file_path} not found"
        # Here, we do not cache the features, operating under the assumption
        # that we will soon use fast multithreaded tokenizers from the
        # `tokenizers` repo everywhere =)
        logger.info("Creating features from dataset file at %s", file_path)
        logger.info("Use ref segment results at %s", ref_path)
        with open(file_path, encoding="utf-8") as f:
            data = f.readlines()  # use this method to avoid delimiter '\u2029' to split a line
        data = [line.strip() for line in data if len(line) > 0 and not line.isspace()]
        # Get ref inf from file
        with open(ref_path, encoding="utf-8") as f:
            ref = [json.loads(line) for line in f.read().splitlines() if (len(line) > 0 and not line.isspace())]
        assert len(data) == len(ref)

        batch_encoding = tokenizer(data, add_special_tokens=True, truncation=True, max_length=block_size)
        self.examples = batch_encoding["input_ids"]
        self.examples = [{"input_ids": torch.tensor(e, dtype=torch.long)} for e in self.examples]

        n = len(self.examples)
        for i in range(n):
            self.examples[i]["chinese_ref"] = torch.tensor(ref[i], dtype=torch.long)
