import dependency_injector.containers as containers
import dependency_injector.providers as providers
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

    def predict(self, text):
        data_set = PandasUtil.to_df(self.repository.scan()['Items'])
        data_set.content = self.text_processor.preprocess_series(data_set.content)
        preprocessed_text = self.text_processor.preprocess_text(text)
        transformed_text, X = self.text_transformer.transform([preprocessed_text], data_set.content.tolist())
        y = data_set.label.tolist()
        model = MultinomialNB()
        model.fit(X, y)
        predicted = model.predict(transformed_text)
        return predicted.item()


class PredictorContainer(containers.DeclarativeContainer):
    instance = providers.Singleton(Predictor,
                                   repository=LabeledContentRepositoryContainer.instance(),
                                   text_processor=TextProcessingContainer.instance(),
                                   text_transformer=TextTransformerContainer.instance()
                                   )
