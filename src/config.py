import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        # Check if running from source in a modular structure
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

DB_FILE = "kpss_tracker.db"
MISTAKE_IMG_DIR = "mistakes_images"
USER_IMG_PATH = os.path.join("assets", "image.png")
LOGO_PATH = os.path.join("assets", "logo.jpg")
HOCA_LIST_PATH = os.path.join("assets", "hoca_listesi.json")

MOTIVATION_QUOTES = [
    "Başarı, her gün tekrarlanan küçük çabaların toplamıdır.",
    "Gelecek, ona bugün hazırlananlara aittir.",
    "Büyük başarılar, büyük hayallerle başlar.",
    "Asla vazgeçme. Kaybedenler sadece vazgeçenlerdir.",
    "Zorluklar, başarının değerini artıran süslerdir.",
    "Disiplin, hedefler ile başarı arasındaki köprüdür."
]

DEFAULT_MEDIA = [
    ("Song", "Eye of the Tiger", "Survivor (Motivasyon Patlaması)"),
    ("Song", "Weightless", "Marconi Union (Stres Düşürücü)"),
    ("Song", "Experience", "Ludovico Einaudi (Verimli Çalışma)"),
    ("Podcast", "Tarih Obası", "Tarih Genel Kültür"),
    ("Podcast", "Zihnimin Kıvrımları", "M. Serdar Kuzuloğlu"),
    ("Podcast", "Psikolojinin Ötesinde", "Beyhan Budak (Sınav Kaygısı)")
]
