import joblib
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

general_path = "/path/to/your/dataset"
data = pd.read_csv(f"{general_path}/features_3_sec.csv")
data = data.iloc[0:, 1:]
y = data["label"]
y = preprocessing.LabelEncoder().fit_transform(y)
X = data.drop(columns=["label"])
cols = X.columns
min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X)
X = pd.DataFrame(X, columns=cols)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
model = XGBClassifier(n_estimators=1000, learning_rate=0.05)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
joblib.dump(min_max_scaler, "ml/scaler.gz")
joblib.dump(model, "ml/model.gz")
