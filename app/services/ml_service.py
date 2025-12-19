
import os
import joblib
def chargeModel_prediction(employee_df):
    WORKDIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    model_path= os.path.join(WORKDIR, "ml","models", "saved_model", "model.pkl")
    model= joblib.load(model_path)
    prediction= model.predict(employee_df)
    confident= model.predict_proba(employee_df).max()
    return prediction, confident