from app.main.inshorts_extracting import InshortsDfDownloader
from app.main.text_processing import TextProcessingChain
from app.main.text_transforming import TextTransformer
from sklearn.naive_bayes import MultinomialNB


class Predicter:
    def __init__(self, categories, learning_set_size):
        self.inshorts_downloader = InshortsDfDownloader()
        self.text_processor = TextProcessingChain()
        self.text_transformer = TextTransformer()

        self.data_set = self.inshorts_downloader.extract_inshorts(categories, learning_set_size)

    def predict(self, text):
        self.data_set.content = self.text_processor.preprocess_series(self.data_set.content)
        preprocessed_text = self.text_processor.preprocess_text(text)
        transformed_text, X = self.text_transformer.transform([preprocessed_text], self.data_set.content.tolist())
        y = self.data_set.label.tolist()
        model = MultinomialNB()
        model.fit(X, y)
        predicted = model.predict(transformed_text)
        return predicted.item()
