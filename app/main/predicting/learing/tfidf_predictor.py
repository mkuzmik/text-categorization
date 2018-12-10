from app.main.predicting.pandas_util import PandasUtil
from app.main.tools import logging

logger = logging.get_logger('TfidfPredictor')


class TfidfPredictor(object):
    def __init__(self, repository, text_processor, text_transformer, model):
        self.repository = repository
        self.text_processor = text_processor
        self.text_transformer = text_transformer
        self.model = model

    def predict(self, text, dataset_size):
        X, y, transformed_input = self.prepare_data(text, dataset_size)
        model = self.model
        logger.info('Learning model %s with TFIDF transformed data', self.model.__class__.__name__)
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
        items = self.repository.scan()
        data_set = PandasUtil.to_df(items)
        data_set = PandasUtil.shuffle(data_set)
        return data_set.head(dataset_size)
