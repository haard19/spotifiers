import pandas as pd
import numpy as np

class Prepare():    

    def __init__(self):  #Constructor
        self.echonest = pd.read_csv('../datasets/transformed/echonest.csv')
        self.features = pd.read_csv('../datasets/transformed/features.csv')
        self.genres = pd.read_csv('../datasets/transformed/genres.csv')
        self.tracks = pd.read_csv('../datasets/transformed/tracks.csv')

    def convert_to_float(self, df, columns):  #Float Conversion
        for i in columns:
            df[i] = df[i].astype('float')
        return df

    def combine_two_rows(self, df):   #Combining 2 rows
        columns = list(df.columns)
        for i in range(0, 519):
            columns[i] = columns[i] + " " + df.iloc[0, i]
        return columns

    def combine_one_row(self, df): 
        columns = list(df.columns)
        for i in range(0, 53):
            if i == 0:
                columns[i] = df.iloc[0, i]
            else:
                columns[i] = columns[i] + " " + df.iloc[0, i]
        return columns

    def getList(self, cd):
        return cd[1:-1].split(',')

    def format_strings(self, x):
        if '-' in x:
            return ''.join(x.split('-'))
        if x.find('/'):
            return '|'.join(x.split('/'))
        return x

    def modifyString(self, serie, val):
        for i in range(0, val):
            if serie[i] == 'Old-Time / Historic':
                serie[i] = 'OldTime|Historic'
        return serie

    def prep(self):
        ## self.echonest data preparation
        self.echonest.drop(['echonest.8', 'echonest.9', 'echonest.15', 'echonest.16', 'echonest.17', 'echonest.18', 'echonest.19'], axis=1, inplace=True)
        self.echonest.drop(['echonest.10', 'echonest.11', 'echonest.12'], axis=1, inplace=True)
        self.echonest.drop(0, axis=0, inplace=True)
        self.echonest.iloc[0, 0] = self.echonest.iloc[1, 0]
        self.echonest.drop(2, axis=0, inplace=True)
        self.echonest.columns = self.echonest.iloc[0]
        self.echonest.drop(1, axis=0, inplace=True)
        self.echonest.reset_index(inplace=True)
        self.echonest.drop('index', inplace=True, axis=1)

        self.echonest = self.convert_to_float(self.echonest, set(self.echonest.columns) - set(['track_id', 'artist_name', 'release']))

        ## Feature data preparation
        self.features.iloc[0,0] = self.features.iloc[2, 0]
        self.features.drop(2, inplace=True)
        self.features.columns = self.combine_two_rows(self.features)
        self.features.drop([0, 1], inplace=True)
        self.features.reset_index(inplace=True)
        self.features.drop('index', axis=1, inplace=True)
        self.features = self.features.astype(dtype='float')
        self.features['feature track_id'] = self.features['feature track_id'].astype('int')

        ## Tracks data preparation
        self.tracks.iloc[0,0] = self.tracks.iloc[1, 0]
        self.tracks.drop(1, axis=0, inplace=True)
        self.tracks.columns = self.combine_one_row(self.tracks)
        self.tracks.drop(0, inplace=True)
        self.tracks.reset_index(inplace=True)
        self.tracks.drop(['index'], axis=1, inplace=True)

        track_title = pd.DataFrame(self.tracks['track.19 title'])
        track_title['track_id'] = self.tracks['track_id']

        self.tracks.drop(['album comments','album.1 date_created', 
                    'album.2 date_released', 'album.11 tracks', 
                    'album.9 tags', 'album.8 producer', 'album.3 engineer', 'album.6 information',
                    'artist active_year_begin', 'artist.1 active_year_end', 'artist.2 associated_labels',
                    'artist.3 bio','artist.4 comments','artist.5 date_created', 'artist.7 id',
                    'artist.8 latitude','artist.9 location','artist.10 longitude', 'artist.11 members',
                    'artist.13 related_projects', 'artist.14 tags','artist.15 website','artist.16 wikipedia_page',
                    'set.1 subset', 'track.1 comments', 'track.2 composer', 'track.3 date_created', 'track.4 date_recorded',
                    'track.10 information', 'track.13 license', 'track.15 lyricist', 'track.17 publisher', 'track.18 tags',
                    'track.19 title'], axis=1, inplace=True)

        self.tracks['album.10 title'].fillna(method='ffill', inplace=True)
        self.tracks.drop(['track.12 language_code', 'album.12 type'], axis=1, inplace=True)
        self.tracks.drop('track.9 genres_all', axis=1, inplace=True)

        for i in range(0, 106574):
            if type(self.tracks['track.7 genre_top'][i]) == float:
                genre_list = self.getList(str(self.tracks['track.8 genres'][i]))
                count = len(genre_list)
                title = ""
                for j in range(0, count):
                    title = title + str(self.genres['title'][j]) + str('|')
                self.tracks['track.7 genre_top'][i] = title

        ## Getting all the data together
        self.features.columns = ['track_id'] + list(self.features.columns[1:])
        self.echonest['track_id'] = self.echonest['track_id'].astype('int')
        self.tracks['track_id'] = self.tracks['track_id'].astype('int')
        self.features.sort_values(by='track_id', inplace=True)
        self.tracks.sort_values(by='track_id', inplace=True)
        self.echonest.sort_values(by='track_id', inplace=True)
        count = 0
        for i in range(0, 106574):
            if self.features['track_id'][i] == self.tracks['track_id'][i]:
                count += 1
            else:
                print(self.features['track_id'][i], self.tracks['track_id'][i])
        final = pd.concat([self.features, self.tracks.drop('track_id', axis=1)], axis=1)
        self.echonest.drop(['artist_name', 'release'], axis=1, inplace=True)
        final = self.echonest.merge(final, on='track_id')
        final.drop('track.8 genres', axis=1, inplace=True)

        final['track.7 genre_top'] = self.modifyString(final['track.7 genre_top'], 13129)
        final['track.7 genre_top'] = final['track.7 genre_top'].apply(self.format_strings)

        metadata = pd.DataFrame()
        metadata['track_id'] = final['track_id']
        track_title = track_title.set_index('track_id')
        track_title.index = [int(i) for i in track_title.index]
        metadata['album_title'] = final['album.10 title']
        metadata['artist_name'] = final['artist.12 name']
        metadata['genre'] = final['track.7 genre_top']
        metadata = metadata.set_index('track_id')
        metadata['track_title'] = track_title.loc[metadata.index]['track.19 title']

        final.drop('album.10 title', axis=1, inplace=True)
        final.drop('artist.12 name', axis=1, inplace=True)
        final.drop('set split', axis=1, inplace=True)

        genre_dummy = pd.DataFrame(data= np.zeros((13129, 163)), columns= list(self.genres['title'].unique()))
        genre_list = pd.Series(data= genre_dummy.columns)
        genre_list = self.modifyString(genre_list, 163)
        genre_list = genre_list.apply(self.format_strings)
        genre_dummy.columns= genre_list
        genre_list = list(genre_list)

        for i in range(0, 13129):
            if '|' in final['track.7 genre_top'][i]:
                divided_list = str(final['track.7 genre_top'][i]).split('|')
                count = len(divided_list)
                for j in range(0, count):
                    if divided_list[j] in genre_list:
                        location = genre_list.index(divided_list[j])
                        genre_dummy.iloc[i, location] = 1
            else:
                location = genre_list.index(final['track.7 genre_top'][i])
                genre_dummy.iloc[i, location] = 1

        final.drop(['track.7 genre_top'], axis= 1, inplace= True)
        final = pd.concat([final, genre_dummy], axis= 1)
            
        metadata.to_csv('../datasets/final/metadata.csv')
        final.to_csv('../datasets/final/final.csv')
