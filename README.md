# 💼 Masraf & Süreç Takip Sistemi (Expense & Workflow Management Portal)

Bu proje, kurum içi masraf taleplerinin BPMN tabanlı iş akışı ve dinamik onay mekanizmalarıyla yönetilmesini sağlayan uçtan uca bir **Yönetim Bilişim Sistemleri (YBS)** portföy projesidir.

---

## 🎯 Projenin Amacı ve İş Kuralları

Kurumsal süreçlerde manuel yürütülen onay mekanizmalarını dijitalleştirerek hata payını azaltmak ve onay hızını artırmak hedeflenmiştir:
* **Harcama Girişi:** Çalışan harcama tutarını, kategorisini ve fiş detayını girer.
* **Dinamik İş Kuralı (BPMN Akışı):**
  * **Tutar $\le$ 5.000 TL:** Yalnızca Departman Yöneticisi onayı yeterlidir.
  * **Tutar > 5.000 TL:** Yüksek bütçe kontrolü amacıyla otomatik olarak **Çift Onay** (Departman Yöneticisi + Finans Müdürü) sürecine aktarılır.
* **Finans/Ödeme Kapatma:** Yalnızca onaylanmış talepler muhasebe/finans birimi tarafından `ODENDI` durumuna getirilerek kapatılabilir.

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3, FastAPI, Uvicorn, Pydantic
* **Veritabanı:** PostgreSQL, DBeaver, psycopg2
* **Frontend:** HTML5, Jinja2 Templates, Bootstrap 5, Bootstrap Icons
* **API Test & Doğrulama:** Postman

---

## 🚀 Kurulum ve Çalıştırma

1. **Depoyu klonlayın:**
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/masraf-takip-sistemi.git](https://github.com/KULLANICI_ADIN/masraf-takip-sistemi.git)
   cd masraf-takip-sistemi


## 📸 Ekran Görüntüleri
<img width="1462" height="767" alt="dashboard" src="https://github.com/user-attachments/assets/a267903e-f9e7-4abf-a85e-0e74627c3754" />



   
