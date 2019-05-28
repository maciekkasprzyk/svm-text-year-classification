import datetime
import pickle
from pprint import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

import paths
from book import construct_list_of_books

def main():
    print("constructing list of books...")
    books = construct_list_of_books()

    texts_list = [book.text for book in books]
    labels = [book.label for book in books]

    # with open('data/preprocessed_texts.json', 'r') as file:
    #     texts_list = json.load(file)

    pipeline = Pipeline([("tfidf", TfidfVectorizer(max_df=0.5)),
                         ("svm", SVC(kernel="linear"))])

    parameters = {
        # 'tfidf__max_df': (0.5, 0.75, 1.0),
        # 'tfidf__max_features': (None, 50000),
        # 'tfidf__ngram_range': ((1, 2), (1, 1)),  # unigrams or bigrams
        # 'tfidf__use_idf': (True, False),
        # 'tfidf__norm': ('l1', 'l2'),

    }

    # x and y are commonly used names for data set and class labels
    x = texts_list
    y = labels

    print("len(x) ", len(x), "len(y) ", len(y))

    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size=0.25)

    grid_search = GridSearchCV(pipeline, parameters, cv=4, n_jobs=-1, verbose=10)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(x_train, y_train)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # y_pred = grid_search.predict(x_test)
    print("Test results: ", grid_search.score(x_test, y_test))
    print()

    with open(paths.last_grid_search_path + str(datetime.datetime.now()), "wb") as file:
        pickle.dump((grid_search, x_test, y_test), file)


if __name__ == '__main__':
    main()
