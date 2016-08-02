#import modules
import sys
import pickle
import numpy
import pandas
import sklearn

sys.path.append('c:\\Users\\Adam\\Udacity\\Intro_to_Machine_Learning\\ud120-projects\\tools')
from feature_format import featureFormat, targetFeatureSplit

sys.path.append('c:\\Users\\Adam\\Udacity\\Intro_to_Machine_Learning\\ud120-projects\\final_project')
from tester import test_classifier, dump_classifier_and_data

# load data
enron_data = pickle.load( \
    open("c:\\Users\\Adam\\Udacity\\Intro_to_Machine_Learning\\ud120-projects\\final_project\\final_project_dataset.pkl", "r"))
    
print '{} Enron employees'.format(len(enron_data.keys()))
print '{} features in dataset'.format(len(enron_data['SKILLING JEFFREY K'].keys()))
print enron_data['SKILLING JEFFREY K']

# convert to pandas dataframe

df = pandas.DataFrame.from_dict(enron_data, orient = 'index')
print df.head()

# Convert to numpy nan
df.replace(to_replace='NaN', value=numpy.nan, inplace=True)

# Count number of NaN's for columns
print df.isnull().sum()

# DataFrame dimensions
print df.shape

# examine missing data
df.loc[df.total_payments.isnull()]
df.loc[df.email_address.isnull()]

# drop 'TOTAL' and 'THE TRAVEL AGENCY IN THE PARK'
df_drop = df.drop(['TOTAL', 'THE TRAVEL AGENCY IN THE PARK'], axis = 0)
print df_drop.shape

# impute zeros to missing
df_imp = df_drop.replace(to_replace=numpy.nan, value=0)
print df_imp.shape
print df_imp.isnull().sum()

# summary
df_imp.describe()

# drop email address
df_noemailaddr = df_imp.drop(['email_address'], axis = 1)
df_noemailaddr.shape

# examine email features
print 'Most received emails: {}'.format(df_noemailaddr['to_messages'].max(axis = 0))
print 'Fewest received emails: {}'.format(df_noemailaddr['to_messages'].min(axis = 0))
print 'Most sent emails: {}'.format(df_noemailaddr['from_messages'].max(axis = 0))
print 'Fewest sent emails: {}'.format(df_noemailaddr['from_messages'].min(axis = 0))

# create new email features
poi_ratio = (df_noemailaddr['from_poi_to_this_person'] + df_noemailaddr['from_this_person_to_poi']) / \
(df_noemailaddr['from_messages'] + df_noemailaddr['to_messages'])
to_poi_ratio = (df_noemailaddr['from_this_person_to_poi']) / (df_noemailaddr['from_messages'])
from_poi_ratio = (df_noemailaddr['from_poi_to_this_person']) / (df_noemailaddr['to_messages'])

df_noemailaddr['poi_ratio'] = pandas.Series(poi_ratio)
df_noemailaddr['to_poi_ratio'] = pandas.Series(to_poi_ratio)
df_noemailaddr['from_poi_ratio'] = pandas.Series(from_poi_ratio)

df_emails = df_noemailaddr.drop(['to_messages', 'from_messages', 'from_this_person_to_poi', 'from_poi_to_this_person'], axis = 1)

# impute email ratios for people without emails as 0
df_final = df_emails.replace(to_replace=numpy.nan, value=0)

print df_final.head()
print df_final.shape
print df_final.loc['SKILLING JEFFREY K']

# split data into test and train sets
labels = df_final['poi']
features = df_final.drop('poi', axis = 1)
shuffle = sklearn.cross_validation.StratifiedShuffleSplit(labels, n_iter=10, test_size=0.1, random_state=1)

# Gaussian NB
from sklearn.naive_bayes import GaussianNB

gnb_clf = GaussianNB()
scores = sklearn.cross_validation.cross_val_score(gnb_clf, features, labels, cv = 5)
print 'Gaussian Naive Bayes: {}'.format(numpy.mean(scores))

# Random Forest
from sklearn.ensemble import RandomForestClassifier

