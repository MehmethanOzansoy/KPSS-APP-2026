import sqlite3
import os
from config import DB_FILE, DEFAULT_MEDIA

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS subjects (id INTEGER PRIMARY KEY AUTOINCREMENT, ders TEXT NOT NULL, konu TEXT NOT NULL, durum TEXT NOT NULL)")
    try: cur.execute("ALTER TABLE subjects ADD COLUMN kategori TEXT DEFAULT 'GY'")
    except: pass
    
    GK_LESSONS = ["Tarih", "Coğrafya", "Vatandaşlık"]
    for ders in GK_LESSONS: 
        cur.execute("UPDATE subjects SET kategori = 'GK' WHERE ders = ? AND kategori = 'GY'", (ders,))
        
    cur.execute("""CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY AUTOINCREMENT, tip TEXT, tarih TEXT, ders TEXT, hedef_soru INTEGER, cozulen INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tests (id INTEGER PRIMARY KEY AUTOINCREMENT, tarih TEXT, ders TEXT, dogru INTEGER, yanlis INTEGER, net REAL, yuzde INTEGER, is_deneme INTEGER DEFAULT 0)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS trials (id INTEGER PRIMARY KEY AUTOINCREMENT, tarih TEXT, turkce_d INTEGER, turkce_y INTEGER, mat_d INTEGER, mat_y INTEGER, tarih_d INTEGER, tarih_y INTEGER, cog_d INTEGER, cog_y INTEGER, vat_d INTEGER, vat_y INTEGER, toplam_net REAL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS exams (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT, tur TEXT, tarih TEXT, reminder_days INTEGER DEFAULT 7)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS mistakes (id INTEGER PRIMARY KEY AUTOINCREMENT, ders TEXT, konu TEXT, not_icerik TEXT, resim_yolu TEXT, tarih TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS media_recs (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, title TEXT, desc TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS daily_tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, priority TEXT, task TEXT, lesson TEXT, duration INTEGER, is_completed INTEGER DEFAULT 0)""")
    
    # Pre-populate Daily Tasks if empty
    cur.execute("SELECT COUNT(*) FROM daily_tasks")
    if cur.fetchone()[0] == 0:
        tasks = [
            ("🔴 Yüksek", "Konu tekrarı", "Türkçe – Paragraf", 40),
            ("🔴 Yüksek", "Soru çözümü", "Matematik – Problemler", 60),
            ("🟡 Orta", "Konu tekrarı", "Tarih – Kurtuluş Savaşı", 30),
            ("🟡 Orta", "Deneme analizi", "Genel", 30),
            ("🟢 Düşük", "Kısa tekrar", "Vatandaşlık – Haklar", 20)
        ]
        for p, t, l, d in tasks:
            cur.execute("INSERT INTO daily_tasks (priority, task, lesson, duration, is_completed) VALUES (?, ?, ?, ?, 0)", (p, t, l, d))

    conn.commit()
    conn.close()

def seed_media_recs():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM media_recs")
    if cur.fetchone()[0] == 0:
        for m in DEFAULT_MEDIA: 
            cur.execute("INSERT INTO media_recs (type, title, desc) VALUES (?, ?, ?)", (m[0], m[1], m[2]))
        conn.commit()
    conn.close()

def load_all_from_db():
    init_db()
    seed_media_recs()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    data = {}
    cur.execute("SELECT * FROM subjects")
    data["subjects"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM goals")
    data["goals"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM tests")
    data["tests"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM trials")
    data["trials"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM exams")
    data["exams"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM mistakes")
    data["mistakes"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM media_recs")
    data["media"] = [dict(row) for row in cur.fetchall()]
    cur.execute("SELECT * FROM daily_tasks")
    data["daily_tasks"] = [dict(row) for row in cur.fetchall()]
    
    conn.close()
    return data

def ensure_default_kpss_topics():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT ders, konu FROM subjects")
    existing = set(cur.fetchall())
    GY_LESSONS = ["Türkçe", "Matematik", "Geometri", "Mantık"]
    data = {
        "Türkçe": ["Sözcükte Anlam", "Cümlede Anlam", "Paragrafta Anlam", "Sözcükte Yapı", "Cümlede Yapı", "Anlatım Bozuklukları", "Noktalama İşaretleri", "Yazım Kuralları", "Sözel Mantık"],
        "Matematik": ["Temel Kavramlar", "Sayılar", "Bölme-Bölünebilme", "Rasyonel Sayılar", "Eşitsizlikler", "Mutlak Değer", "Üslü-Köklü Sayılar", "Çarpanlara Ayırma", "Oran-Orantı", "Problemler", "Kümeler", "Fonksiyonlar", "Permütasyon-Kombinasyon-Olasılık", "Geometri", "Sayısal Mantık"],
        "Tarih": ["İslamiyet Öncesi Türk Tarihi", "İlk Türk-İslam Devletleri", "Osmanlı Devleti Kuruluş-Yükselme", "Osmanlı Kültür ve Medeniyeti", "17-18. YY Osmanlı", "19. YY Osmanlı (Dağılma)", "Kurtuluş Savaşı Hazırlık", "Kurtuluş Savaşı Cepheler", "Atatürk Dönemi İç-Dış Politika", "Atatürk İlkeleri ve İnkılaplar", "Çağdaş Türk ve Dünya Tarihi"],
        "Coğrafya": ["Türkiye'nin Coğrafi Konumu", "Türkiye'nin Yer şekilleri", "Türkiye'nin İklimi ve Bitki Örtüsü", "Türkiye'de Nüfus ve Yerleşme", "Türkiye'de Tarım ve Hayvancılık", "Türkiye'de Madenler ve Enerji Kaynakları", "Türkiye'de Sanayi, Ticaret, Ulaşım", "Türkiye'de Turizm", "Bölgesel Coğrafya"],
        "Vatandaşlık": ["Hukukun Temel Kavramları", "Anayasa Hukuku Tarihi", "1982 Anayasası Temel Esaslar", "Yasama", "Yürütme", "Yargı", "İdare Hukuku"]}
    for ders, topics in data.items():
        kat = "GY" if ders in GY_LESSONS else "GK"
        for konu in topics:
            if (ders, konu) not in existing: cur.execute("INSERT INTO subjects (ders, konu, durum, kategori) VALUES (?, ?, ?, ?)", (ders, konu, "Başlanmadı", kat))
    conn.commit()
    conn.close()

def ensure_specific_exams():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT ad, tarih FROM exams")
    existing = {(row[0], row[1]) for row in cur.fetchall()}
    exams = [("KPSS Lisans", "Genel Yetenek-Genel Kültür", "2026-09-06"), ("Eğitim Bilimleri", "KPSS", "2026-09-06"), ("Alan Bilgisi 1", "KPSS", "2026-09-12"), ("Alan Bilgisi 2", "KPSS", "2026-09-13"), ("ÖABT", "KPSS", "2026-09-20")]
    for ad, tur, tar in exams:
        if (ad, tar) not in existing: cur.execute("INSERT INTO exams (ad, tur, tarih) VALUES (?, ?, ?)", (ad, tur, tar))
    conn.commit()
    conn.close()
