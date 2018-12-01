from sklearn.naive_bayes import MultinomialNB

from app.main.data.repository import LabeledContentRepositoryContainer
from app.main.predicting.pandas_util import PandasUtil
from app.main.predicting.text_processing import TextProcessingContainer
from app.main.predicting.text_transformer import TextTransformerContainer


class Predictor:
    def __init__(self, repository, text_processor, text_transformer):
        self.repository = repository
        self.text_processor = text_processor
        self.text_transformer = text_transformer

    def predict(self, text, dataset_size):
        X, y, transformed_input = self.prepare_data(text, dataset_size)
        model = MultinomialNB()
        model.fit(X, y)
        predicted = model.predict(transformed_input)
        return predicted.item()

    def prepare_data(self, text, dataset_size):
        data_set = self.get_dataset(dataset_size)
        data_set.content = self.text_processor.preprocess_series(data_set.content)
        preprocessed_text = self.text_processor.preprocess_text(text)
        transformed_text, X = self.text_transformer.transform([preprocessed_text], data_set.content.tolist())
        return X, data_set.label.tolist(), transformed_text

    def get_dataset(self, dataset_size):
        data_set = PandasUtil.to_df(self.repository.scan())
        data_set = PandasUtil.shuffle(data_set)
        return data_set.head(dataset_size)


class PredictorContainer(object):
    instance = Predictor(repository=LabeledContentRepositoryContainer.instance,
                         text_processor=TextProcessingContainer.instance,
                         text_transformer=TextTransformerContainer.instance)
