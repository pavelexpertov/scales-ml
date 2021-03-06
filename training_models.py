import pandas as pd
import sklearn
from sklearn import tree

# In [ ]
df = pd.read_csv('balance-scale.data', header=None, names=['C','LW','LD','RW','RD'])
df

# In [ ]
# Creating a list of records where the format is ['description', mean, std]
recording_list = []
# In [ ]
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

X = df.loc[:, ['LW','LD','RW','RD']]
y = df.loc[:, ['C']]

clf = DecisionTreeClassifier()
scores = cross_val_score(clf, X, y, cv=3)
print('With 3 cross_validation', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With 3 cross_validation DecisionTreeClassifier', scores.mean(), scores.std()])

clf = DecisionTreeClassifier()
scores = cross_val_score(clf, X, y, cv=5)
print('With 5 cross_validation', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With 5 cross_validation DecisionTreeClassifier', scores.mean(), scores.std()])

clf = DecisionTreeClassifier()
scores = cross_val_score(clf, X, y, cv=10)
print('With 10 cross_validation', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With 10 cross_validation DecisionTreeClassifier', scores.mean(), scores.std()])


# <markdown>
# It looks like that the mean of cross validation results is affected by the number of specified folds during cross validation. It means that the decision tree model gets more accurate as you feed it a lot more data.

# Let's look at the importance of the features.

# In [ ]
clf = DecisionTreeClassifier()
clf.fit(X, y)
clf.feature_importances_

# <markdown>
# It looks like that importances of the attributes are balanced out well with a difference between 1 to 3 percent. Thus it means that pretty much they are equal to each other.

# Even though the balanced class (i.e. 'B') is only 8% of the dataset, models still looks like to struggle to perform good on average even though the it would have trained on a large number of 'L' or 'R' classes.

# I need to look at other machine learning algorithms to see whether they perform better.

# In [ ]
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import numpy as np
enc_y = LabelEncoder()
enc_y.fit(np.ravel(y.to_numpy()))
encoded_y = enc_y.transform(np.ravel(y.to_numpy()))
clf = LogisticRegression(random_state=0)
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With LogisticRegression', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With LogisticRegression', scores.mean(), scores.std()])

# In [ ]
from sklearn.linear_model import SGDClassifier
clf = SGDClassifier(max_iter=1000, tol=1e-3)
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With SGDClassifier', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With SGDClassifier', scores.mean(), scores.std()])

# In [ ]
from sklearn.svm import SVC
clf = SVC(gamma='auto')
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With SVC', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With SVC', scores.mean(), scores.std()])

# In [ ]
from sklearn.svm import LinearSVC
clf = LinearSVC(max_iter=5000)
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With LinearSVC', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With LinearSVC', scores.mean(), scores.std()])

# In [ ]
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=200)
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With RandomForestClassifier', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With RandomForestClassifier', scores.mean(), scores.std()])

# In [ ]
from sklearn.naive_bayes import CategoricalNB
clf = CategoricalNB()
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With CategoricalNB', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With CategoricalNB', scores.mean(), scores.std()])

# In [ ]
from sklearn.neighbors import NearestCentroid
clf = NearestCentroid()
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With NearestCentroid', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With NearestCentroid', scores.mean(), scores.std()])

# In [ ]
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier()
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With KNeighborsClassifier', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With KNeighborsClassifier', scores.mean(), scores.std()])

# In [ ]
from sklearn.neighbors import RadiusNeighborsClassifier
clf = RadiusNeighborsClassifier(radius=2.0)
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With RadiusNeighborsClassifier', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With RadiusNeighborsClassifier', scores.mean(), scores.std()])

# In [ ]
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(max_iter=1200)
scores = cross_val_score(clf, X, encoded_y, cv=10)
print('With MLPClassifier', 'Mean:', scores.mean(), scores.std())
recording_list.append(['With MLPClassifier', scores.mean(), scores.std()])

# In [ ]
sorted_list = sorted(recording_list, key=lambda item: item[1], reverse=True)
for classifier, mean, std in sorted_list:
    print(classifier, 'Mean:', mean, 'std:', std)

