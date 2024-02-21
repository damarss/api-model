from fastapi import FastAPI
import pickle

app = FastAPI()

# load model and encoder
with open("./model/model_awal_rf.pkl", "rb") as f:
    model = pickle.load(f)

# load encoder
with open("./encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

def preprocess_input(input_data):
    # encode input data
    input_data_encoded = encoder.transform(input_data)
    return input_data_encoded

@app.get("/")
async def root():
    return {"message": "API Model is online!"}

@app.get("/predict/")
async def predict():
    return {"message": model.feature_names_in_.tolist()}