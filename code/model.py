import pandas as pd
import json
from sklearn.cluster import KMeans, MiniBatchKMeans, Birch
from sklearn.utils import shuffle

class Model:

    def __init__(self):
        self.final = pd.read_csv('../datasets/final/final.csv')
        self.metadata = pd.read_csv('../datasets/final/metadata.csv')
        self.metadata = self.metadata.set_index('track_id')
        self.final = shuffle(self.final)
        self.model = None
        self.Y = None
        self.X = None

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

    def train(self, ratio, model):
        split = round(self.final.shape[0]*(ratio/100))
        self.X = self.final.loc[[i for i in range(0, split)]]
        self.Y = self.final.loc[[i for i in range(split, self.final.shape[0])]]
        self.X = shuffle(self.X)
        self.Y = shuffle(self.Y)

        if model=="KMeans":
            kmeans = KMeans(n_clusters=6)
            self.model = self.fit(self.X, kmeans, 1)
        elif model=="MiniBatchKMeans":
            self.model = MiniBatchKMeans(n_clusters = 6)
            mini = self.model
            if "label" in self.X.columns:
                self.X.drop('label', axis=1, inplace=True)
            split = self.X.shape[0]//3
            part_1, part_2, part_3 = self.X.iloc[0: split], self.X.iloc[split:split*2], self.X.iloc[split*2:split*3]
            for i in [part_1, part_2, part_3]:
                t = self.fit(i, mini)
                mini = t[1]
                i = t[0]
            self.X = pd.concat([part_1, part_2, part_3])
            self.model = t
        else:
            self.model = Birch(n_clusters = 6)
            mini = self.model 
            if "label" in self.X.columns:
                self.X.drop('label', axis=1, inplace=True)
            split = self.X.shape[0]//3 # shape of the data frame
            part_1, part_2, part_3 = self.X.iloc[0: split], self.X.iloc[split:split*2], self.X.iloc[split*2:split*3]#dividing into three parts for fitting the model
            for i in [part_1, part_2, part_3]:
                t = self.fit(i, mini)
                mini = t[1]
                i = t[0]
            self.X = pd.concat([part_1, part_2, part_3])#grouping all parts together after fitting
            self.model = t
        

    def recommend(self):# recommends the music data
        recommendations = self.predict(self.model, self.Y)
        output = self.getData(recommendations, self.metadata, self.Y)
        genre_recommend, artist_name_recommend, mixed_recommend = output[0], output[1], output[2]
        return json.loads(json.dumps(mixed_recommend[:25].to_json(orient="records")))    