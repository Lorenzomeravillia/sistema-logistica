diff --git a/ottimizzazione_percorsi.py b/ottimizzazione_percorsi.py
index 38a52e7fa831fbc4f10e11fd7b6b6b7d0c8ab6d1..6b33829c81c6fddcaf7d8ee001f31766b6e0d249 100644
--- a/ottimizzazione_percorsi.py
+++ b/ottimizzazione_percorsi.py
@@ -1,31 +1,33 @@
 # Sistema di Ottimizzazione Percorsi Logistici
 # Calcola il percorso ottimale per le consegne
 
-import math
-import random
-from typing import List, Tuple, Dict
+import math
+import random
+from typing import List, Tuple, Dict
+import tkinter as tk
+from tkinter import ttk
 
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
         
diff --git a/ottimizzazione_percorsi.py b/ottimizzazione_percorsi.py
index 38a52e7fa831fbc4f10e11fd7b6b6b7d0c8ab6d1..6b33829c81c6fddcaf7d8ee001f31766b6e0d249 100644
--- a/ottimizzazione_percorsi.py
+++ b/ottimizzazione_percorsi.py
@@ -115,50 +117,89 @@ class OttimizzatorePercorsi:
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
 
-# Esempio di utilizzo
-if __name__ == "__main__":
-    # Coordinate del deposito centrale (es. Milano)
-    ottimizzatore = OttimizzatorePercorsi(45.4642, 9.1900)
-    
-    # Aggiungi alcune consegne di esempio
-    consegne_esempio = [
-        PuntoConsegna("C001", "Cliente Milano Centro", 45.4641, 9.1919, 150),
-        PuntoConsegna("C002", "Cliente Monza", 45.5845, 9.2744, 200),
-        PuntoConsegna("C003", "Cliente Bergamo", 45.6983, 9.6773, 300),
-        PuntoConsegna("C004", "Cliente Como", 45.8080, 9.0852, 180),
-        PuntoConsegna("C005", "Cliente Lodi", 45.3138, 9.5019, 250),
-        PuntoConsegna("C006", "Cliente Pavia", 45.1847, 9.1582, 120),
-        PuntoConsegna("C007", "Cliente Brescia", 45.5416, 10.2118, 280),
-        PuntoConsegna("C008", "Cliente Varese", 45.8206, 8.8250, 160),
-    ]
-    
-    for consegna in consegne_esempio:
-        ottimizzatore.aggiungi_consegna(consegna)
-        
-    # Dividi le consegne per veicoli con capacità 500 kg
-    veicoli = ottimizzatore.dividi_per_veicoli(500)
-    
-    # Genera il report
-    ottimizzatore.genera_report_percorsi(veicoli)
+class OttimizzatoreGUI:
+    """Interfaccia grafica semplificata per l'ottimizzazione"""
+
+    def __init__(self):
+        self.ottimizzatore = OttimizzatorePercorsi(45.4642, 9.1900)
+        self.root = tk.Tk()
+        self.root.title("Ottimizzazione Percorsi")
+        self._build_widgets()
+
+    def _build_widgets(self):
+        frm_add = ttk.LabelFrame(self.root, text="Aggiungi consegna")
+        frm_add.pack(fill="x", padx=5, pady=5)
+
+        labels = ["ID", "Nome", "Lat", "Lon", "Peso"]
+        self.entries = []
+        for i, label in enumerate(labels):
+            ttk.Label(frm_add, text=label).grid(row=0, column=i, padx=2)
+            ent = ttk.Entry(frm_add, width=10)
+            ent.grid(row=1, column=i, padx=2)
+            self.entries.append(ent)
+        ttk.Button(frm_add, text="Aggiungi", command=self.aggiungi).grid(row=1, column=len(labels), padx=4)
+
+        frm_cap = ttk.Frame(self.root)
+        frm_cap.pack(fill="x", padx=5, pady=5)
+        ttk.Label(frm_cap, text="Capacità veicolo kg:").grid(row=0, column=0)
+        self.cap_entry = ttk.Entry(frm_cap, width=8)
+        self.cap_entry.insert(0, "500")
+        self.cap_entry.grid(row=0, column=1)
+        ttk.Button(frm_cap, text="Ottimizza", command=self.ottimizza).grid(row=0, column=2, padx=4)
+
+        self.report = tk.Text(self.root, height=15, width=70)
+        self.report.pack(fill="both", expand=True, padx=5, pady=5)
+
+    def aggiungi(self):
+        try:
+            idc, nome, lat, lon, peso = [e.get() for e in self.entries]
+            lat = float(lat)
+            lon = float(lon)
+            peso = float(peso)
+        except ValueError:
+            return
+        self.ottimizzatore.aggiungi_consegna(PuntoConsegna(idc, nome, lat, lon, peso))
+        for e in self.entries:
+            e.delete(0, tk.END)
+
+    def ottimizza(self):
+        try:
+            cap = float(self.cap_entry.get())
+        except ValueError:
+            cap = 500
+        veicoli = self.ottimizzatore.dividi_per_veicoli(cap)
+        self.report.delete(1.0, tk.END)
+        for vid, consegne in veicoli.items():
+            self.report.insert(tk.END, f"\nVEICOLO {vid}\n")
+            for p in consegne:
+                self.report.insert(tk.END, f"  - {p}\n")
+
+    def run(self):
+        self.root.mainloop()
+
+
+if __name__ == "__main__":
+    gui = OttimizzatoreGUI()
+    gui.run()
