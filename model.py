from typing import List
from pydantic import BaseModel

class Mitra(BaseModel):
    id: int
    total_menjadi_mitra_calculate: int
    SUSENAS: int
    SAKERNAS: int
    PODES: int
    KSA: int
    IMK: int
    Pendalaman_Materi: float
    Keaktifan_Pelatihan: float
    umur: int
    latitude: float
    longitude: float
    satker_latitude: float
    satker_longitude: float
    jk: str
    pendidikan: int

class ListMitra(BaseModel):
    daftar_mitra: List[Mitra]