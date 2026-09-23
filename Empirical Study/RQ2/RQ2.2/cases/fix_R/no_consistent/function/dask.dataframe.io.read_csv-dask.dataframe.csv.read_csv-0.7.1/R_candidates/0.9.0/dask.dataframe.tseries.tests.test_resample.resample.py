    def resample(df, freq, how='mean', **kwargs):
        return df.resample(freq, how=how, **kwargs)
