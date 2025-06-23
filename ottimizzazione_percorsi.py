# Sistema di Ottimizzazione Percorsi Logistici
# Calcola il percorso ottimale per le consegne

import math
import random
from typing import List, Tuple, Dict
import tkinter as tk
from tkinter import ttk

class PuntoConsegna:
    """Rappresenta un punto di consegna"""
    
    def __init__(self, id_cliente, nome, latitudine, longitudine, peso_merce):
        self.id = id_cliente
        self.nome = nome
        self.lat = latitudine
        self.lon = longitudine
        self.peso_merce = peso_merce
        
    def __str__(self):
        return f"{self.nome} ({self.peso_merce}kg)"

class OttimizzatorePercorsi:
    """Ottimizza i percorsi di consegna usando algoritmi euristici"""
    
    def __init__(self, deposito_lat, deposito_lon):
        self.deposito = (deposito_lat, deposito_lon)
        self.consegne = []
        
    def aggiungi_consegna(self, punto: PuntoConsegna):
        """Aggiunge un punto di consegna"""
        self.consegne.append(punto)
        
    def calcola_distanza(self, punto1: Tuple[float, float], punto2: Tuple[float, float]) -> float:
        """Calcola la distanza euclidea tra due punti (approssimazione)"""
        # In un sistema reale useresti la formula di Haversine per coordinate GPS
        lat1, lon1 = punto1
        lat2, lon2 = punto2
        
        # Conversione gradi in km (approssimativa)
        diff_lat = (lat2 - lat1) * 111  # 1 grado lat ≈ 111 km
        diff_lon = (lon2 - lon1) * 111 * math.cos(math.radians(lat1))
        
        return math.sqrt(diff_lat**2 + diff_lon**2)
        
    def percorso_nearest_neighbor(self) -> List[PuntoConsegna]:
        """Algoritmo del vicino più vicino per ottimizzare il percorso"""
        if not self.consegne:
            return []
            
        percorso = []
        consegne_rimanenti = self.consegne.copy()
        posizione_attuale = self.deposito
        
        while consegne_rimanenti:
            # Trova il punto più vicino
            punto_piu_vicino = None
            distanza_minima = float('inf')
            
            for punto in consegne_rimanenti:
                dist = self.calcola_distanza(posizione_attuale, (punto.lat, punto.lon))
                if dist < distanza_minima:
                    distanza_minima = dist
                    punto_piu_vicino = punto
                    
            # Aggiungi al percorso e aggiorna posizione
            percorso.append(punto_piu_vicino)
            consegne_rimanenti.remove(punto_piu_vicino)
            posizione_attuale = (punto_piu_vicino.lat, punto_piu_vicino.lon)
            
        return percorso
        
    def dividi_per_veicoli(self, capacita_veicolo: float) -> Dict[int, List[PuntoConsegna]]:
        """Divide le consegne tra più veicoli in base alla capacità"""
        percorso_ottimizzato = self.percorso_nearest_neighbor()
        veicoli = {}
        veicolo_corrente = 1
        carico_corrente = 0
        consegne_veicolo = []
        
        for punto in percorso_ottimizzato:
            if carico_corrente + punto.peso_merce > capacita_veicolo:
                # Assegna al veicolo corrente e passa al successivo
                veicoli[veicolo_corrente] = consegne_veicolo
                veicolo_corrente += 1
                consegne_veicolo = [punto]
                carico_corrente = punto.peso_merce
            else:
                consegne_veicolo.append(punto)
                carico_corrente += punto.peso_merce
                
        # Assegna l'ultimo veicolo
        if consegne_veicolo:
            veicoli[veicolo_corrente] = consegne_veicolo
            
        return veicoli
        
    def calcola_distanza_totale(self, percorso: List[PuntoConsegna]) -> float:
        """Calcola la distanza totale di un percorso"""
        if not percorso:
            return 0
            
        distanza_totale = 0
        posizione_attuale = self.deposito
        
        for punto in percorso:
            distanza_totale += self.calcola_distanza(posizione_attuale, (punto.lat, punto.lon))
            posizione_attuale = (punto.lat, punto.lon)
            
        # Ritorno al deposito
        distanza_totale += self.calcola_distanza(posizione_attuale, self.deposito)
        
        return distanza_totale
        
    def genera_report_percorsi(self, veicoli: Dict[int, List[PuntoConsegna]]):
        """Genera un report dettagliato dei percorsi"""
        print("\n=== REPORT OTTIMIZZAZIONE PERCORSI ===")
        print(f"Deposito: {self.deposito[0]:.4f}, {self.deposito[1]:.4f}")
        print(f"Totale consegne: {len(self.consegne)}")
        print(f"Veicoli necessari: {len(veicoli)}")
        print("-" * 60)
        
        distanza_totale_flotta = 0
        
        for veicolo_id, consegne in veicoli.items():
            print(f"\nVEICOLO {veicolo_id}:")
            peso_totale = sum(p.peso_merce for p in consegne)
            distanza_percorso = self.calcola_distanza_totale(consegne)
            distanza_totale_flotta += distanza_percorso
            
            print(f"  Numero fermate: {len(consegne)}")
            print(f"  Peso totale: {peso_totale:.1f} kg")
            print(f"  Distanza stimata: {distanza_percorso:.1f} km")
            print(f"  Percorso:")
            
            for i, punto in enumerate(consegne, 1):
                print(f"    {i}. {punto}")
                
        print("\n" + "-" * 60)
        print(f"DISTANZA TOTALE FLOTTA: {distanza_totale_flotta:.1f} km")

