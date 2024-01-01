import json, glob
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FOLDER_PATH = os.path.join(ROOT_DIR, 'collected_data', '*.json')

X = []
y = []

# Use glob to get all JSON files in the 'OUT' folder
for json_file in glob.glob(OUT_FOLDER_PATH):
    with open(json_file, 'r') as file:
        try:
            data
        except NameError:
            data = json.load(file)
        else:
            data.extend(json.load(file))
        print(json_file, len(data))

# Extract features and target variable
X = np.array([[item['def_ask_avg'], item['def_pid_avg'], item['Bid Standard Deviation'], item['Ask Standard Deviation'], item['Spread']] for item in data])
y = np.array([item['Last_Price'] for item in data])

# Scaling the data is important for Neural Networks
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build the Neural Network model
model = Sequential([
    Dense(10, activation='relu', input_shape=(X_train.shape[1],)),  # Input layer
    Dense(10, activation='relu'),  # Hidden layer
    Dense(1)  # Output layer
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model on test set
mse = model.evaluate(X_test, y_test)
print(f"Mean Squared Error on Test Set: {mse:.4f}")

model.save(os.path.join(ROOT_DIR, '..', 'neural_network_model.h5'))
