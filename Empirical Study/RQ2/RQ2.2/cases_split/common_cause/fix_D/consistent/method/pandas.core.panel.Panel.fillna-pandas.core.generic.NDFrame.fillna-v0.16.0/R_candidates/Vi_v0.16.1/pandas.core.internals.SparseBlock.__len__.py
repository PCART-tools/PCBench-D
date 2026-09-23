    def __len__(self):
        try:
            return self.sp_index.length
        except:
            return 0
