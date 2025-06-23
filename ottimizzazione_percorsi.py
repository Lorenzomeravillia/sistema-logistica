# Sistema di Ottimizzazione Percorsi Logistici
# Calcola il percorso ottimale per le consegne

import math
import random
from typing import List, Tuple, Dict

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

# Esempio di utilizzo
if __name__ == "__main__":
    # Coordinate del deposito centrale (es. Milano)
    ottimizzatore = OttimizzatorePercorsi(45.4642, 9.1900)
    
    # Aggiungi alcune consegne di esempio
    consegne_esempio = [
        PuntoConsegna("C001", "Cliente Milano Centro", 45.4641, 9.1919, 150),
        PuntoConsegna("C002", "Cliente Monza", 45.5845, 9.2744, 200),
        PuntoConsegna("C003", "Cliente Bergamo", 45.6983, 9.6773, 300),
        PuntoConsegna("C004", "Cliente Como", 45.8080, 9.0852, 180),
        PuntoConsegna("C005", "Cliente Lodi", 45.3138, 9.5019, 250),
        PuntoConsegna("C006", "Cliente Pavia", 45.1847, 9.1582, 120),
        PuntoConsegna("C007", "Cliente Brescia", 45.5416, 10.2118, 280),
        PuntoConsegna("C008", "Cliente Varese", 45.8206, 8.8250, 160),
    ]
    
    for consegna in consegne_esempio:
        ottimizzatore.aggiungi_consegna(consegna)
        
    # Dividi le consegne per veicoli con capacità 500 kg
    veicoli = ottimizzatore.dividi_per_veicoli(500)
    
    # Genera il report
    ottimizzatore.genera_report_percorsi(veicoli)