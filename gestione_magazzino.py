# Sistema di Gestione Magazzino Logistico
# Questo modulo gestisce l'inventario di un magazzino

import datetime
import json
import tkinter as tk
from tkinter import ttk, messagebox

class Magazzino:
    """Classe principale per la gestione del magazzino"""
    
    def __init__(self, nome_magazzino):
        self.nome = nome_magazzino
        self.inventario = {}
        self.movimenti = []
        
    def aggiungi_prodotto(self, codice, nome, quantita, posizione):
        """Aggiunge un nuovo prodotto al magazzino"""
        if codice in self.inventario:
            print(f"Prodotto {codice} già esistente. Usa 'aggiorna_quantita' per modificare.")
            return False
            
        self.inventario[codice] = {
            'nome': nome,
            'quantita': quantita,
            'posizione': posizione,
            'data_inserimento': datetime.datetime.now().isoformat()
        }
        
        self.registra_movimento('INGRESSO', codice, quantita)
        print(f"Prodotto {nome} aggiunto con successo!")
        return True
        
    def aggiorna_quantita(self, codice, quantita, tipo_movimento):
        """Aggiorna la quantità di un prodotto esistente"""
        if codice not in self.inventario:
            print(f"Prodotto {codice} non trovato!")
            return False
            
        if tipo_movimento == 'INGRESSO':
            self.inventario[codice]['quantita'] += quantita
        elif tipo_movimento == 'USCITA':
            if self.inventario[codice]['quantita'] >= quantita:
                self.inventario[codice]['quantita'] -= quantita
            else:
                print("Quantità insufficiente!")
                return False
                
        self.registra_movimento(tipo_movimento, codice, quantita)
        return True
        
    def registra_movimento(self, tipo, codice, quantita):
        """Registra ogni movimento di magazzino"""
        movimento = {
            'timestamp': datetime.datetime.now().isoformat(),
            'tipo': tipo,
            'codice_prodotto': codice,
            'quantita': quantita
        }
        self.movimenti.append(movimento)
        
    def cerca_prodotto(self, codice):
        """Cerca un prodotto per codice"""
        return self.inventario.get(codice, None)
        
    def report_inventario(self):
        """Genera un report dell'inventario attuale"""
        print(f"\n=== INVENTARIO MAGAZZINO {self.nome} ===")
        print(f"Data report: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("-" * 60)
        
        for codice, info in self.inventario.items():
            print(f"Codice: {codice}")
            print(f"  Nome: {info['nome']}")
            print(f"  Quantità: {info['quantita']}")
            print(f"  Posizione: {info['posizione']}")
            print("-" * 60)
            
    def salva_dati(self, filename):
        """Salva i dati del magazzino in un file JSON"""
        dati = {
            'nome_magazzino': self.nome,
            'inventario': self.inventario,
            'movimenti': self.movimenti
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)
        print(f"Dati salvati in {filename}")
        
    def carica_dati(self, filename):
        """Carica i dati del magazzino da un file JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                dati = json.load(f)
                
            self.nome = dati['nome_magazzino']
            self.inventario = dati['inventario']
            self.movimenti = dati['movimenti']
            print(f"Dati caricati da {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} non trovato!")
            return False

class MagazzinoGUI:
    """Interfaccia grafica semplificata per il magazzino"""

    def __init__(self, magazzino: Magazzino):
        self.magazzino = magazzino
        self.root = tk.Tk()
        self.root.title(f"Magazzino {magazzino.nome}")
        self._build_widgets()

    def _build_widgets(self):
        frame_add = ttk.LabelFrame(self.root, text="Aggiungi prodotto")
        frame_add.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame_add, text="Codice").grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(frame_add, text="Nome").grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(frame_add, text="Quantità").grid(row=0, column=2, padx=2, pady=2)
        ttk.Label(frame_add, text="Posizione").grid(row=0, column=3, padx=2, pady=2)

        self.codice_entry = ttk.Entry(frame_add, width=10)
        self.nome_entry = ttk.Entry(frame_add, width=20)
        self.qta_entry = ttk.Entry(frame_add, width=6)
        self.pos_entry = ttk.Entry(frame_add, width=6)
        self.codice_entry.grid(row=1, column=0, padx=2, pady=2)
        self.nome_entry.grid(row=1, column=1, padx=2, pady=2)
        self.qta_entry.grid(row=1, column=2, padx=2, pady=2)
        self.pos_entry.grid(row=1, column=3, padx=2, pady=2)
        ttk.Button(frame_add, text="Aggiungi", command=self.aggiungi).grid(row=1, column=4, padx=4)

        frame_mov = ttk.LabelFrame(self.root, text="Movimento")
        frame_mov.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame_mov, text="Codice").grid(row=0, column=0, padx=2)
        ttk.Label(frame_mov, text="Quantità").grid(row=0, column=1, padx=2)
        ttk.Label(frame_mov, text="Tipo").grid(row=0, column=2, padx=2)

        self.codice_mov = ttk.Entry(frame_mov, width=10)
        self.qta_mov = ttk.Entry(frame_mov, width=6)
        self.tipo_mov = ttk.Combobox(frame_mov, values=["INGRESSO", "USCITA"], width=10)
        self.tipo_mov.current(0)
        self.codice_mov.grid(row=1, column=0, padx=2)
        self.qta_mov.grid(row=1, column=1, padx=2)
        self.tipo_mov.grid(row=1, column=2, padx=2)
        ttk.Button(frame_mov, text="Registra", command=self.movimento).grid(row=1, column=3, padx=4)

        frame_report = ttk.LabelFrame(self.root, text="Inventario")
        frame_report.pack(fill="both", expand=True, padx=5, pady=5)

        self.report_text = tk.Text(frame_report, height=10, width=60)
        self.report_text.pack(fill="both", expand=True)
        ttk.Button(self.root, text="Aggiorna report", command=self.aggiorna_report).pack(pady=5)

    def aggiungi(self):
        codice = self.codice_entry.get()
        nome = self.nome_entry.get()
        try:
            qta = int(self.qta_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Quantità non valida")
            return
        pos = self.pos_entry.get()
        if self.magazzino.aggiungi_prodotto(codice, nome, qta, pos):
            self.aggiorna_report()

    def movimento(self):
        codice = self.codice_mov.get()
        try:
            qta = int(self.qta_mov.get())
        except ValueError:
            messagebox.showerror("Errore", "Quantità non valida")
            return
        tipo = self.tipo_mov.get()
        if self.magazzino.aggiorna_quantita(codice, qta, tipo):
            self.aggiorna_report()

    def aggiorna_report(self):
        self.report_text.delete(1.0, tk.END)
        lines = []
        for codice, info in self.magazzino.inventario.items():
            lines.append(f"{codice}: {info['nome']} - {info['quantita']} pezzi @ {info['posizione']}")
        self.report_text.insert(tk.END, "\n".join(lines))

    def run(self):
        self.aggiorna_report()
        self.root.mainloop()


if __name__ == "__main__":
    gui = MagazzinoGUI(Magazzino("Magazzino Demo"))
    gui.run()
