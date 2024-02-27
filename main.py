from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pickle
import pandas as pd
from model import ListMitra
from preprocessing import encode_data

app = FastAPI()

# load model and encoder
with open("./model/model_optimal_smote_rf.pkl", "rb") as f:
    model = pickle.load(f)

# load encoder
with open("./encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

@app.get("/")
async def root():
    return {"message": "API Model is online!"}

@app.post("/predict/")
async def predict(mitra_predict: ListMitra):
    daftar_mitra = mitra_predict.daftar_mitra
    try:
        # buat dataframe untuk prediksi
        df = pd.DataFrame(jsonable_encoder(daftar_mitra))
        df.set_index("id", inplace=True)

        # encode data
        df_encoded = encode_data(df, encoder, pd)
        df_encoded.to_csv("df_encoded.csv")

        # predict
        predictions = model.predict(df_encoded)

        # buat dataframe untuk hasil prediksi
        result = pd.DataFrame({"id_mitra": df.index, "status_rekomendasi": predictions.astype(bool)})

        return {"data": result.to_dict(orient="records")}
    except Exception as e:
        return {"message": str(e)}