random_forest_clf = RandomForestClassifier(n_estimators = 10)
scores = sklearn.cross_validation.cross_val_score(random_forest_clf, features, labels, cv = 5)
print 'Random Forest: {}'.format(numpy.mean(scores))

# AdaBoost
from sklearn.ensemble import AdaBoostClassifier

ab_clf = AdaBoostClassifier(n_estimators=100)
scores = sklearn.cross_validation.cross_val_score(ab_clf, features, labels, cv = 5)
print 'AdaBoost: {}'.format(numpy.mean(scores))

# optimize Random Forest parameters
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.grid_search import GridSearchCV

pipe_rf = Pipeline([('feat', SelectKBest()), ('clf', RandomForestClassifier())])

K = range(15, 19)
max_depth = [1, 3, 5, 10, 15, 25]
min_samples_split = [1, 2, 3, 4, 5]
n_estimators = [10, 20, 50] 
min_samples_leaf = [1,2,3,4]
criterion = ['gini', 'entropy']

param_grid_rf = [{'feat__k': K,
              'clf__max_depth': max_depth,
              'clf__min_samples_split': min_samples_split,
              'clf__n_estimators': n_estimators,
              'clf__min_samples_leaf': min_samples_leaf,
              'clf__criterion': criterion}]

gs_rf = GridSearchCV(estimator = pipe_rf, param_grid = param_grid_rf, cv = shuffle)
gs_rf.fit(features, labels)

print gs_rf.best_params_
print gs_rf.best_score_

# Random Forest features
features_list = list(features.columns)
feature_indices_rf = gs_rf.best_estimator_.named_steps['feat'].get_support(indices = True)
final_feature_list_rf = [features_list[i] for i in feature_indices_rf]

print final_feature_list_rf

print 'Feature scores: {}'.format(sorted(zip(features_list, gs_rf.best_estimator_.named_steps['feat'].scores_), 
                                         key = lambda x: x[1], reverse = True))
                                         
# optimize AdaBoost parameters
from sklearn.tree import DecisionTreeClassifier

pipe_ada = Pipeline([('feat', SelectKBest()),
                     ('clf', AdaBoostClassifier(DecisionTreeClassifier()))])

K = range(15, 19)
n_estimators_ada = [5, 10, 30, 40, 45, 50, 100, 150]
learning_rate = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 5]
algorithm = ['SAMME', 'SAMME.R']

param_grid_ada = [{'feat__k': K,
                  'clf__n_estimators': n_estimators_ada,
                  'clf__learning_rate': learning_rate,
                  'clf__algorithm': algorithm}]

gs_ada = GridSearchCV(estimator = pipe_ada, param_grid = param_grid_ada, cv = shuffle, scoring = 'f1_weighted')
gs_ada.fit(features, labels)

print gs_ada.best_params_
print gs_ada.best_score_

# AdaBoost features
features_list = list(features.columns)
feature_indices_ada = gs_ada.best_estimator_.named_steps['feat'].get_support(indices = True)
final_feature_list_ada = [features_list[i] for i in feature_indices_ada]

print 'Final feature list: {}'.format(final_feature_list_ada)
                                         
print 'Feature scores: {}'.format(sorted(zip(features_list, gs_ada.best_estimator_.named_steps['feat'].scores_), 
                                         key = lambda x: x[1], reverse = True))
                                         
# Random Forest validation
rf_best_clf = gs_rf.best_estimator_
list_cols = list(df_final.columns.values)
list_cols.remove('poi')
list_cols.insert(0, 'poi')
data = df_final[list_cols].fillna(0).to_dict(orient='records')
enron_data_sub = {}
counter = 0
for item in data:
    enron_data_sub[counter] = item
    counter += 1
    
test_classifier(rf_best_clf, enron_data_sub, list_cols)

# AdaBoost validation
ada_best_clf = gs_ada.best_estimator_
test_classifier(ada_best_clf, enron_data_sub, list_cols)

# Dump classifier and data
dump_classifier_and_data(ada_best_clf, enron_data_sub, list_cols)