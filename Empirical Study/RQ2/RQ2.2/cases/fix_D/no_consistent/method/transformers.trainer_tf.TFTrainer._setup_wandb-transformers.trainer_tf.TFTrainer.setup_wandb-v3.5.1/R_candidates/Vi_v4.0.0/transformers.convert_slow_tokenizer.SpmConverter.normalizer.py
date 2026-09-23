    def normalizer(self, proto):
        precompiled_charsmap = proto.normalizer_spec.precompiled_charsmap
        return normalizers.Precompiled(precompiled_charsmap)
