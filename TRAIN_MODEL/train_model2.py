import json, glob
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FOLDER_PATH = os.path.join(ROOT_DIR, 'collected_data', '*.json')

X = []
y = []

# Use glob to get all JSON files in the 'OUT' folder
for json_file in glob.glob(OUT_FOLDER_PATH):
    print(json_file)
    with open(json_file, 'r') as file:
        try:
            data
        except NameError:
            data = json.load(file)
        else:
            data.extend(json.load(file))
            print(len(data))

# Extract features and target variable
X = [[item['def_bid_avg'], item['def_ask_avg'], item['Bid Standard Deviation'], item['Ask Standard Deviation'], item['Spread']] for item in data]
y = [item['Last_Price'] for item in data]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model using Gradient Boosting
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)

# Predict on the test set
y_pred = gb_model.predict(X_test)


# Save the model locally
joblib.dump(gb_model, os.path.join(ROOT_DIR, '..', 'gradient_boosting_model_local.pkl'))

# Calculate and print the mean squared error on the test set
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error on Test Set: {mse:.4f}")

# print feature importances:
feature_importances = gb_model.feature_importances_
features = ['def_bid_avg', 'def_ask_avg', 'Bid Standard Deviation', 'Ask Standard Deviation', 'Spread']
for feature, importance in zip(features, feature_importances):
    print(f"Feature Importance:\n{feature}: {importance:.4f}")
