from app.main.inshorts_extracting import InshortsDfDownloader
from app.main.text_processing import TextProcessingChain
from app.main.text_transforming import TextTransformer


class Predicter:
    def __init__(self, categories, learning_set_size):
        self.inshorts_downloader = InshortsDfDownloader()
        self.text_processor = TextProcessingChain()
        self.text_transformer = TextTransformer()

        self.data_set = self.inshorts_downloader.extract_inshorts(categories, learning_set_size)

    def predict(self, text):
        # TODO implementation
        pass
