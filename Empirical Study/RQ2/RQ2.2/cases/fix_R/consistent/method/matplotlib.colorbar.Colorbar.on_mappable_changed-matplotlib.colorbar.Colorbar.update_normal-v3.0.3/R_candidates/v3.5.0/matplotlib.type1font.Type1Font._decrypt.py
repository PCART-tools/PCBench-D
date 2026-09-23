    @staticmethod
    def _decrypt(ciphertext, key, ndiscard=4):
        """
        Decrypt ciphertext using the Type-1 font algorithm

        The algorithm is described in Adobe's "Adobe Type 1 Font Format".
        The key argument can be an integer, or one of the strings
        'eexec' and 'charstring', which map to the key specified for the
        corresponding part of Type-1 fonts.

        The ndiscard argument should be an integer, usually 4.
        That number of bytes is discarded from the beginning of plaintext.
        """

        key = _api.check_getitem({'eexec': 55665, 'charstring': 4330}, key=key)
        plaintext = []
        for byte in ciphertext:
            plaintext.append(byte ^ (key >> 8))
            key = ((key+byte) * 52845 + 22719) & 0xffff

        return bytes(plaintext[ndiscard:])
