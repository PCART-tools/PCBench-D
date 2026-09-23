    def _send_frame(self, message, opcode):
        """Send a frame over the websocket with message as its payload."""
        if self._closing:
            ws_logger.warning('websocket connection is closing.')

        rsv = 0

        # Only compress larger packets (disabled)
        # Does small packet needs to be compressed?
        # if self.compress and opcode < 8 and len(message) > 124:
        if self.compress and opcode < 8:
            if not self._compressobj:
                self._compressobj = zlib.compressobj(wbits=-self.compress)

            message = self._compressobj.compress(message)
            message = message + self._compressobj.flush(
                zlib.Z_FULL_FLUSH if self.notakeover else zlib.Z_SYNC_FLUSH)
            if message.endswith(_WS_DEFLATE_TRAILING):
                message = message[:-4]
            rsv = rsv | 0x40

        msg_length = len(message)

        use_mask = self.use_mask
        if use_mask:
            mask_bit = 0x80
        else:
            mask_bit = 0

        if msg_length < 126:
            header = PACK_LEN1(0x80 | rsv | opcode, msg_length | mask_bit)
        elif msg_length < (1 << 16):
            header = PACK_LEN2(0x80 | rsv | opcode, 126 | mask_bit, msg_length)
        else:
            header = PACK_LEN3(0x80 | rsv | opcode, 127 | mask_bit, msg_length)
        if use_mask:
            mask = self.randrange(0, 0xffffffff)
            mask = mask.to_bytes(4, 'big')
            message = bytearray(message)
            _websocket_mask(mask, message)
            self.writer.write(header + mask + message)
            self._output_size += len(header) + len(mask) + len(message)
        else:
            if len(message) > MSG_SIZE:
                self.writer.write(header)
                self.writer.write(message)
            else:
                self.writer.write(header + message)

            self._output_size += len(header) + len(message)

        if self._output_size > self._limit:
            self._output_size = 0
            return self.stream.drain()

        return noop()
