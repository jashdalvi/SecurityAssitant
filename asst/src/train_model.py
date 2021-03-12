import pickle
from sklearn.model_selection import cross_val_score,StratifiedKFold,GridSearchCV
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import numpy as np
import os



emb_path = os.path.join(os.path.join("..",'data'),"data.pickle")
with open(emb_path,'rb') as f:
    data = pickle.load(f)

X = data['embeddings']
y = data['labels']

print('Creating data for ML model')
np.random.seed(42)
scalar = StandardScaler()
X = np.array(X)
y = np.array(y)
indexes = np.random.permutation(np.arange(X.shape[0]))
le = LabelEncoder()
y = le.fit_transform(y)
X = X[indexes]
y = y[indexes]
model = LinearSVC()
#model = SVC(kernel = 'linear')
pipeline = Pipeline([('transformer', scalar), ('estimator',model)])
#pipeline = Pipeline([('estimator',model)])
cv = StratifiedKFold(n_splits=5)
grid_svc = GridSearchCV(pipeline,param_grid = {'estimator__C':[0.0001,0.001,0.01,0.1,1,10]},scoring = 'accuracy',verbose = True,cv = cv,n_jobs = -1)
grid_svc.fit(X,y)
print("The Best score for svc model is {} with params {}".format(grid_svc.best_score_,grid_svc.best_params_))
cross_val_scores = cross_val_score(grid_svc,X,y,cv = cv)

print('The cross-validation  score for Linear Support vector Machine model is {}'.format(cross_val_scores.mean()))

print('Now training on whole data and saving model')
#scalar_all = StandardScaler()
#X = scalar_all.fit_transform(X)
#model = SVC(kernel = 'linear')
X = data['embeddings']
y = data['labels']
np.random.seed(42)
scalar_all = StandardScaler()
X = np.array(X)
y = np.array(y)
indexes = np.random.permutation(np.arange(X.shape[0]))
le = LabelEncoder()
y = le.fit_transform(y)
X = X[indexes]
y = y[indexes]
X = scalar_all.fit_transform(X)
print(X.shape)
print(y.shape)
model = grid_svc.best_estimator_
model.fit(X,y)
y_pred = model.predict(X)
print(classification_report(y,y_pred,target_names = le.classes_))

head_model_path = os.path.join("..",'data/head_model.sav')
scaling_path = os.path.join("..",'data/scaling.pkl')
labelencoder_path = os.path.join("..",'data/labelencoder.pkl')

if os.path.exists(head_model_path):
    os.remove(head_model_path)

if os.path.exists(scaling_path):
    os.remove(scaling_path)

if os.path.exists(labelencoder_path):
    os.remove(labelencoder_path)


with open(head_model_path,'wb') as fhandle:
    pickle.dump(model,fhandle)

with open(scaling_path,'wb') as f:
    pickle.dump(scalar_all,f)

with open(labelencoder_path,'wb') as flabel:
    pickle.dump(le,flabel)



