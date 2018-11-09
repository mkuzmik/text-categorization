class PandasUtil:

    @staticmethod
    def shuffle(data_frame):
        return data_frame.sample(frac=1)

    @staticmethod
    def split_df(df):
        return df.content.tolist(), df.label.tolist()