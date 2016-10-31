import json
import cPickle as pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

"""
    Takes labelled data, converts them to feature vectors and trains a classifier
"""
class ModelTrainer():

    def __init__(self, inPath, outPath):
        self.inPath = inPath
        self.outPath = outPath

        # feature vectorizer
        self.vectorizer = TfidfVectorizer()

    def run(self):
        # load json
        with open(self.inPath) as f:
            data = json.load(f)

        # list(sentence)
        allSentences = []

        # list(label -> sentenceCount)
        labels = []

        # construct the data set
        for d in data:
            label = d['label']
            sentences = d['sentences']
            if sentences and label:
                allSentences.extend(sentences)
                for i in xrange(len(sentences)):
                    labels.append(label)

            print('Processing: ', label)

        # import into vectorizer
        features = self.vectorizer.fit_transform(allSentences)

        # train the model
        print('Training model...')
        clf = KNeighborsClassifier(15, 'distance')
        clf.fit(features.toarray(), labels)

        # save the model
        #print('Pickling...')
        #pickle.dump(clf, open(self.outPath, "wb"))

        return clf


if __name__ == '__main__':
    trainer = ModelTrainer(inPath='clean.json', outPath='model.pickle')
    trainer.run()
