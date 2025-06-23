# Sistema di Gestione Magazzino Logistico
# Questo modulo gestisce l'inventario di un magazzino

import datetime
import json

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

# Esempio di utilizzo
if __name__ == "__main__":
    # Crea un nuovo magazzino
    magazzino = Magazzino("Milano Nord")
    
    # Aggiungi alcuni prodotti
    magazzino.aggiungi_prodotto("PRD001", "Scatole cartone 50x40x30", 100, "A1-01")
    magazzino.aggiungi_prodotto("PRD002", "Pallet EUR", 50, "B2-05")
    magazzino.aggiungi_prodotto("PRD003", "Film estensibile", 200, "C3-02")
    
    # Registra alcuni movimenti
    magazzino.aggiorna_quantita("PRD001", 20, "USCITA")
    magazzino.aggiorna_quantita("PRD002", 10, "INGRESSO")
    
    # Genera report
    magazzino.report_inventario()
    
    # Salva i dati
    magazzino.salva_dati("dati_magazzino.json")