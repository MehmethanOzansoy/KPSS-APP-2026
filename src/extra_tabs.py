import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from datetime import datetime, date
import os
import sqlite3
import random
import shutil
from PIL import Image, ImageGrab
from config import DB_FILE, MISTAKE_IMG_DIR, USER_IMG_PATH, MOTIVATION_QUOTES

class ExtraTabsMixin:
    # ---- 3. MISTAKES ----
    def build_mistake_tab(self):
        self.tab_mistake.grid_columnconfigure(1, weight=1); self.tab_mistake.grid_rowconfigure(0, weight=1)
        l = ctk.CTkFrame(self.tab_mistake, width=250); l.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        ctk.CTkLabel(l, text="Yanlış Ekle", font=("Roboto", 16, "bold")).pack(pady=10)
        self.ent_mis_ders = ctk.CTkEntry(l, placeholder_text="Ders"); self.ent_mis_ders.pack(pady=5, padx=5, fill="x")
        self.ent_mis_konu = ctk.CTkEntry(l, placeholder_text="Konu"); self.ent_mis_konu.pack(pady=5, padx=5, fill="x")
        self.ent_mis_not = ctk.CTkTextbox(l, height=100); self.ent_mis_not.pack(pady=5, padx=5, fill="x")
        self.lbl_mis_prev = ctk.CTkLabel(l, text="Resim Yok", height=100, fg_color="gray"); self.lbl_mis_prev.pack(pady=5, padx=5, fill="x")
        self.curr_paste_img = None
        ctk.CTkButton(l, text="Yapıştır", command=self.paste_img).pack(pady=5)
        ctk.CTkButton(l, text="Dosya Seç", command=self.select_img).pack(pady=5)
        ctk.CTkButton(l, text="Kaydet", command=self.save_mistake, fg_color="green").pack(pady=10)
        r = ctk.CTkFrame(self.tab_mistake); r.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        r.grid_rowconfigure(0, weight=1); r.grid_columnconfigure(0, weight=1)
        self.tree_mistake = ttk.Treeview(r, columns=("tarih", "ders", "konu"), show="headings")
        self.tree_mistake.heading("tarih", text="Tarih"); self.tree_mistake.heading("ders", text="Ders"); self.tree_mistake.heading("konu", text="Konu")
        self.tree_mistake.grid(row=0, column=0, sticky="nsew"); self.tree_mistake.bind("<<TreeviewSelect>>", self.on_mistake_sel)
        d = ctk.CTkFrame(r, height=150); d.grid(row=1, column=0, sticky="ew", pady=(10,0))
        self.txt_mistake_det = ctk.CTkTextbox(d, height=80); self.txt_mistake_det.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        b = ctk.CTkFrame(d, fg_color="transparent"); b.pack(side="right", fill="y")
        ctk.CTkButton(b, text="Resmi Aç", command=self.open_mistake_img).pack(pady=5, padx=5)
        ctk.CTkButton(b, text="Sil", fg_color="red", command=self.del_mistake).pack(pady=5, padx=5)
        self.load_mistakes()

    def paste_img(self):
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image): self.curr_paste_img = img; self.show_preview(img)
        except: pass

    def select_img(self):
        p = filedialog.askopenfilename(); 
        if p: img = Image.open(p); self.curr_paste_img = img; self.show_preview(img)

    def show_preview(self, img):
        try:
            prev = img.copy(); prev.thumbnail((200, 100))
            ci = ctk.CTkImage(light_image=prev, dark_image=prev, size=prev.size); self.lbl_mis_prev.configure(image=ci, text="")
        except: pass

    def save_mistake(self):
        d, k, n, p = self.ent_mis_ders.get(), self.ent_mis_konu.get(), self.ent_mis_not.get("0.0", "end"), ""
        if self.curr_paste_img:
            fn = f"mistake_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"; p = os.path.join(MISTAKE_IMG_DIR, fn); self.curr_paste_img.save(p)
        conn = sqlite3.connect(DB_FILE); conn.execute("INSERT INTO mistakes (ders, konu, not_icerik, resim_yolu, tarih) VALUES (?,?,?,?,?)", (d, k, n, p, date.today().isoformat())); conn.commit(); conn.close(); self.load_mistakes(); self.curr_paste_img = None; self.lbl_mis_prev.configure(image=None, text="Kaydedildi")

    def load_mistakes(self):
        from database import load_all_from_db
        self.data = load_all_from_db()
        for i in self.tree_mistake.get_children(): self.tree_mistake.delete(i)
        for m in self.data["mistakes"]: self.tree_mistake.insert("", "end", iid=str(m["id"]), values=(m["tarih"], m["ders"], m["konu"]))

    def on_mistake_sel(self, e):
        sel = self.tree_mistake.selection()
        if not sel: return
        mid = int(sel[0]); r = next((x for x in self.data["mistakes"] if x["id"]==mid), None)
        if r: self.txt_mistake_det.delete("0.0", "end"); self.txt_mistake_det.insert("0.0", f"Not: {r['not_icerik']}")

    def open_mistake_img(self):
        sel = self.tree_mistake.selection()
        if not sel: return
        mid = int(sel[0]); r = next((x for x in self.data["mistakes"] if x["id"]==mid), None)
        if r and r["resim_yolu"] and os.path.exists(r["resim_yolu"]): os.startfile(r["resim_yolu"])

    def del_mistake(self):
        sel = self.tree_mistake.selection()
        if not sel or not messagebox.askyesno("Sil", "Silinsin mi?"): return
        mid = int(sel[0]); conn = sqlite3.connect(DB_FILE); conn.execute("DELETE FROM mistakes WHERE id=?", (mid,)); conn.commit(); conn.close(); self.load_mistakes()

    # ---- 7. EXAMS ----
    def build_exams_tab(self):
        self.tab_exams.grid_columnconfigure(0, weight=1); self.tab_exams.grid_rowconfigure(1, weight=1)
        f = ctk.CTkFrame(self.tab_exams); f.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.ent_exam_name = ctk.CTkEntry(f, placeholder_text="Sınav Adı"); self.ent_exam_name.pack(side="left", padx=5)
        self.ent_exam_date = ctk.CTkEntry(f, placeholder_text="YYYY-AA-GG"); self.ent_exam_date.pack(side="left", padx=5)
        self.ent_exam_type = ctk.CTkComboBox(f, values=["KPSS", "Başvuru", "Diğer"]); self.ent_exam_type.pack(side="left", padx=5)
        ctk.CTkButton(f, text="Ekle", command=self.add_exam).pack(side="left", padx=5)
        self.tree_exams = ttk.Treeview(self.tab_exams, columns=("ad", "tur", "tarih", "kalan"), show="headings")
        self.tree_exams.heading("ad", text="Ad"); self.tree_exams.heading("tur", text="Tür"); self.tree_exams.heading("tarih", text="Tarih"); self.tree_exams.heading("kalan", text="Kalan")
        self.tree_exams.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        ctk.CTkButton(self.tab_exams, text="Sil", fg_color="red", command=self.delete_exam).grid(row=2, column=0, pady=5, sticky="e", padx=10)
        self.load_exams()

    def add_exam(self):
        n, d, t = self.ent_exam_name.get(), self.ent_exam_date.get(), self.ent_exam_type.get()
        try: datetime.strptime(d, "%Y-%m-%d")
        except: return
        conn = sqlite3.connect(DB_FILE); conn.execute("INSERT INTO exams (ad, tur, tarih) VALUES (?,?,?)", (n, t, d)); conn.commit(); conn.close(); self.load_exams()

    def load_exams(self):
        from database import load_all_from_db
        self.data = load_all_from_db(); td = date.today()
        for i in self.tree_exams.get_children(): self.tree_exams.delete(i)
        for e in self.data["exams"]:
            try: dt = datetime.strptime(e["tarih"], "%Y-%m-%d").date(); diff = (dt - td).days; kalan = f"{diff} G" if diff >= 0 else "Geçti"
            except: kalan = "Hata"
            self.tree_exams.insert("", "end", iid=str(e["id"]), values=(e["ad"], e["tur"], e["tarih"], kalan))

    def delete_exam(self):
        sel = self.tree_exams.selection()
        if not sel: return
        eid = int(sel[0]); conn = sqlite3.connect(DB_FILE); conn.execute("DELETE FROM exams WHERE id=?", (eid,)); conn.commit(); conn.close(); self.load_exams()

    # ---- 8. MOTIVATION ----
    def build_motivation_tab(self):
        self.tab_motivation.grid_columnconfigure(0, weight=1); self.tab_motivation.grid_columnconfigure(1, weight=1); self.tab_motivation.grid_rowconfigure(0, weight=1)
        l = ctk.CTkFrame(self.tab_motivation); l.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.lbl_quote = ctk.CTkLabel(l, text="...", font=("Georgia", 18, "italic"), wraplength=400); self.lbl_quote.pack(pady=20)
        ctk.CTkButton(l, text="Yeni Söz", command=self.refresh_quote).pack()
        self.mot_img_lbl = ctk.CTkLabel(l, text="Resim", width=300, height=200, fg_color="gray"); self.mot_img_lbl.pack(pady=10)
        self.mot_images = [USER_IMG_PATH] if os.path.exists(USER_IMG_PATH) else []
        if os.path.exists("docs"):
            for f in os.listdir("docs"):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')): self.mot_images.append(os.path.join("docs", f))
        self.curr_mot_idx = 0
        r = ctk.CTkFrame(self.tab_motivation); r.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frm_alert = ctk.CTkFrame(r, fg_color="gray"); self.frm_alert.pack(fill="x", padx=10, pady=10)
        self.lbl_alert = ctk.CTkLabel(self.frm_alert, text="...", font=("Segoe UI", 16, "bold"), text_color="white"); self.lbl_alert.pack(pady=10)
        self.tree_tasks = ttk.Treeview(r, columns=("id", "prio", "task", "status"), show="headings", height=8)
        self.tree_tasks.heading("prio", text="P"); self.tree_tasks.heading("task", text="Görev"); self.tree_tasks.heading("status", text="D"); self.tree_tasks.column("id", width=0, stretch=False); self.tree_tasks.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree_tasks.bind("<Double-1>", self.toggle_task_status)
        self.tree_media = ttk.Treeview(r, columns=("type", "title"), show="headings", height=5)
        self.tree_media.heading("type", text="Tür"); self.tree_media.heading("title", text="Başlık"); self.tree_media.pack(fill="both", expand=True, padx=10, pady=5)
        self.refresh_quote(); self.show_mot_img(0); self.load_media_recs(); self.load_daily_tasks()

    def load_daily_tasks(self):
        from database import load_all_from_db
        self.data = load_all_from_db(); ac = True
        for i in self.tree_tasks.get_children(): self.tree_tasks.delete(i)
        for t in self.data["daily_tasks"]:
            s = "☑" if t["is_completed"] else "⬜"
            if not t["is_completed"]: ac = False
            self.tree_tasks.insert("", "end", iid=str(t["id"]), values=(t["id"], t["priority"], t["task"], s))
        self.frm_alert.configure(fg_color="#43a047" if ac else "#fdd835"); self.lbl_alert.configure(text="Tebrikler! 🎉" if ac else "Hedefler Bekliyor! 💪")

    def toggle_task_status(self, e):
        sel = self.tree_tasks.selection()
        if not sel: return
        tid = int(sel[0]); curr = next((x for x in self.data["daily_tasks"] if x["id"]==tid), None)
        if curr:
            v = 0 if curr["is_completed"] else 1
            conn = sqlite3.connect(DB_FILE); conn.execute("UPDATE daily_tasks SET is_completed = ? WHERE id=?", (v, tid)); conn.commit(); conn.close(); self.load_daily_tasks()

    def refresh_quote(self):
        self.lbl_quote.configure(text=f"“{random.choice(MOTIVATION_QUOTES)}”")

    def show_mot_img(self, i):
        if not self.mot_images: return
        try:
            img = Image.open(self.mot_images[i]); img.thumbnail((300, 200))
            ci = ctk.CTkImage(light_image=img, dark_image=img, size=img.size); self.mot_img_lbl.configure(image=ci, text="")
        except: pass

    def load_media_recs(self):
        from database import load_all_from_db
        self.data = load_all_from_db()
        for i in self.tree_media.get_children(): self.tree_media.delete(i)
        for m in self.data["media"]: self.tree_media.insert("", "end", iid=str(m["id"]), values=(m["type"], m["title"]))
