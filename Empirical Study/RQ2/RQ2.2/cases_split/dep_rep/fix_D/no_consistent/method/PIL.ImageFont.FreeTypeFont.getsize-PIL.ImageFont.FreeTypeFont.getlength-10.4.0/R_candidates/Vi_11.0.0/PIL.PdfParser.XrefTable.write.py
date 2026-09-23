    def write(self, f: IO[bytes]) -> int:
        keys = sorted(set(self.new_entries.keys()) | set(self.deleted_entries.keys()))
        deleted_keys = sorted(set(self.deleted_entries.keys()))
        startxref = f.tell()
        f.write(b"xref\n")
        while keys:
            # find a contiguous sequence of object IDs
            prev: int | None = None
            for index, key in enumerate(keys):
                if prev is None or prev + 1 == key:
                    prev = key
                else:
                    contiguous_keys = keys[:index]
                    keys = keys[index:]
                    break
            else:
                contiguous_keys = keys
                keys = []
            f.write(b"%d %d\n" % (contiguous_keys[0], len(contiguous_keys)))
            for object_id in contiguous_keys:
                if object_id in self.new_entries:
                    f.write(b"%010d %05d n \n" % self.new_entries[object_id])
                else:
                    this_deleted_object_id = deleted_keys.pop(0)
                    check_format_condition(
                        object_id == this_deleted_object_id,
                        f"expected the next deleted object ID to be {object_id}, "
                        f"instead found {this_deleted_object_id}",
                    )
                    try:
                        next_in_linked_list = deleted_keys[0]
                    except IndexError:
                        next_in_linked_list = 0
                    f.write(
                        b"%010d %05d f \n"
                        % (next_in_linked_list, self.deleted_entries[object_id])
                    )
        return startxref
