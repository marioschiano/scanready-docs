# ScanReady

Workflow di ottimizzazione adattiva e bake per scansioni in Blender

<p align="center">
  <img src="../img/hero.png" alt="Panoramica del workflow ScanReady" style="max-width:620px;width:100%;">
</p>

<br>

ScanReady è un addon per Blender pensato per trasformare scansioni 3D pesanti in asset ottimizzati e pronti per il realtime.

E pensato per artisti 3D, creatori di asset, workflow di fotogrammetria, VR, videogame, visualizzazione realtime e scene interattive.

Invece di trattare tutta la mesh nello stesso modo, ScanReady usa un workflow di riduzione adattiva che aiuta a proteggere silhouette, bordi, cambi di forma e dettagli importanti, riducendo in modo piu aggressivo le aree piatte o meno rilevanti.

<p align="center">
  <b>Scansione high-poly -> Mesh ottimizzata -> UV -> Bake -> Asset realtime</b>
</p>

---

## Perche ScanReady e diverso

Molti workflow di ottimizzazione usano una semplice riduzione uniforme.

ScanReady invece usa **Adaptive Reduce** per distribuire la riduzione in modo piu intelligente:

- Le aree piatte possono essere ridotte di piu.
- I dettagli importanti vengono protetti meglio.
- Le silhouette e le transizioni di forma rimangono piu leggibili.
- Le superfici rumorose della scansione possono essere semplificate senza perdere subito l'identita dell'oggetto.

<p align="center">
  <img src="../img/why-scanready-adaptive-optimization.png" alt="Confronto tra Blender Decimate e ScanReady Adaptive Reduce" style="max-width:1000px;width:100%;">
</p>

<p align="center">
  <b>Blender Decimate vs ScanReady Adaptive Reduce</b><br>
  <span style="font-size:0.9em; opacity:0.75;">Stessa scansione, densita finale simile. ScanReady riduce in modo piu aggressivo le zone piatte e protegge meglio dettagli, bordi e cambi di forma.</span>
</p>

---

## Perche ScanReady?

Le scansioni 3D grezze possono essere molto pesanti:

- milioni di poligoni;
- mesh rumorose;
- nessuna UV pulita;
- materiali non pronti per il realtime;
- bake complessi da configurare manualmente;
- performance scarse in VR, videogame o scene interattive.

ScanReady aiuta a passare da una scansione pesante a un asset piu leggero, con UV e texture bake pronte per essere usate in produzione.

---

# Prima / Dopo

Ottimizzato per workflow realtime senza sprecare poligoni inutilmente.

<p align="center">
  <img src="../img/one_click_before_after.jpg" alt="Confronto prima e dopo di una scansione ottimizzata con ScanReady" style="max-width:820px;width:100%;">
</p>

<p align="center">
  <b>Da scansioni fotogrammetriche pesanti ad asset ottimizzati e pronti per videogame.</b>
</p>

<p align="center">
  <img src="../img/one-click-bake.gif" alt="Workflow One Click Bake di ScanReady" width="700">
</p>

<p align="center">
  <b>1M poligoni -> mesh game-ready ottimizzata da 20K</b>
</p>

---

## One Click Bake

Il workflow **ONE CLICK BAKE** esegue automaticamente i passaggi principali:

1. Pulizia della scansione selezionata.
2. Creazione di una preview lowpoly ottimizzata.
3. Generazione delle UV.
4. Stima o preparazione del cage.
5. Bake delle texture.
6. Collegamento dei materiali finali.
7. Salvataggio delle immagini se **Save Images** e attivo.

E il percorso piu veloce per ottenere una prima versione dell'asset.

---

## Funzioni principali

### Ottimizzazione adattiva

**Adaptive Reduce** riduce meglio le zone piatte e protegge dettagli, bordi e silhouette importanti.

### Workflow One Click

**ONE CLICK BAKE** esegue automaticamente pulizia, preview lowpoly, UV, cage, bake e materiali finali.

### Workflow Smart UV

ScanReady usa **Smart UV Project** per generare UV automatiche sulla mesh ottimizzata.

### Generazione automatica del cage

**Auto Cage Extrusion** stima una distanza di cage iniziale per rendere piu rapido il setup del bake.

### Texture Baking

ScanReady supporta bake di **Base Color**, **Normal**, **Roughness** e **Occlusion**.

### Supporto multi-materiale

**Bake Materials** permette di dividere il bake in piu materiali quando una scansione grande richiede piu spazio texture.

### Ottimizzazione realtime

Il workflow e pensato per asset piu leggeri destinati a VR, videogame, AR e visualizzazione realtime.

### Bake sicuro per la memoria

Le opzioni **Safe Memory Bake** e **Force CPU Baking** aiutano con scene pesanti e sistemi con VRAM limitata.

### Preset riutilizzabili

I preset permettono di salvare e riutilizzare setup di workflow per scansioni simili.

---

## Panoramica del workflow

ScanReady puo essere usato in due modi:

- **One Click Bake**: workflow automatico completo.
- **Workflow manuale**: controllo separato di riduzione, UV, cage e bake.

Il workflow manuale e utile quando vuoi controllare meglio il risultato:

### 1. Preview / Reduce

   Crea una mesh ottimizzata dalla scansione high-poly.

### 2. UV / Cage

   Genera UV e prepara il cage per il bake.

### 3. Bake / Output

   Esegue il bake delle texture e crea l'asset finale.

---

## Pensato per il realtime

ScanReady è pensato per preparare asset destinati a:

- VR e AR;
- videogame;
- realtime visualization;
- scene interattive;
- engine come Unreal Engine, Unity, Godot o viewer realtime;
- ambienti dove poligoni, memoria e texture devono rimanere sotto controllo.

---

## Cosa crea ScanReady

Alla fine del workflow ScanReady puo creare:

- una mesh finale ottimizzata;
- UV automatiche;
- texture bake salvate su disco;
- materiali finali collegati alle texture;
- un asset piu leggero rispetto alla scansione originale.

---

## Compatibilita

ScanReady è distribuito come **Blender Extension**.

E pensato per Blender moderno e per il nuovo sistema di estensioni.

---

## Inizia da qui

Per iniziare:

- [Installazione](installation.md)
- [Guida rapida](quick-start.md)
- [One Click Bake](one-click.md)
- [Step 1 - Preview / Reduce](step1.md)
- [Step 2 - UV / Cage](step2.md)
- [Step 3 - Bake / Output](step3.md)

---

## Video e tutorial

I video tutorial verranno aggiunti in questa sezione.

---

## Supporto

Per problemi, domande o feedback:

**Email:** <support.marioschiano3d@gmail.com>
