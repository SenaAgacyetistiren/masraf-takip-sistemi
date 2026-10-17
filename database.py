import psycopg2
from psycopg2.extras import RealDictCursor

# PostgreSQL bağlantı ayarları
# password kısmına DBeaver'a bağlanırken kullandığın şifreyi yaz
DB_CONFIG = {
    "dbname": "masraf_db",
    "user": "postgres",
    "password": "",     # <--- BURAYA KENDİ ŞİFRENİ YAZ
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Masraf talepleri tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS talepler (
            id SERIAL PRIMARY KEY,
            calisan_adi VARCHAR(100) NOT NULL,
            kategori VARCHAR(50) NOT NULL,
            tutar NUMERIC(10, 2) NOT NULL,
            aciklama TEXT,
            durum VARCHAR(30) DEFAULT 'ONAY_BEKLIYOR',
            onay_turu VARCHAR(50),
            red_nedeni TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Talepler tablosu PostgreSQL (masraf_db) içinde başarıyla oluşturuldu!")