# <markdown>
# After experimenting with 11 algorithms, it looks like a neural network type classifier wins the testing round.
#
# Now I need to perform two things:
#     - I will need to delve further into algorithms to understand how they work as to have an idea why they perform either poorly or brilliantly. Algorithms I decided to learn about are:
#         1. MLPClassififer -- to understand neural networks in general
#         2. SGDClassifier -- to understand the stochastic classifier since it's second best
#         3. Decision Tree -- to understand decision trees since it's the worst model to train from the get go.
#     - During testing, I have been wondering about the current dataset and I think I have managed to notice few descrepencies I didn't see before. I will elaborate on this later.
#

# <markdown>
```     ______                  __  _                ___
#    /  _/ /____  _________ _/ /_(_)___  ____     |__ \
#    / // __/ _ \/ ___/ __ `/ __/ / __ \/ __ \    __/ /
#  _/ // /_/  __/ /  / /_/ / /_/ / /_/ / / / /   / __/
# /___/\__/\___/_/   \__,_/\__/_/\____/_/ /_/   /____/
```

# <markdown>
# Purpose of this iteration is to see whether decision trees algorithms will be improved from its worse accuracy performance.

# The plan is to test different set of configurations and then do the same thing for feature engineered features.

# After reading about complex decisions trees that can fail to generalise a problem [Link](https://scikit-learn.org/stable/modules/tree.html#tree),
# the following has been advised to attempt to reduce the chances of such issue:
# - Set a required minimum samples at leaf nodes.
# - Set a depth level number to say how far the tree can go.


# In [ ]
# Testing parameters with original dataset
from sklearn.model_selection import GridSearchCV

decision_tree_clf = DecisionTreeClassifier()
parameters = {
    'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None],
    'min_samples_leaf': [0.2, 0.4, 0.5, 1]
}
clf = GridSearchCV(decision_tree_clf, parameters, cv=10)
X = df.loc[:, ['LW','LD','RW','RD']]
y = df.loc[:, ['C']]
clf.fit(X, y)
pd.DataFrame(clf.cv_results_).loc[:, ['param_max_depth', 'param_min_samples_leaf', 'mean_test_score', 'std_test_score', 'rank_test_score']].sort_values(by=['rank_test_score']).head()

# In [ ]
# Creating columns for the calculated weights.
left_array = df.loc[:, ['LW', 'LD']].to_numpy()
calculations = [item[0] * item[1] for item in left_array]
df['L_calc'] = calculations
right_array = df.loc[:, ['RW', 'RD']].to_numpy()
calculations = [item[0] * item[1] for item in right_array]
df['R_calc'] = calculations
df.head()

# In [ ]
# Testing parameters with a new feature of calculations of weight and height for each side.

decision_tree_clf = DecisionTreeClassifier()
parameters = {
    'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None],
    'min_samples_leaf': [0.2, 0.4, 0.5, 1]
}
clf = GridSearchCV(decision_tree_clf, parameters, cv=10)
X = df.loc[:, ['LW','LD','RW','RD', 'L_calc', 'R_calc']]
y = df.loc[:, ['C']]
clf.fit(X, y)
pd.DataFrame(clf.cv_results_).loc[:, ['param_max_depth', 'param_min_samples_leaf', 'mean_test_score', 'std_test_score', 'rank_test_score']].sort_values(by=['rank_test_score']).head()

# In [ ]
# Test the configurations by using just the calculations of the weights and distance.
decision_tree_clf = DecisionTreeClassifier()
parameters = {
    'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None],
    'min_samples_leaf': [0.2, 0.4, 0.5, 1]
}
clf = GridSearchCV(decision_tree_clf, parameters, cv=10)
X = df.loc[:, [ 'L_calc', 'R_calc']]
y = df.loc[:, ['C']]
clf.fit(X, y)
pd.DataFrame(clf.cv_results_).loc[:, ['param_max_depth', 'param_min_samples_leaf', 'mean_test_score', 'std_test_score', 'rank_test_score']].sort_values(by=['rank_test_score']).head()


# <markdown>
# It looks like by introducing the calculations of weights and heights for each side helped the decision tree tremendously. Especially when only providing the calculatins on their own.

# I suppose that such calculations is kinda like a cheat, because I think it makes it easier for the model to 'sense' the algorithmic logic.

# I am very interested to see what will happen if I introduce boolean flag features (like making a hot-spot (I think) type features that are used for neural networks).

# In [ ]
# Creating feature columns to represent hot-spotted boolean values for the classes.
samples_array = df.loc[:, ['LW', 'LD', 'RW', 'RD']].to_numpy()
df['left_flag'] = [(item[0] * item[1]) > (item[2] * item[3]) for item in samples_array]
df['right_flag'] = [(item[0] * item[1]) < (item[2] * item[3]) for item in samples_array]
df['balanced_flag'] = [(item[0] * item[1]) == (item[2] * item[3]) for item in samples_array]
df.head()

# In [ ]
# Test the configurations by using just the calculations of the weights and distance.
decision_tree_clf = DecisionTreeClassifier()
parameters = {
    'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None],
    'min_samples_leaf': [0.2, 0.4, 0.5, 1]
}
clf = GridSearchCV(decision_tree_clf, parameters, cv=10)
X = df.loc[:, ['LW', 'LD', 'RW', 'RD', 'left_flag', 'balanced_flag', 'right_flag']]
y = df.loc[:, ['C']]
clf.fit(X, y)
pd.DataFrame(clf.cv_results_).loc[:, ['param_max_depth', 'param_min_samples_leaf', 'mean_test_score', 'std_test_score', 'rank_test_score']].sort_values(by=['rank_test_score']).head()

# In [ ]
# Test the configurations by using just the calculations of the weights and distance.
decision_tree_clf = DecisionTreeClassifier()
parameters = {
    'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None],
    'min_samples_leaf': [0.2, 0.4, 0.5, 1]
}
clf = GridSearchCV(decision_tree_clf, parameters, cv=10)
X = df.loc[:, ['left_flag', 'balanced_flag', 'right_flag']]
y = df.loc[:, ['C']]
clf.fit(X, y)
pd.DataFrame(clf.cv_results_).loc[:, ['param_max_depth', 'param_min_samples_leaf', 'mean_test_score', 'std_test_score', 'rank_test_score']].sort_values(by=['rank_test_score']).head()

# <markdown>
Conclusions after trying feature engineering:
- Calculated weights on each side:
  - with the rest of features, it's on average 90%
  - on their own, it's staggering 97%
- Boolean flags
  - With or without the rest of the feautres, it's pretty much 100%.
    - In other words, I have already done the job for the algorithm :smiley:.

Thus, it seems that the calculated weights of the features helps to make better guesses about the incoming values whereas the boolean flags are cheats.

The next experiment will see whether I can make a model from balanced dataset where there are equal number of samples for each class.

Before I do that though, I need to look into overfitting problems of the algorithm. During experiments, I noticed that the decision tree's accuracy would decrease
if I fed it less training data when I performed different cross-validations (i.e. k-folds).
What I would like to see is whether samples that sit on each end of the range (e.g. on value 1 and 5 rather than inbetween them) that can affect the accuracy and only use original features and the calculated weights.
I will make the rations of class samples balanced as to be consistent with the mentioned experiment.

ToDo Overfitting Experiments:
- [x] Only upper values of the range (i.e. 5 in weights and distance no matter what in other values as long as conditions are met)
    - ~[ ] With original features~
    - [x] With original features and the calculated weights
- [x] Only lower values of the range (i.e. 1 in weights and distance no matter what in other values as long as conditions are met)
    - ~[ ] With original features~
    - [x] With original features and the calculated weights
- [x] Upper and lower values of the range (i.e. both of the prior conditions)
    - ~[ ] With original features~
    - [x] With original features and the calculated weights

Update: just did some look up at the tree algorithm structures in 'looking_at_decision_trees_structre.py' file and its generated pdf documents.

# In [ ]
upper_values_df = df[(df.LD == 5) | (df.LW == 5) | (df.RD == 5) | (df.RW == 5)]
lower_values_df = df[(df.LD == 1) | (df.LW == 1) | (df.RD == 1) | (df.RW == 1)]
upper_values_df.groupby('C').count()
lower_values_df.groupby('C').count()

# From the looks of it, I will choose 15 samples of each class for lower and upper values
SEED = 1111

# Making random samples for lower values by each class
bal_df = lower_values_df[lower_values_df.C == 'B']
left_df = lower_values_df[lower_values_df.C == 'L']
right_df = lower_values_df[lower_values_df.C == 'R']

bal_samples = bal_df.sample(n=15, random_state=SEED)
left_samples = left_df.sample(n=15, random_state=SEED)
right_samples = right_df.sample(n=15, random_state=SEED)

lower_samples_df = pd.concat([bal_samples, left_samples, right_samples])
lower_samples_df.index

# Making random samples for upper values by each class
bal_df = upper_values_df[upper_values_df.C == 'B']
left_df = upper_values_df[upper_values_df.C == 'L']
right_df = upper_values_df[upper_values_df.C == 'R']
bal_df.describe()
left_df.describe()

bal_samples = bal_df.sample(n=15, random_state=SEED)
left_samples = left_df.sample(n=15, random_state=SEED)
right_samples = right_df.sample(n=15, random_state=SEED)

upper_samples_df = pd.concat([bal_samples, left_samples, right_samples])
upper_samples_df.index

both_samples_df = pd.concat([lower_samples_df, upper_samples_df])

# In [ ]
# For dataset description purpose
lower_samples_df.describe()

# In [ ]
upper_samples_df.describe()

# In [ ]

def separate_dataframe_from_training_one(original_df, training_df):
    '''Return a newly-generated dataframe where one's rows don't exist in a training one'''
    original_set = set(original_df.index)
    training_set = set(training_df.index)
    non_training_set = original_set - training_set
    return original_df.iloc[list(non_training_set)]

# In [ ]
from sklearn.metrics import accuracy_score

separated_df = separate_dataframe_from_training_one(df, lower_samples_df)

decision_tree_clf = DecisionTreeClassifier()
list_of_features = ['LW', 'LD', 'RW', 'RD', 'L_calc', 'R_calc']
X = lower_samples_df.loc[:, list_of_features]
y = lower_samples_df.loc[:, ['C']]
decision_tree_clf.fit(X, y)
X = separated_df.loc[:, list_of_features]
y = separated_df.loc[:, ['C']]
accuracy_score(decision_tree_clf.predict(X), y)

# In [ ]
# Storing tree into the dot format for observation
# tree.export_graphviz(decision_tree_clf, out_file='lower_1_tree.dot')

# In [ ]
separated_df = separate_dataframe_from_training_one(df, upper_samples_df)

decision_tree_clf = DecisionTreeClassifier()
list_of_features = ['LW', 'LD', 'RW', 'RD', 'L_calc', 'R_calc']
# list_of_features = ['LW', 'LD', 'RW', 'RD']
X = upper_samples_df.loc[:, list_of_features]
y = upper_samples_df.loc[:, ['C']]
decision_tree_clf.fit(X, y)
X = separated_df.loc[:, list_of_features]
y = separated_df.loc[:, ['C']]
accuracy_score(decision_tree_clf.predict(X), y)

# In [ ]
separated_df = separate_dataframe_from_training_one(df, both_samples_df)

decision_tree_clf = DecisionTreeClassifier()
list_of_features = ['LW', 'LD', 'RW', 'RD', 'L_calc', 'R_calc']
# list_of_features = ['LW', 'LD', 'RW', 'RD']
X = both_samples_df.loc[:, list_of_features]
y = both_samples_df.loc[:, ['C']]
decision_tree_clf.fit(X, y)
X = separated_df.loc[:, list_of_features]
y = separated_df.loc[:, ['C']]
accuracy_score(decision_tree_clf.predict(X), y)

# <markdown>
It looks like that the models still perform good even though I was expecting some overfitting problems. Even if there are only few samples to train from for particular boundaries
(e.g. on average 70% accuracy for lower values and average 80)

I believe it is because the samples have a wide range of values for weights and distances that still managed to make well-performed models
(e.g. lower-values-only samples without the calculated weights would produce on average 59%).

Thus, I shall make samples that only contain measurements that meet certain range criterial (i.e. maximum and minimum values)

I believe this is because there's a wide range of the calculated weights for the classes and thus it helped the model
to determine classes accurately. Like you can see below.

# In [ ]
# Checking out the calculated weights
upper_samples_df.loc[:, ['L_calc', 'R_calc']].describe()
lower_samples_df.loc[:, ['L_calc', 'R_calc']].describe()
both_samples_df.loc[:, ['L_calc', 'R_calc']].describe()

lower_samples_df.R_calc.nunique()
lower_samples_df.L_calc.nunique()
both_samples_df.L_calc.nunique()
both_samples_df.R_calc.nunique()

# <markdown>
Thus, I shall make a dataframes for calculated weights value to see whether I can achieve overfitting.

# In [ ]
upper_values_df = df[(df.LD >= 4) & (df.LW >= 4) & (df.RD >= 4) & (df.RW >= 4)]
lower_values_df = df[(df.LD <= 2) & (df.LW <= 2) & (df.RD <= 2) & (df.RW <= 2)]
upper_values_df.groupby('C').count()
lower_values_df.groupby('C').count()
lower_values_df[lower_values_df.C == 'B'].describe()
lower_values_df[lower_values_df.C == 'R'].describe()
lower_values_df[lower_values_df.C == 'L'].describe()
upper_values_df[upper_values_df.C == 'B'].describe()
upper_values_df[upper_values_df.C == 'R'].describe()
upper_values_df[upper_values_df.C == 'L'].describe()
# Ok, it looks like there are very few samples for training purposes which is kinda ideal for overfitting.
# But what's more ideal is the range of calculated weights that hopefully will introduce overfitting.
# It looks like there are only maximum 6 samples, I shall pick just 4 for each class and value boundary.
SEED = 1111

# Making random samples for lower values by each class
bal_df = lower_values_df[lower_values_df.C == 'B']
left_df = lower_values_df[lower_values_df.C == 'L']
right_df = lower_values_df[lower_values_df.C == 'R']

bal_samples = bal_df.sample(n=4, random_state=SEED)
left_samples = left_df.sample(n=4, random_state=SEED)
right_samples = right_df.sample(n=4, random_state=SEED)

lower_samples_df = pd.concat([bal_samples, left_samples, right_samples])
lower_samples_df.index

# Making random samples for upper values by each class
bal_df = upper_values_df[upper_values_df.C == 'B']
left_df = upper_values_df[upper_values_df.C == 'L']
right_df = upper_values_df[upper_values_df.C == 'R']
bal_df.describe()
left_df.describe()

bal_samples = bal_df.sample(n=4, random_state=SEED)
left_samples = left_df.sample(n=4, random_state=SEED)
right_samples = right_df.sample(n=4, random_state=SEED)

upper_samples_df = pd.concat([bal_samples, left_samples, right_samples])
upper_samples_df.index

both_samples_df = pd.concat([lower_samples_df, upper_samples_df])

# In [ ]
# For dataset description purpose
lower_samples_df.describe()

# In [ ]
upper_samples_df.describe()

# In [ ]
from sklearn.metrics import accuracy_score

separated_df = separate_dataframe_from_training_one(df, lower_samples_df)

decision_tree_clf = DecisionTreeClassifier()
list_of_features = ['LW', 'LD', 'RW', 'RD', 'L_calc', 'R_calc']
X = lower_samples_df.loc[:, list_of_features]
y = lower_samples_df.loc[:, ['C']]
decision_tree_clf.fit(X, y)
X = separated_df.loc[:, list_of_features]
y = separated_df.loc[:, ['C']]
accuracy_score(decision_tree_clf.predict(X), y)

# In [ ]
# Storing tree into the dot format for observation
# tree.export_graphviz(decision_tree_clf, out_file='lower_2_tree.dot')

# In [ ]
separated_df = separate_dataframe_from_training_one(df, upper_samples_df)

decision_tree_clf = DecisionTreeClassifier()
list_of_features = ['LW', 'LD', 'RW', 'RD', 'L_calc', 'R_calc']
# list_of_features = ['LW', 'LD', 'RW', 'RD']
X = upper_samples_df.loc[:, list_of_features]
y = upper_samples_df.loc[:, ['C']]
decision_tree_clf.fit(X, y)
X = separated_df.loc[:, list_of_features]
y = separated_df.loc[:, ['C']]
accuracy_score(decision_tree_clf.predict(X), y)

# In [ ]
separated_df = separate_dataframe_from_training_one(df, both_samples_df)

decision_tree_clf = DecisionTreeClassifier()
list_of_features = ['LW', 'LD', 'RW', 'RD', 'L_calc', 'R_calc']
# list_of_features = ['LW', 'LD', 'RW', 'RD']
X = both_samples_df.loc[:, list_of_features]
y = both_samples_df.loc[:, ['C']]
decision_tree_clf.fit(X, y)
X = separated_df.loc[:, list_of_features]
y = separated_df.loc[:, ['C']]
accuracy_score(decision_tree_clf.predict(X), y)

# <markdown>
Ok, I can see that the model is under performing for three categories of datasets,
I will pick the lower tier for comparison since it looks like it

Update: just did some look up at the tree algorithm structures in 'looking_at_decision_trees_structre.py' file and its generated pdf documents.

At this point, I will have a look at SGDClassifier algorithm.
