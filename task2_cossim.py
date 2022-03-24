import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import random


def cossim(title):
    train_df = pd.read_csv('train_clean_cossim.csv')
    train_df = train_df.rename(columns={'Unnamed: 0': 'index'})

    def get_important_features(data):
        important_features = []

        for i in range(data.shape[0]):
            temp = ""
            for column in data:
                temp = temp + data[column][i]
            important_features.append(temp)
        return important_features

    temp = train_df.iloc[:, 2:-1]
    train_df['important_features'] = get_important_features(temp)
    cm = CountVectorizer().fit_transform(train_df['important_features'])
    cs = cosine_similarity(cm)
    car_selected = title
    car_id = train_df[train_df.title == car_selected]['index'].values[0]
    scores = list(enumerate(cs[car_id]))
    sorted_scores = sorted(scores,key = lambda x:x[1],reverse = True)
    sorted_scores = sorted_scores[1:]
    all_car = []
    all_car_id = []
    for item in sorted_scores:
        car_listing = train_df[train_df.index == item[0]]['listing_id'].values[0]
        temp = train_df.loc[train_df['listing_id'] == car_listing, 'title'].iloc[0]
        if temp not in all_car:
            all_car.append(temp)
            all_car_id.append(car_listing)
        if len(all_car) ==10:
            break
    suggested_listing = random.sample(all_car_id, 5)

    return suggested_listing