import sqlite3


def baglan():
    return sqlite3.connect("banka.db")


def bakiye_goster(hesap_id):
    conn = baglan()
    sonuc = conn.execute(
        "SELECT bakiye FROM hesaplar WHERE id = ?", (hesap_id,)
    ).fetchone()
    conn.close()
    if sonuc is None:
        return None
    return sonuc[0]


def para_yatir(hesap_id, tutar):
    if tutar <= 0:
        print("Hata: Tutar 0'dan büyük olmalı.")
        return
    if bakiye_goster(hesap_id) is None:
        print("Hata: Böyle bir hesap yok.")
        return

    conn = baglan()
    conn.execute(
        "UPDATE hesaplar SET bakiye = bakiye + ? WHERE id = ?", (tutar, hesap_id)
    )
    conn.execute(
        "INSERT INTO islemler (hesap_id, tur, tutar) VALUES (?, 'yatirma', ?)",
        (hesap_id, tutar),
    )
    conn.commit()
    conn.close()
    print(f"{tutar} TL yatırıldı. Yeni bakiye: {bakiye_goster(hesap_id)} TL")


if __name__ == "__main__":
    print("Önceki bakiye:", bakiye_goster(1))
    para_yatir(1, 500)
    para_yatir(1, -50)
    para_yatir(99, 100)
