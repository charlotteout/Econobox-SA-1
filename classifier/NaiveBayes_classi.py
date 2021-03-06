from classifier.classifier_base import ClassifierBase
from classifier import models_store_path
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import _joblib
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
from preprocessing import TFIDF_preprocessing
from data import train_negative_location, train_positive_location, test_location
import numpy as np

class NaiveBayes_classi(ClassifierBase):
    """Naive Bayes classifier"""

    def __init__(self,
                 embedding_dimension,
                 name="ourNB"):
        super().__init__(embedding_dimension, name=name)
        self.history = None
        self.model = None

    def build(self, **kwargs):
        print("Building model")

        self.model = MultinomialNB(alpha=1.8)

    def train(self, x,y, **kwargs):
        print("in naive bayes train")
        print(x)
        print(y)
        self.history = self.model.fit(x,y)
        crossvalscore = cross_val_score(self.model, x, y, cv=5, scoring='f1')
        print(crossvalscore)

    def test(self, x,y, **kwargs):
        print("testing model")
        y_pred = self.model.predict(x)
        score =f1_score(y, y_pred)
        return(score)

    def make_predictions(self, x, save=True, **kwargs):
        print("Making predictions")
        print(x.shape)
        preds = self.model.predict_proba(x)
        print(preds)
        preds_classes = np.argmax(preds, axis=-1).astype("int")
        preds_classes[preds_classes == 0] = -1
        if save: self.save_predictions(preds_classes)

    def save(self, overwrite=True, **kwargs):
        print("Saving model")
        path = models_store_path+self.name
        pickle.dump(self, open(path, 'wb'))
        _joblib.dump(self.model, self.name)


    def load(self, **kwargs):
        print("Loading model")
        path = models_store_path+self.name
        self.model = _joblib.load(self.name)