class OttimizzatoreGUI:
    """Interfaccia grafica semplificata per l'ottimizzazione"""

    def __init__(self):
        self.ottimizzatore = OttimizzatorePercorsi(45.4642, 9.1900)
        self.root = tk.Tk()
        self.root.title("Ottimizzazione Percorsi")
        self._build_widgets()

    def _build_widgets(self):
        frm_add = ttk.LabelFrame(self.root, text="Aggiungi consegna")
        frm_add.pack(fill="x", padx=5, pady=5)

        labels = ["ID", "Nome", "Lat", "Lon", "Peso"]
        self.entries = []
        for i, label in enumerate(labels):
            ttk.Label(frm_add, text=label).grid(row=0, column=i, padx=2)
            ent = ttk.Entry(frm_add, width=10)
            ent.grid(row=1, column=i, padx=2)
            self.entries.append(ent)
        ttk.Button(frm_add, text="Aggiungi", command=self.aggiungi).grid(row=1, column=len(labels), padx=4)

        frm_cap = ttk.Frame(self.root)
        frm_cap.pack(fill="x", padx=5, pady=5)
        ttk.Label(frm_cap, text="Capacità veicolo kg:").grid(row=0, column=0)
        self.cap_entry = ttk.Entry(frm_cap, width=8)
        self.cap_entry.insert(0, "500")
        self.cap_entry.grid(row=0, column=1)
        ttk.Button(frm_cap, text="Ottimizza", command=self.ottimizza).grid(row=0, column=2, padx=4)

        self.report = tk.Text(self.root, height=15, width=70)
        self.report.pack(fill="both", expand=True, padx=5, pady=5)

    def aggiungi(self):
        try:
            idc, nome, lat, lon, peso = [e.get() for e in self.entries]
            lat = float(lat)
            lon = float(lon)
            peso = float(peso)
        except ValueError:
            return
        self.ottimizzatore.aggiungi_consegna(PuntoConsegna(idc, nome, lat, lon, peso))
        for e in self.entries:
            e.delete(0, tk.END)

    def ottimizza(self):
        try:
            cap = float(self.cap_entry.get())
        except ValueError:
            cap = 500
        veicoli = self.ottimizzatore.dividi_per_veicoli(cap)
        self.report.delete(1.0, tk.END)
        for vid, consegne in veicoli.items():
            self.report.insert(tk.END, f"\nVEICOLO {vid}\n")
            for p in consegne:
                self.report.insert(tk.END, f"  - {p}\n")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = OttimizzatoreGUI()
    gui.run()
