import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

supabase: Client = create_client(url, key)

def get_latest_model_url():
    res = supabase.storage.from_("model").list(options={
        "limit": 1,
        "sortBy": {
            "column": "created_at",
            "order": "desc"
        }
    })

    url = supabase.storage.from_("model").get_public_url(res[0]['name'])
    return url

def check_latest_model_url(url: str):
    latest_url = get_latest_model_url()
    return url==latest_url