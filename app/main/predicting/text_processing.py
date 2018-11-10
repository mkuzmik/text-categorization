import re
import unicodedata
from functools import reduce

import dependency_injector.containers as containers
import dependency_injector.providers as providers
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.toktok import ToktokTokenizer


class TextProcessor:

    def __init__(self):
        self.tokenizer = ToktokTokenizer()
        self.lemmatizer = WordNetLemmatizer()
        self.stopword_list = nltk.corpus.stopwords.words('english')

    def remove_accented_chars(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def apply_on(self, collection, fun):
        mapped = list(map(lambda x: (fun(x), 1 if fun(x) != x else 0), collection))
        is_changed = list(map(lambda x: x[1], mapped))
        changed_count = reduce(lambda x, y: x + y, is_changed)
        collection = list(map(lambda x: x[0], mapped))
        return collection, changed_count

    def remove_special_characters(self, text, remove_digits=True):
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        text = re.sub(pattern, '', text)
        return text

    def lemmatize(self, text):
        text = ' '.join([self.lemmatizer.lemmatize(word) for word in text.split(' ')])
        return text

    def remove_stopwords(self, text, is_lower_case=False):
        tokens = self.tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in self.stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in self.stopword_list]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text


class TextProcessingChain:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.applies = [
            lambda s: s.lower(),
            self.text_processor.remove_accented_chars,
            self.text_processor.remove_special_characters,
            self.text_processor.lemmatize,
            self.text_processor.remove_stopwords
        ]

    def preprocess_text(self, text):
        return reduce(lambda res, fun: fun(res), self.applies, text)

    def preprocess_series(self, series):
        return reduce(lambda res, fun: list(map(fun, res)), self.applies, series)


class TextProcessingContainer(containers.DeclarativeContainer):
    instance = providers.Singleton(TextProcessingChain)
