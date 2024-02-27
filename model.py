from typing import List
from pydantic import BaseModel

class Mitra(BaseModel):
    id: int
    total_menjadi_mitra_calculate: int
    SUSENAS: bool
    SAKERNAS: bool
    PODES: bool
    KSA: bool
    IMK: bool
    Pendalaman_Materi: float
    Keaktifan_Pelatihan: float
    umur: int
    alamat: str
    jk: str
    pendidikan: str
    status: str

class ListMitra(BaseModel):
    daftar_mitra: List[Mitra]