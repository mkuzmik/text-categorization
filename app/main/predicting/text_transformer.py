import dependency_injector.containers as containers
import dependency_injector.providers as providers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class TextTransformer:
    def __init__(self):
        self.tfidf_transformer = TfidfTransformer()
        self.count_vect = CountVectorizer()

    def transform_tfidf(self, data):
        X_counts = self.count_vect.fit_transform(data)
        return self.tfidf_transformer.fit_transform(X_counts)

    def transform(self, test, train):
        transformed = self.transform_tfidf(test + train)
        return transformed[:len(test)], transformed[len(test):]


class TextTransformerContainer(containers.DeclarativeContainer):
    instance = providers.Singleton(TextTransformer)
