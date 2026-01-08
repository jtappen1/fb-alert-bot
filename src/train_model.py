from dataset.dataset import create_splits
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import math
import pickle

X_train, X_test, y_train, y_test = create_splits()

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Root Mean Squared Error: {math.sqrt(mse):.2f}")
print(f"R^2 Score: {r2:.2f}")

with open("guitar_model.pkl", "wb") as f:
    pickle.dump(model, f)