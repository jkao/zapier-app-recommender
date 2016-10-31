import json
import nltk
import nltk.data
import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

"""
    Tokenizes and stems words
"""
class DataCleaner():

    def __init__(self, inPath='entries.json', outPath='clean.json'):
        self.inPath = inPath
        self.outPath = outPath

        self.lemmatizer = WordNetLemmatizer()
        self.sentenceTokenizer = nltk.data.load('/home/jeffk/nltk_data/tokenizers/punkt/english.pickle')

        self.stopwords = set(['send', 'do', 'include']).union(stopwords.words('english'))

    def stringToSentences(self, string0):
        return self.sentenceTokenizer.tokenize(string0)

    def normalizeString(self, string0, lemmatize=True):
        # strip and lower
        string1 = string0.encode('utf-8').strip().lower()

        # remove punctuation
        string2 = ' '.join(re.split('[' + string.punctuation + ']', string1))

        # tokenize
        tokens0 = nltk.word_tokenize(string2)

        # stop words
        tokens1 = [token for token in tokens0 if token not in self.stopwords]

        # stem
        tokens2 = tokens1
        if lemmatize:
            tokens2 = [self.lemmatizer.lemmatize(token.decode('utf-8')) for token in tokens1]

        return ' '.join(tokens2)

    def processStringField(self, acc, stringField, splitSentences=False):
        if stringField:
            # maybe split sentences
            sentences = [stringField]
            if splitSentences:
                sentences = self.stringToSentences(stringField)

            # sentences to tokens
            for s in self.stringToSentences(stringField):
                tokens = self.normalizeString(s)
                if tokens:
                    acc.append(tokens)

    def processStringListField(self, acc, data, field, splitSentences=False):
        if data[field]:
            for item in data[field]:
                self.processStringField(acc, item, splitSentences)

    def run(self):
        # load json
        with open(self.inPath) as f:
            data = json.load(f)

        normalizedEntries = []

        for entry in data:
            sentences = []

            self.processStringField(sentences, entry['serviceSummary'], splitSentences=True)
            #self.processStringListField(sentences, entry, 'zapRecipes', splitSentences=False)
            self.processStringListField(sentences, entry, 'triggersAndActionsStrings', splitSentences=True)
            self.processStringListField(sentences, entry, 'reviewStrings', splitSentences=True)
            self.processStringListField(sentences, entry, 'appCopySectionStrings', splitSentences=True)
            self.processStringField(sentences, entry['title'], splitSentences=False)
            self.processStringField(sentences, entry['appHeroIntro'], splitSentences=False)

            label = entry['appName']

            normalizedEntries.append({
                'label': label,
                'sentences': sentences,
            })

        # save json file
        with open(self.outPath, 'w') as f:
            json.dump(normalizedEntries, f)


if __name__ == '__main__':
    dc = DataCleaner(inPath='entries.json', outPath='clean.json')
    dc.run()
