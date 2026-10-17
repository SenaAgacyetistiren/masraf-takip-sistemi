from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from database import get_connection

app = FastAPI(title="Masraf & Süreç Takip Sistemi")

# HTML Şablon Klasörünü Tanımlıyoruz
templates = Jinja2Templates(directory="templates")

# Ana Sayfa: Web Arayüzü (Dashboard)
@app.get("/", response_class=HTMLResponse)
def ana_sayfa(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# İstek modelleri (Pydantic)
class TalepOlustur(BaseModel):
    calisan_adi: str
    kategori: str
    tutar: float
    aciklama: Optional[str] = None

class OnayDurumu(BaseModel):
    durum: str
    red_nedeni: Optional[str] = None

# 2. Yeni Masraf Talebi Oluşturma (5.000 TL Kuralı)
@app.post("/talepler/")
def talep_olustur(talep: TalepOlustur):
    if talep.tutar > 5000:
        onay_turu = "Yonetici + Finans Cift Onayi"
    else:
        onay_turu = "Yalnizca Departman Yoneticisi Onayi"
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO talepler (calisan_adi, kategori, tutar, aciklama, durum, onay_turu)
        VALUES (%s, %s, %s, %s, 'ONAY_BEKLIYOR', %s)
        RETURNING id;
    """, (talep.calisan_adi, talep.kategori, talep.tutar, talep.aciklama, onay_turu))
    
    yeni_id = cursor.fetchone()["id"]
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        "mesaj": "Talep başarıyla kaydedildi.",
        "talep_id": yeni_id,
        "onay_turu": onay_turu,
        "durum": "ONAY_BEKLIYOR"
    }

# 3. Talepleri Listeleme
@app.get("/talepler/")
def talepleri_listele(durum: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    if durum:
        cursor.execute("SELECT * FROM talepler WHERE durum = %s ORDER BY tarih DESC;", (durum,))
    else:
        cursor.execute("SELECT * FROM talepler ORDER BY tarih DESC;")
        
    talepler = cursor.fetchall()
    cursor.close()
    conn.close()
    return talepler

# 4. Talep Onaylama veya Reddetme
@app.put("/talepler/{talep_id}/onay")
def talep_onayla_reddet(talep_id: int, veri: OnayDurumu):
    if veri.durum not in ["ONAYLANDI", "REDDEDILDI"]:
        raise HTTPException(status_code=400, detail="Durum 'ONAYLANDI' veya 'REDDEDILDI' olmalıdır.")
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE talepler 
        SET durum = %s, red_nedeni = %s
        WHERE id = %s
        RETURNING *;
    """, (veri.durum, veri.red_nedeni, talep_id))
    
    guncellenen = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    if not guncellenen:
        raise HTTPException(status_code=404, detail="Talep bulunamadı.")
        
    return {"mesaj": f"Talep durumu '{veri.durum}' olarak güncellendi.", "talep": guncellenen}

# 5. Muhasebe / Finans Ödeme Tamamlama
@app.put("/talepler/{talep_id}/ode")
def odeme_yap(talep_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE talepler 
        SET durum = 'ODENDI'
        WHERE id = %s AND durum = 'ONAYLANDI'
        RETURNING *;
    """, (talep_id,))
    
    guncellenen = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    if not guncellenen:
        raise HTTPException(status_code=400, detail="Ödeme yapılabilmesi için talebin ONAYLANDI durumunda olması gerekir.")
        
    return {"mesaj": "Ödeme tamamlandı ve süreç kapatıldı.", "talep": guncellenen}