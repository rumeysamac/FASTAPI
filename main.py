from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Tüm HTTP Metotları Projesi", version="1.0")

# Sahte bir veritabanı (bellekte tutulan sözlük)
veritabani = {
    1: {"ad": "Laptop", "fiyat": 30000.0, "stok": 5},
    2: {"ad": "Mouse", "fiyat": 750.0, "stok": 50},
}


# Pydantic Modelleri
class Urun(BaseModel):
  ad: str
  fiyat: float
  stok: int


class UrunGuncelle(BaseModel):
  ad: str | None = None
  fiyat: float | None = None
  stok: int | None = None


# 1. GET: Tüm ürünleri listele
@app.get("/urunler")
def urunleri_getir():
  return {"urunler": veritabani}


# 2. GET: Tek bir ürünü ID'ye göre getir
@app.get("/urunler/{urun_id}")
def urun_getir(urun_id: int):
  if urun_id not in veritabani:
    raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
  return {"urun_id": urun_id, "veri": veritabani[urun_id]}


# 3. POST: Yeni ürün ekle
@app.post("/urunler")
def urun_ekle(urun: Urun):
  yeni_id = max(veritabani.keys()) + 1 if veritabani else 1
  veritabani[yeni_id] = {"ad": urun.ad, "fiyat": urun.fiyat, "stok": urun.stok}
  return {
      "mesaj": "Ürün başarıyla eklendi!",
      "id": yeni_id,
      "veri": veritabani[yeni_id],
  }


# 4. PUT: Ürünü tamamen güncelle (Yoksa hata dönebilir veya oluşturulabilir)
@app.put("/urunler/{urun_id}")
def urun_guncelle_tam(urun_id: int, urun: Urun):
  if urun_id not in veritabani:
    raise HTTPException(status_code=404, detail="Güncellenecek ürün bulunamadı!")
  veritabani[urun_id] = {"ad": urun.ad, "fiyat": urun.fiyat, "stok": urun.stok}
  return {"mesaj": "Ürün tamamen güncellendi!", "veri": veritabani[urun_id]}


# 5. PATCH: Ürünün sadece gönderilen alanlarını güncelle
@app.patch("/urunler/{urun_id}")
def urun_guncelle_kismen(urun_id: int, urun: UrunGuncelle):
  if urun_id not in veritabani:
    raise HTTPException(status_code=404, detail="Ürün bulunamadı!")

  mevcut_veri = veritabani[urun_id]
  guncel_veri = urun.model_dump(
      exclude_unset=True
  )  # Sadece gönderilen alanları al

  for anahtar, deger in guncel_veri.items():
    mevcut_veri[anahtar] = deger

  return {"mesaj": "Ürün kısmen güncellendi!", "veri": mevcut_veri}


# 6. DELETE: Ürün sil
@app.delete("/urunler/{urun_id}")
def urun_sil(urun_id: int):
  if urun_id not in veritabani:
    raise HTTPException(status_code=404, detail="Silinecek ürün bulunamadı!")
  silinen = veritabani.pop(urun_id)
  return {"mesaj": "Ürün başarıyla silindi!", "silinen_veri": silinen}