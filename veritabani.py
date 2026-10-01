import sqlite3

def baglan():
    conn = sqlite3.connect("banka.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def tablolari_olustur():
    conn = baglan()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS musteriler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_soyad TEXT NOT NULL,
        tc_no TEXT UNIQUE NOT NULL,
        kayit_tarihi TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS hesaplar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        musteri_id INTEGER NOT NULL,
        bakiye REAL NOT NULL DEFAULT 0 CHECK (bakiye >= 0),
        acilis_tarihi TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (musteri_id) REFERENCES musteriler(id)
    );

    CREATE TABLE IF NOT EXISTS islemler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hesap_id INTEGER NOT NULL,
        tur TEXT NOT NULL CHECK (tur IN ('yatirma', 'cekme', 'havale_giden', 'havale_gelen')),
        tutar REAL NOT NULL CHECK (tutar > 0),
        tarih TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hesap_id) REFERENCES hesaplar(id)
    );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    tablolari_olustur()
    print("Tablolar oluşturuldu: banka.db")
