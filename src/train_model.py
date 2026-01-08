from dataset.dataset import create_splits
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import math
import pickle
from enum import Enum

class ModelType(Enum):
    RF = "random_forest"
    GB = "gradient_boosting"

def select_model(model_type: ModelType) -> tuple[object, str]:
    if model_type == ModelType.RF:
        return RandomForestRegressor(
            n_estimators=200,
            max_depth=None,
            min_samples_split=2,
            random_state=42,
            n_jobs=-1
        ), "random_forest_model.pkl"
    else:
        return GradientBoostingRegressor(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            random_state=42
        ), "gradient_boosting_model.pkl"
    

def train_model(model_type: ModelType):

    X_train, X_test, y_train, y_test = create_splits()

    model, model_filename = select_model(model_type)
    
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    print("Train RMSE:", math.sqrt(mean_squared_error(y_train, train_pred)))
    print("Test  RMSE:", math.sqrt(mean_squared_error(y_test, test_pred)))

    print("Train R2:", r2_score(y_train, train_pred))
    print("Test  R2:", r2_score(y_test, test_pred))

    with open("models/" + model_filename, "wb") as f:
        pickle.dump(model, f)
    print(f"Saved: {model_filename}")

if __name__ == "__main__":
    train_model(ModelType.RF)