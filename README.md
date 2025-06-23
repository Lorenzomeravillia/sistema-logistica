# Sistema di Gestione Logistica

Questo repository contiene un sistema base per la gestione logistica scritto in Python. Il sistema include moduli per la gestione del magazzino e l'ottimizzazione dei percorsi di consegna.

## 📦 Contenuto del Repository

### 1. `gestione_magazzino.py`
Sistema completo per la gestione dell'inventario di magazzino con le seguenti funzionalità:
- Aggiunta e aggiornamento prodotti
- Tracciamento movimenti (ingressi/uscite)
- Generazione report inventario
- Salvataggio/caricamento dati in formato JSON

### 2. `ottimizzazione_percorsi.py`
Modulo per l'ottimizzazione dei percorsi di consegna che include:
- Algoritmo del vicino più vicino per ottimizzare i percorsi
- Divisione automatica delle consegne tra veicoli multipli
- Calcolo distanze e generazione report dettagliati

### 3. `requirements.txt`
Lista delle dipendenze Python necessarie per eseguire i moduli.

## 🚀 Come Utilizzare

### Gestione Magazzino
```python
from gestione_magazzino import Magazzino

# Crea un nuovo magazzino
magazzino = Magazzino("Milano Nord")

# Aggiungi prodotti
magazzino.aggiungi_prodotto("PRD001", "Scatole cartone", 100, "A1-01")

# Aggiorna quantità
magazzino.aggiorna_quantita("PRD001", 20, "USCITA")

# Genera report
magazzino.report_inventario()
```

### Ottimizzazione Percorsi
```python
from ottimizzazione_percorsi import OttimizzatorePercorsi, PuntoConsegna

# Crea ottimizzatore con coordinate deposito
ottimizzatore = OttimizzatorePercorsi(45.4642, 9.1900)

# Aggiungi consegne
consegna = PuntoConsegna("C001", "Cliente Milano", 45.4641, 9.1919, 150)
ottimizzatore.aggiungi_consegna(consegna)

# Ottimizza e dividi per veicoli
veicoli = ottimizzatore.dividi_per_veicoli(500)
```

## 📊 Esempi di Output

Il sistema genera report dettagliati che includono:
- Stato attuale dell'inventario
- Storico movimenti magazzino
- Percorsi ottimizzati per ogni veicolo
- Statistiche di distanza e carico

## 🔧 Requisiti

- Python 3.7+
- Moduli standard Python (datetime, json, math, random, typing)

## 📝 Note per l'Integrazione con OpenAI Codex

Questi file sono stati progettati per essere facilmente analizzati e modificati tramite AI. Il codice include:
- Commenti dettagliati in italiano
- Struttura modulare e chiara
- Esempi di utilizzo integrati
- Documentazione delle funzioni

## 🚧 Possibili Estensioni

- Integrazione con database reali
- API REST per accesso remoto
- Visualizzazione grafica dei percorsi
- Algoritmi di ottimizzazione più avanzati
- Gestione multi-magazzino

## 📄 Licenza

Questo codice è fornito a scopo educativo e di test.
