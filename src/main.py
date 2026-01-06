import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import date
import os
import sys

# Modüler importlar
from config import (
    resource_path, DB_FILE, MISTAKE_IMG_DIR, USER_IMG_PATH, 
    LOGO_PATH, HOCA_LIST_PATH, MOTIVATION_QUOTES
)
from database import (
    init_db, seed_media_recs, load_all_from_db, 
    ensure_default_kpss_topics, ensure_specific_exams
)
from ui_tabs import HomeTabMixin
from study_tabs import StudyTabsMixin
from extra_tabs import ExtraTabsMixin

class KPSSTrackerApp(ctk.CTk, HomeTabMixin, StudyTabsMixin, ExtraTabsMixin):
    def __init__(self):
        super().__init__()
        self.title("KPSS Takip Sistemi 2026")
        self.geometry("1300x850")
        
        # Maximize on startup
        try: self.after(0, lambda: self.state('zoomed'))
        except: pass

        # App Icon
        try:
            icon_path = resource_path("assets/logo.jpg")
            if os.path.exists(icon_path):
                icon_img = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, icon_img)
        except: pass

        # DB Setup
        init_db()
        seed_media_recs()
        ensure_default_kpss_topics()
        ensure_specific_exams()
        self.data = load_all_from_db()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.apply_global_style()
        self.create_widgets()
        self.update_summary()
        self.schedule_reminder_check()

    def apply_global_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#F4ECD8", fieldbackground="#F4ECD8", foreground="black", font=("Segoe UI", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"), background="#e0e0e0")
        style.map("Treeview", background=[("selected", "#d1c4e9")])

    def create_widgets(self):
        self.tabview = ctk.CTkTabview(self, segmented_button_fg_color="transparent", 
                                     segmented_button_selected_color="transparent",
                                     segmented_button_unselected_color="transparent")
        self.tabview.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        # Hide the default tab buttons
        self.tabview._segmented_button.grid_forget()
        
        self.tab_home = self.tabview.add("Ana Sayfa")
        self.tab_progress = self.tabview.add("Ders İlerleme")
        self.tab_mistake = self.tabview.add("Yanlış Defteri")
        self.tab_goals = self.tabview.add("Hedefler")
        self.tab_tests = self.tabview.add("Test & Deneme")
        self.tab_net = self.tabview.add("Net Hesapla")
        self.tab_exams = self.tabview.add("Sınavlar")
        self.tab_motivation = self.tabview.add("Motivasyon")
        
        self.build_home_tab()
        self.build_progress_tab()
        self.build_mistake_tab()
        self.build_goals_tab()
        self.build_tests_tab()
        self.build_net_calculator_tab()
        self.build_exams_tab()
        self.build_motivation_tab()

    def update_summary(self):
        kpss_date = date(2026, 9, 6); basvuru_start = date(2026, 7, 29); today = date.today()
        diff_kpss = (kpss_date - today).days; diff_basvuru = (basvuru_start - today).days
        self.lbl_kpss_cw.configure(text=str(diff_kpss))
        if hasattr(self, 'lbl_app_cw'):
            if diff_basvuru > 0: self.lbl_app_cw.configure(text=f"Başvurulara {diff_basvuru} gün var")
            else: self.lbl_app_cw.configure(text="Başvurular Başladı!")
        
        self.draw_heatmap()
        self.load_progress_trees()
        self.update_charts()

    def schedule_reminder_check(self):
        # Placeholder for background checks
        self.after(60000, self.schedule_reminder_check)

if __name__ == "__main__":
    app = KPSSTrackerApp()
    app.mainloop()
