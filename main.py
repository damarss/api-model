from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pickle
import pandas as pd
from model import ListMitra
from preprocessing import encode_data, measure_distance
from fastapi.middleware.cors import CORSMiddleware
from utils import get_latest_model_url, check_latest_model_url
from urllib.request import Request, urlopen
import aiohttp
import requests
import fsspec
import uvicorn

app = FastAPI()

origins = [
    "https://organic-garbanzo-9xq4rgx4x96f9prr-3000.app.github.dev",
    "https://skripsi-ivory.vercel.app",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load encoder
with open("./encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

@app.get("/")
async def root():
    return {"message": "API Model is online!"}

@app.post("/predict/")
async def predict(mitra_predict: ListMitra):
    daftar_mitra = mitra_predict.daftar_mitra

    # ambil url model terbaru
    url_model = get_latest_model_url()

    with fsspec.open(url_model, "rb") as f:
        model = pickle.load(f)

    columns = model.get_booster().feature_names

    try:
        # buat dataframe untuk prediksi
        df = pd.DataFrame(jsonable_encoder(daftar_mitra))
        df.set_index("id", inplace=True)

        df['jarak'] = df.apply(measure_distance, axis=1)
        df.drop(columns=['latitude', 'longitude', 'satker_latitude', 'satker_longitude'], 
                inplace=True)

        # encode data
        df_encoded = encode_data(df, encoder, pd)

        # urutkan kolom
        df_encoded = df_encoded[columns]

        # predict
        predictions = model.predict(df_encoded)

        # buat dataframe untuk hasil prediksi
        result = pd.DataFrame({"id_mitra": df.index, "status_rekomendasi": predictions.astype(bool)})

        return {"data": result.to_dict(orient="records")}
    except Exception as e:
        return {"kolom": columns,
                "message": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
