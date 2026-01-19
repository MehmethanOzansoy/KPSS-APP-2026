import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import customtkinter as ctk
from datetime import datetime, date, timedelta
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import random
import sqlite3

from config import (
    resource_path, DB_FILE, MISTAKE_IMG_DIR, USER_IMG_PATH, 
    LOGO_PATH, HOCA_LIST_PATH, MOTIVATION_QUOTES
)

class HomeTabMixin:
    def build_home_tab(self):
        self.tab_home.grid_columnconfigure(0, weight=1)
        self.tab_home.grid_rowconfigure(0, weight=1)
        
        self.home_main_scroll = ctk.CTkScrollableFrame(self.tab_home, fg_color="transparent")
        self.home_main_scroll.pack(fill="both", expand=True)
        self.home_main_scroll.grid_columnconfigure(0, weight=1)
        self.home_main_scroll.grid_columnconfigure(1, weight=1)

        # 1. Modern Header with Navbar
        header_frame = ctk.CTkFrame(self.home_main_scroll, fg_color="#1e3a5f", height=70, corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo and Title
        logo_title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_title_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        logo_path = resource_path("logo.jpg")
        if not os.path.exists(logo_path):
            logo_path = resource_path("image.png")
            
        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                pil_img.thumbnail((50, 50))
                ctk_logo = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
                ctk.CTkLabel(logo_title_frame, image=ctk_logo, text="").pack(side="left", padx=(0, 10))
            except: pass
        
        ctk.CTkLabel(logo_title_frame, text="KPSS Çalışma Paneli", 
                    font=("Segoe UI", 20, "bold"), text_color="white").pack(side="left")
        
        # Modern Navigation Buttons
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, padx=20, pady=10)
        
        nav_buttons = [
            ("🏠 Ana Sayfa", lambda: self.tabview.set("Ana Sayfa")),
            ("📊 Ders İlerleme", lambda: self.tabview.set("Ders İlerleme")),
            ("📓 Yanlış Defteri", lambda: self.tabview.set("Yanlış Defteri")),
            ("🎯 Hedefler", lambda: self.tabview.set("Hedefler")),
            ("📝 Test & Deneme", lambda: self.tabview.set("Test & Deneme")),
            ("🧠 Net Hesapla", lambda: self.tabview.set("Net Hesapla")),
            ("📅 Sınavlar", lambda: self.tabview.set("Sınavlar")),
            ("💪 Motivasyon", lambda: self.tabview.set("Motivasyon"))
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(nav_frame, text=text, width=100, height=35,
                              fg_color="transparent", hover_color="#2c5282",
                              border_width=0, font=("Segoe UI", 10),
                              command=command)
            btn.pack(side="left", padx=3)
        
        # User Profile
        if os.path.exists(USER_IMG_PATH):
            try:
                prof_img = Image.open(USER_IMG_PATH)
                prof_img.thumbnail((40, 40))
                ctk_prof = ctk.CTkImage(light_image=prof_img, dark_image=prof_img, size=prof_img.size)
                ctk.CTkLabel(header_frame, image=ctk_prof, text="").grid(row=0, column=2, padx=20, pady=10, sticky="e")
            except: pass

        # 2. Countdown Cards (2 columns)
        countdown_container = ctk.CTkFrame(self.home_main_scroll, fg_color="transparent")
        countdown_container.grid(row=1, column=0, columnspan=2, padx=10, pady=20)
        countdown_container.grid_columnconfigure(0, weight=1)
        countdown_container.grid_columnconfigure(1, weight=1)
        
        # KPSS Card (Left)
        kpss_card = ctk.CTkFrame(countdown_container, fg_color="#1e3a5f", corner_radius=15)
        kpss_card.grid(row=0, column=0, padx=10, sticky="ew")
        ctk.CTkLabel(kpss_card, text="⏳ KPSS 2026 Lisans", font=("Segoe UI", 14, "bold"), text_color="#90caf9").pack(pady=(15, 5))
        self.lbl_kpss_cw = ctk.CTkLabel(kpss_card, text="...", font=("Segoe UI", 32, "bold"), text_color="#ffffff")
        self.lbl_kpss_cw.pack(pady=5)
        ctk.CTkLabel(kpss_card, text="Gün Kaldı", font=("Segoe UI", 11), text_color="#b0bec5").pack(pady=(0, 15))
        
        # Application Card (Right)
        app_card = ctk.CTkFrame(countdown_container, fg_color="#2e7d32", corner_radius=15)
        app_card.grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(app_card, text="📅 Başvuru Süreci", font=("Segoe UI", 14, "bold"), text_color="#c5e1a5").pack(pady=(15, 5))
        self.lbl_app_cw = ctk.CTkLabel(app_card, text="...", font=("Segoe UI", 16, "bold"), text_color="#ffffff")
        self.lbl_app_cw.pack(pady=(5, 15))

        # 3. Content Area
        left_side = ctk.CTkFrame(self.home_main_scroll, fg_color="transparent")
        left_side.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        right_side = ctk.CTkFrame(self.home_main_scroll, fg_color="transparent")
        right_side.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        # Heatmap
        heatmap_container = ctk.CTkFrame(left_side, fg_color="white", corner_radius=10)
        heatmap_container.pack(fill="x", pady=(10, 5), padx=5)
        ctk.CTkLabel(heatmap_container, text="📊 Haftalık Soru Isı Haritası", font=("Segoe UI", 16, "bold"), text_color="#1976d2").pack(pady=(12, 8))
        self.canvas_heatmap = tk.Canvas(heatmap_container, width=560, height=160, bg="#fafafa", bd=0, highlightthickness=0)
        self.canvas_heatmap.pack(pady=5, padx=15)
        
        # Legend
        legend_frame = ctk.CTkFrame(heatmap_container, fg_color="transparent")
        legend_frame.pack(pady=(5, 12))
        ctk.CTkLabel(legend_frame, text="Az", font=("Segoe UI", 9), text_color="#666").pack(side="left", padx=3)
        for color in ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]:
            tk.Canvas(legend_frame, width=12, height=12, bg=color, bd=0, highlightthickness=0).pack(side="left", padx=2)
        ctk.CTkLabel(legend_frame, text="Yüksek", font=("Segoe UI", 9), text_color="#666").pack(side="left", padx=3)

        # Hoca Listesi
        hoca_frame = ctk.CTkFrame(left_side, fg_color="#f8f9fa", corner_radius=10)
        hoca_frame.pack(fill="both", expand=True, pady=(15, 0), padx=5)
        ctk.CTkLabel(hoca_frame, text="📚 Önerilen KPSS Hocaları", font=("Segoe UI", 18, "bold"), text_color="#1976d2").pack(pady=12)
        hoca_data = self.load_hoca_listesi()
        scroll_hoca = ctk.CTkScrollableFrame(hoca_frame, height=250, fg_color="transparent")
        scroll_hoca.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        ders_renkleri = {"Turkce": "#e91e63", "Matematik": "#2196f3", "Tarih": "#ff9800", "Cografya": "#4caf50", "Vatandaslik": "#9c27b0"}
        ders_isimleri = {"Turkce": "Türkçe", "Matematik": "Matematik", "Tarih": "Tarih", "Cografya": "Coğrafya", "Vatandaslik": "Vatandaşlık"}
        for ders_key, hocalar in hoca_data.get("KPSS_YouTube_Hocalari", {}).items():
            ders_card = ctk.CTkFrame(scroll_hoca, fg_color="white", corner_radius=8, border_width=2, border_color=ders_renkleri.get(ders_key, "#cccccc"))
            ders_card.pack(fill="x", pady=6, padx=3)
            header_frm = ctk.CTkFrame(ders_card, fg_color=ders_renkleri.get(ders_key, "#cccccc"), corner_radius=6)
            header_frm.pack(fill="x", padx=6, pady=6)
            ctk.CTkLabel(header_frm, text=ders_isimleri.get(ders_key, ders_key), font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=6, padx=8)
            teachers_frm = ctk.CTkFrame(ders_card, fg_color="transparent")
            teachers_frm.pack(fill="x", padx=12, pady=(0, 8))
            for idx, hoca in enumerate(hocalar):
                hoca_row = ctk.CTkFrame(teachers_frm, fg_color="#f5f5f5" if idx % 2 == 0 else "white", corner_radius=4)
                hoca_row.pack(fill="x", pady=2)
                ctk.CTkLabel(hoca_row, text=f"▶ {hoca['name']}", font=("Segoe UI", 11), text_color="#333", anchor="w").pack(side="left", padx=8, pady=5)
                ctk.CTkLabel(hoca_row, text=hoca['platform'], font=("Segoe UI", 9, "italic"), text_color="#666").pack(side="right", padx=8)

        # Right Side Charts
        ctk.CTkLabel(right_side, text="Deneme Net Gelişimi", font=("Segoe UI", 16, "bold")).pack(pady=(10,5))
        self.fig_line, self.ax_line = plt.subplots(figsize=(5, 3), dpi=100)
        self.fig_line.patch.set_facecolor('#F0F0F0')
        self.canvas_line = FigureCanvasTkAgg(self.fig_line, master=right_side)
        self.canvas_line.get_tk_widget().pack(pady=5, fill="x")

        ctk.CTkLabel(right_side, text="Ders Bazlı Başarı", font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.fig_bar, self.ax_bar = plt.subplots(figsize=(5, 3), dpi=100)
        self.fig_bar.patch.set_facecolor('#F0F0F0')
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=right_side)
        self.canvas_bar.get_tk_widget().pack(pady=5, fill="x")

        ctk.CTkLabel(right_side, text="⚠️ Zayıf Konular (<%60)", font=("Segoe UI", 16, "bold"), text_color="#d32f2f").pack(pady=(20, 5))
        self.tree_weak = ttk.Treeview(right_side, columns=("ders", "oran"), show="headings", height=5)
        self.tree_weak.heading("ders", text="Ders / Konu"); self.tree_weak.heading("oran", text="Başarı %")
        self.tree_weak.column("oran", width=80, anchor="center"); self.tree_weak.pack(pady=5, padx=5, fill="x")
        
        self.update_charts()

    def build_quick_note_section(self, parent):
        """Ana sayfaya hızlı not alma ve dinamik motivasyon alanı ekler."""
        note_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        note_frame.pack(fill="x", pady=15, padx=5)
        
        # Başlık ve İkon
        header_frm = ctk.CTkFrame(note_frame, fg_color="transparent")
        header_frm.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frm, text="📝 Hızlı Çalışma Notu", 
                     font=("Segoe UI", 15, "bold"), text_color="#2c3e50").pack(side="left")
        
        # Kaydet Butonu (Küçük ve Şık)
        save_btn = ctk.CTkButton(header_frm, text="Kaydet", width=60, height=24,
                                 fg_color="#27ae60", hover_color="#219150",
                                 command=self.save_quick_note)
        save_btn.pack(side="right")

        # Not Giriş Alanı
        self.txt_quick_note = ctk.CTkTextbox(note_frame, height=80, font=("Segoe UI", 12),
                                            fg_color="#fdfdfd", border_width=1, border_color="#ecf0f1")
        self.txt_quick_note.pack(fill="x", padx=10, pady=(0, 10))
        
        # Veritabanından veya dosyadan eski notu yükle
        self.load_quick_note()

        # Dinamik Motivasyon Sözü (Alt Bilgi)
        quote_frame = ctk.CTkFrame(note_frame, fg_color="#f8f9fa", corner_radius=5)
        quote_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        random_quote = random.choice(MOTIVATION_QUOTES) if 'MOTIVATION_QUOTES' in globals() else "Başarı azim gerektirir."
        ctk.CTkLabel(quote_frame, text=f"💡 {random_quote}", 
                     font=("Segoe UI", 10, "italic"), text_color="#7f8c8d", wraplength=350).pack(pady=5)

    def save_quick_note(self):
        """Notu güvenli bir şekilde kaydeder."""
        note_content = self.txt_quick_note.get("1.0", "end-1c")
        try:
            # Notu hem belleğe hem dosyaya yaz (Persistance)
            with open(resource_path("assets/quick_note.txt"), "w", encoding="utf-8") as f:
                f.write(note_content)
            messagebox.showinfo("Başarılı", "Çalışma notun kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")

    def load_quick_note(self):
        """Eski notu yükler."""
        note_path = resource_path("assets/quick_note.txt")
        if os.path.exists(note_path):
            try:
                with open(note_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.txt_quick_note.insert("1.0", content)
            except: pass

    def update_charts(self):
        self.ax_line.clear()
        dates = []; nets = []
        sorted_trials = sorted(self.data["trials"], key=lambda k: k.get('tarih', ''))
        for t in sorted_trials:
            try:
                d_obj = datetime.strptime(t["tarih"], "%Y-%m-%d")
                dates.append(d_obj.strftime("%d/%m"))
                nets.append(t.get("toplam_net", t.get("net", 0)))
            except: pass
        if dates and len(dates) == len(nets):
            self.ax_line.plot(dates, nets, marker='o', color='#1976d2', linewidth=2)
            self.ax_line.grid(True, linestyle='--', alpha=0.5)
        else:
            self.ax_line.text(0.5, 0.5, "Henüz deneme kaydı yok.", ha="center", va="center", transform=self.ax_line.transAxes)
        try: self.fig_line.tight_layout()
        except: pass
        self.canvas_line.draw()

        self.ax_bar.clear()
        subjects = ["Türkçe", "Matematik", "Tarih", "Coğrafya", "Vatandaşlık"]
        success_rates = []; colors = ["#ef5350", "#42a5f5", "#ffa726", "#66bb6a", "#ab47bc"]
        test_stats = {s: [0, 0] for s in subjects}
        for t in self.data["tests"]:
            if t["ders"] in test_stats:
                test_stats[t["ders"]][0] += t["dogru"]
                test_stats[t["ders"]][1] += (t["dogru"] + t["yanlis"])
        for s in subjects:
            cor, tot = test_stats[s]
            success_rates.append((cor / tot * 100) if tot > 0 else 0)
        bars = self.ax_bar.bar(subjects, success_rates, color=colors, width=0.6)
        self.ax_bar.set_ylim(0, 100)
        for bar in bars:
            h = bar.get_height()
            if h > 0: self.ax_bar.text(bar.get_x() + bar.get_width()/2., h, f'%{int(h)}', ha='center', va='bottom', fontsize=8)
        try: self.fig_bar.tight_layout()
        except: pass
        self.canvas_bar.draw()

    def draw_heatmap(self):
        self.canvas_heatmap.delete("all")
        cols, rows, cell_size, gap = 53, 7, 14, 4
        data_map = {}
        for t in self.data["tests"]: data_map[t["tarih"]] = data_map.get(t["tarih"], 0) + (t["dogru"] + t["yanlis"])
        for g in self.data["goals"]: data_map[g["tarih"]] = data_map.get(g["tarih"], 0) + g["cozulen"]
        end = date.today(); start = end - timedelta(days=(cols*rows)-1); curr = start
        for c in range(cols):
            for r in range(rows):
                val = data_map.get(curr.isoformat(), 0)
                if val == 0: color = "#ebedf0"
                elif val < 30: color = "#c6e48b"
                elif val < 60: color = "#7bc96f"
                elif val < 100: color = "#239a3b"
                elif val < 150: color = "#196127"
                else: color = "#0d4429"
                x0, y0 = c * (cell_size + gap) + 20, r * (cell_size + gap) + 15
                self.canvas_heatmap.create_rectangle(x0, y0, x0+cell_size, y0+cell_size, fill=color, outline="", tags=f"cell_{c}_{r}")
                self.canvas_heatmap.tag_bind(f"cell_{c}_{r}", "<Enter>", lambda e, d=curr.isoformat(), v=val: self.show_heatmap_tooltip(e, d, v))
                self.canvas_heatmap.tag_bind(f"cell_{c}_{r}", "<Leave>", lambda e: self.hide_heatmap_tooltip())
                curr += timedelta(days=1)
        self.update_weak_topics()

    def show_heatmap_tooltip(self, event, date_str, value):
        try:
            tooltip_text = f"{date_str}: {value} soru"
            self.hide_heatmap_tooltip()
            x, y = event.x, event.y
            self.heatmap_tooltip = self.canvas_heatmap.create_rectangle(x+10, y-25, x+120, y-5, fill="#333", outline="")
            self.heatmap_tooltip_text = self.canvas_heatmap.create_text(x+65, y-15, text=tooltip_text, fill="white", font=("Segoe UI", 9))
        except: pass

    def hide_heatmap_tooltip(self):
        try:
            if hasattr(self, 'heatmap_tooltip'):
                self.canvas_heatmap.delete(self.heatmap_tooltip)
                self.canvas_heatmap.delete(self.heatmap_tooltip_text)
        except: pass

    def load_hoca_listesi(self):
        hf = resource_path("assets/hoca_listesi.json")
        if os.path.exists(hf):
            try:
                with open(hf, "r", encoding="utf-8") as f: return json.load(f)
            except: pass
        return {"KPSS_YouTube_Hocalari": {}}
