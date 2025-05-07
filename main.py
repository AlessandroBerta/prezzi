from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from plyer import gps
import sqlite3
from datetime import datetime

DB = "prezzi.db"

def setup_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rilevamenti (
            barcode TEXT, nome TEXT, prezzo REAL, supermercato TEXT,
            lat REAL, lon REAL, data TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS supermercati (
            nome TEXT, lat REAL, lon REAL
        )
    ''')
    conn.commit()
    conn.close()

def salva_rilevamento(barcode, nome, prezzo, supermercato, lat, lon):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO rilevamenti VALUES (?, ?, ?, ?, ?, ?, ?)",
              (barcode, nome, prezzo, supermercato, lat, lon, data))
    conn.commit()
    conn.close()

class ScanScreen(Screen):
    def on_enter(self):
        self.show_dialog("Funzionalità di scansione non implementata in questa versione.")

    def show_dialog(self, text):
        MDDialog(title="Info", text=text).open()

class ResultScreen(Screen):
    def update(self, barcode, nome, prezzo, media, emoji, storico):
        self.ids.prod_label.text = f"{nome} ({barcode})"
        self.ids.price_current.text = f"{prezzo:.2f} €"
        self.ids.price_avg.text = f"{media:.2f} €"
        self.ids.smile.text = emoji
        self.ids.history.text = "\n".join(f"{d} - {p:.2f} €" for p, d in storico)

class MainApp(MDApp):
    def build(self):
        setup_db()
        return Builder.load_file("main.kv")

MainApp().run()
