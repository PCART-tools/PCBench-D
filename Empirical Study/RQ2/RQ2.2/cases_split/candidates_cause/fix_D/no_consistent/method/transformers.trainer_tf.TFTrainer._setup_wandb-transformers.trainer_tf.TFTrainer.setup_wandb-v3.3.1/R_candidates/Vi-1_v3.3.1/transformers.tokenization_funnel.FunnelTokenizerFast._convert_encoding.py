    def _convert_encoding(self, encoding, **kwargs):
        # The fast tokenizer doesn't use the function above so we fix the cls token type id when decoding the fast
        # tokenzier output.
        encoding_dict = super()._convert_encoding(encoding, **kwargs)
        if "token_type_ids" in encoding_dict:
            # Note: we can't assume the <cls> token is in first position because left padding is a thing, hence the
            # double list comprehension.
            encoding_dict["token_type_ids"] = [
                [self.cls_token_type_id if i == self.cls_token_id else t for i, t in zip(input_ids, type_ids)]
                for input_ids, type_ids in zip(encoding_dict["input_ids"], encoding_dict["token_type_ids"])
            ]
        return encoding_dict
