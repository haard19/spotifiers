import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

class Model:

    def __init__(self):
        self.final = pd.read_csv('../datasets/final/final.csv')
        self.metadata = pd.read_csv('../datasets/final/metadata.csv')
        self.final = shuffle(self.final)
        self.model = None
        self.Y = None

    def fit(self, df, algo, flag=0):
        if flag:
            algo.fit(df)
        else:
            algo.partial_fit(df)          
        df['label'] = algo.labels_
        return (df, algo)

    def predict(self, t, Y):
        y_pred = t[1].predict(Y)
        mode = pd.Series(y_pred).mode()
        return t[0][t[0]['label'] == mode.loc[0]]

    def getData(self, recommendations, meta, Y):
        dat = []
        for i in Y['track_id']:
            dat.append(i)
        genre_mode = meta.loc[dat]['genre'].mode()
        artist_mode = meta.loc[dat]['artist_name'].mode()
        return meta[meta['genre'] == genre_mode.iloc[0]], meta[meta['artist_name'] == artist_mode.iloc[0]], meta.loc[recommendations['track_id']]

    def train(self, ratio):
        split = round(self.final.shape[0]*(ratio/100))
        X = self.final.loc[[i for i in range(0, split)]]
        self.Y = self.final.loc[[i for i in range(split, self.final.shape[0])]]
        X = shuffle(X)
        self.Y = shuffle(self.Y)
        self.metadata = self.metadata.set_index('track_id')

        kmeans = KMeans(n_clusters=6)
        self.model = self.fit(X, kmeans, 1)

    def recommend(self):
        recommendations = self.predict(self.model, self.Y)
        output = self.getData(recommendations, self.metadata, self.Y)
        genre_recommend, artist_name_recommend, mixed_recommend = output[0], output[1], output[2]
        # mixed_recommend.apply(lambda x: x.str.strip())
        return json.loads(json.dumps(mixed_recommend[:25].to_json(orient="records")))