import json, glob
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FOLDER_PATH = os.path.join(ROOT_DIR, 'collected_data', '*.json')

X = []
y = []
avge_unit=0
# Use glob to get all JSON files in the 'OUT' folder
for json_file in glob.glob(OUT_FOLDER_PATH):
    total_Sum=0
    with open(json_file, 'r') as file:
        file_data=json.load(file)
        for ind,record in enumerate(file_data):
            if ind==0:record["reltive_price_change"]=0
            else: 
                record["reltive_price_change"]=(record["Last_Price"]/file_data[ind-1]["Last_Price"])*100
                total_Sum+=record["reltive_price_change"]
        try:
            data
        except NameError:
            data = file_data
        else:
            data.extend(file_data)
        print(json_file, len(data))
        avge_unit=total_Sum/len(data)


# Extract features and target variable
X = [[item['Bid Standard Deviation'], item['Ask Standard Deviation'], item['Spread']] for item in data]
y = [item['reltive_price_change'] for item in data]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model  1000 100
rf_retrained_local = RandomForestRegressor(n_estimators=1000, max_depth=1000, random_state=42) # Updated n_estimators and added max_depth
rf_retrained_local.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_retrained_local.predict(X_test)

# Calculate and print the mean squared error on the test set
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error on Test Set: {mse:.4f}  avge_unit is={avge_unit}")

# Feature Importance
importances = rf_retrained_local.feature_importances_
feature_names = [ 'Bid Standard Deviation', 'Ask Standard Deviation', 'Spread']
sorted_indices = importances.argsort()[::-1]
print("Feature Importance:")
for i in sorted_indices:
    print(f"{feature_names[i]}: {importances[i]:.4f}")

# Save the retrained model locally
joblib.dump(rf_retrained_local, os.path.join(ROOT_DIR, '..', 'retrained_random_forest_model_local.pkl'))
