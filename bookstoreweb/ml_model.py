import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstoreweb.settings')
django.setup()

from webapp.models import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.linear_model import Ridge
import pickle

def query_to_vct_features():
    # Get all tag name
    tag_queryset = Tag.objects.all().values()
    tags = [tag['tag'] for tag in tag_queryset]

    # Get all book, book_id
    book_queryset = Book.objects.all()
    book_id = [book.item_id for book in book_queryset]

    # Get all user_id
    user_queryset = UserAccount.objects.all().values('id')
    user_df = pd.DataFrame.from_records(user_queryset)
    user_id_to_index = {user_id: index for index, user_id in enumerate(user_df['id'])}

    # Make binary_tag DataFrame of books, 1 if book has this tag, otherwise 0
    binary_df = pd.DataFrame(0, index=range(len(set(book_id))), columns=['book_id'] + tags)
    binary_df['book_id'] = book_id
    book_id_to_index = {book_id: index for index, book_id in enumerate(binary_df['book_id'])}

    for book in book_queryset:
        tags_of_book = book.book_tags.values()
        index = book_id_to_index[book.item_id]
        for tg in tags_of_book:
            binary_df.at[index, tg['tag']] = 1

    # Make features vector by Tfidf
    X_train_counts = binary_df.iloc[:, -727:] # 727 features
    transformer = TfidfTransformer(smooth_idf=True, norm ='l2')
    tfidf = transformer.fit_transform(X_train_counts.values.tolist()).toarray()

    return tfidf, book_id_to_index, user_id_to_index

def get_items_rated_by_user(user_id):
    rate_query_set = Rating.objects.filter(user = user_id).values('item', 'rating')
    if len(rate_query_set) != 0:
        rate_df = pd.DataFrame.from_records(rate_query_set)
    else: rate_df = pd.DataFrame(columns= ['item', 'rating'])
    return (rate_df['item'], rate_df['rating']) 

def training_model():
    tfidf, book_id_to_index, user_id_to_index = query_to_vct_features()
    num_users = UserAccount.objects.count()

    d = tfidf.shape[1]
    W = np.zeros((d, num_users))
    b = np.zeros((1, num_users))

    for n in range(num_users):
        user_id = list(user_id_to_index.keys())[n]
        user_idx = user_id_to_index[user_id]
        ids, scores = get_items_rated_by_user(user_id)
        if len(ids) == 0:
            continue
        ids = ids.map(book_id_to_index)
        clf = Ridge(alpha=0.01, fit_intercept=True)
        Xhat = tfidf[ids, :]
        clf.fit(Xhat, scores)
        W[:, user_idx] = clf.coef_
        b[0, user_idx] = clf.intercept_

    with open('./webapp/model_params.pkl', 'wb') as f:
        pickle.dump({'W': W, 'b': b}, f)

def predict_rating(user_id, item_id, tfidf, W, b, book_id_to_index, user_id_to_index):
    user_idx = user_id_to_index[user_id]
    item_idx = book_id_to_index[item_id]
    return tfidf[item_idx, :].dot(W[:, user_idx]) + b[0, user_idx]

def recommend_books(user_id, num_recommendations):
    rated_books, true_ratings = get_items_rated_by_user(user_id)
    tfidf, book_id_to_index, user_id_to_index = query_to_vct_features()

    all_books = set(book_id_to_index)
    unrated_books = list(all_books - set(rated_books))

    with open('./webapp/model_params.pkl', 'rb') as f:
        params = pickle.load(f)
    W = params['W']
    b = params['b']
    
    predictions = [(item_id, predict_rating(user_id, item_id, tfidf, W, b, book_id_to_index, user_id_to_index)) for item_id in unrated_books]
    predictions.sort(key=lambda x: x[1], reverse=True)
    recommendations = predictions[:num_recommendations]
    books = []
    for rec in recommendations:
        books.append(rec[0])
    return books

if __name__ == '__main__':
    training_model()