# Step 1 - Preview / Reduce

Crea una preview ottimizzata e leggera dalla scansione high-poly.

Il tempo di elaborazione dipende dalla densità della scansione e dalla potenza del computer: una scansione con milioni di poligoni può richiedere anche circa un minuto o più su un PC di media potenza.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-reduce.gif" alt="Controllo Optimize Reduce di ScanReady che aggiorna la densità della preview low-poly" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
Optimize / Reduce controlla quanta geometria viene mantenuta nella preview low-poly. Il valore predefinito 0.10 crea una preview con circa 90% di poligoni in meno.
</p>

---

## Ottimizzazione adattiva

L'ottimizzazione non viene applicata in modo uniforme su tutto il modello.

ScanReady preserva il dettaglio importante della superficie mentre semplifica in modo più aggressivo le regioni piatte o meno dettagliate.

Questo aiuta a creare asset low-poly più puliti ed efficienti per workflow realtime.

### Adaptive Reduce

Adaptive Reduce è attivo di default e aiuta ScanReady a distribuire la riduzione dei poligoni in modo più intelligente sulla scansione.

Invece di trattare ogni superficie allo stesso modo, permette alle aree piatte di essere ridotte di più e protegge le regioni dove il dettaglio della superficie è più importante.

Questa è la differenza principale tra un semplice passaggio Blender Decimate e il workflow ScanReady. Una decimazione standard può ridurre bordi utili e regioni piatte rumorose con la stessa priorità. ScanReady crea prima pesi adattivi, poi li usa per ridurre le superfici ampie in modo più aggressivo mantenendo più protetti cambi di normale forti, silhouette, bordi e transizioni importanti della forma.

Usa il preset Adaptive Reduce come punto di partenza rapido:

- **Balanced** per la maggior parte delle scansioni e degli asset realtime generici.
- **Preserve Details** quando la scansione contiene pieghe importanti, forme scultoree, incisioni o dettagli ravvicinati.
- **Flat Surfaces** quando l'oggetto contiene ampie aree semplici che possono essere semplificate in modo più aggressivo.
- **Hard Surface** per veicoli e scansioni hard-surface, dove un passaggio approssimato più veloce deve proteggere soprattutto i cambi di normale più forti.

<!-- Sostituire il placeholder con ../../img/step1-adaptive-reduce.gif -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Confronto preset Adaptive Reduce di ScanReady" style="max-width:820px;width:100%;">
</p>

<!-- Sostituire il placeholder con ../../img/step1-blender-decimate-vs-scanready.jpg -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Confronto Blender Decimate con ScanReady Adaptive Reduce" style="max-width:1000px;width:100%;">
</p>

<p align="center">
  <b>Blender Decimate vs ScanReady Adaptive Reduce</b><br>
  <span style="font-size:0.9em; opacity:0.75;">Qui andrà un render comparativo reale in Blender: stessa scansione, densità finale simile, Decimate standard da un lato e ScanReady Adaptive Reduce dall'altro.</span>
</p>

## Miglioramento performance

Le scansioni pesanti possono diventare rapidamente difficili da gestire dentro Blender.

### Esempio

- Scansione originale -> 1M+ poligoni
- Preview ottimizzata -> 20K poligoni

Questo aiuta a migliorare la risposta del viewport e rende l'asset più facile da elaborare nei workflow realtime.

---

## Workflow non distruttivo

ScanReady non modifica mai la scansione high-poly originale.

Una mesh ottimizzata duplicata viene generata automaticamente per il workflow, mantenendo intatta la scansione originale.

---

## Perché la riduzione è importante

Le scansioni high-poly sono spesso troppo pesanti per l'uso diretto.

Possono causare:

- performance lente nel viewport;
- scene Blender pesanti;
- esportazioni difficili;
- performance realtime scarse;
- asset VR troppo densi per essere visualizzati fluidamente;
- oggetti game troppo pesanti e difficili da gestire in produzione.

Preview / Reduce crea una versione più leggera della scansione prima di continuare con UV e bake.

Aiuta anche a rimuovere piccoli artefatti mesh generati da fotogrammetria o acquisizione 3D, come poligoni staccati, vertici isolati e frammenti sospesi.

---

Step 1 crea una preview low-poly ottimizzata dalla scansione high-poly selezionata.

Questo è il primo passaggio importante quando prepari un oggetto scansionato per **VR, AR, videogame, visualizzazione realtime o scene interattive**.

ScanReady prima pulisce i frammenti indesiderati comuni della scansione, poi riduce il modello preservando la forma generale e l'identità visiva della scansione originale.

---

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-top:24px; margin-bottom:28px;">

<div style="flex:1 1 320px; min-width:260px;">

<h3>Optimize / Reduce</h3>

<p>
Il valore predefinito e <strong>0.10</strong>.
</p>

<p>
Mantiene circa <strong>10% dei poligoni originali</strong>, creando una preview low-poly più leggera con circa <strong>90% di poligoni in meno</strong>.
</p>

<p>
Dopo aver cliccato <strong>Create Low-poly Preview</strong>, puoi ancora regolare questo valore per provare risultati più leggeri o più dettagliati.
</p>

<p>
Scansioni molto dense con milioni di poligoni possono comunque richiedere tempo di elaborazione.
</p>

<p>
Gli aggiornamenti realtime dipendono dalla complessità della scansione e dalle performance di Blender.
</p>

</div>

<div style="flex:0 0 360px; text-align:center;">
  <img src="../../img/step1-slider_reduce.gif" alt="Slider Optimize Reduce di ScanReady che aggiorna il valore della preview low-poly" style="width:360px; max-width:100%;">
</div>

</div>

---

## Impostazioni principali

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Final Faces</h3>

<p>
Imposta il numero target di facce per la mesh low-poly ottimizzata.
</p>

<p>
Usa valori più bassi per asset VR o game leggeri.
</p>

<p>
Usa valori più alti quando l'oggetto deve conservare più dettaglio nella silhouette.
</p>

<h3>Optimize / Reduce</h3>

<p>
Controlla quanto ScanReady riduce la scansione high-poly selezionata.
</p>

<p>
Il valore predefinito e <strong>0.10</strong>, che mantiene circa <strong>10% dei poligoni originali</strong>.
</p>

<p>
Valori più bassi generano asset più leggeri.
</p>

<p>
Valori più alti preservano più dettaglio della forma.
</p>

<h3>Reduction</h3>

<p>
Mostra la percentuale di riduzione corrente in base alle impostazioni di ottimizzazione selezionate.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <img src="../../img/step1-preview-reduce_optimize.png" alt="Pannello Step 1 Preview Reduce di ScanReady con pulsante Create Low-poly Preview" style="width:320px; max-width:100%;">
</div>

</div>

---

## View Options

Nel pannello attuale di ScanReady, **Show Wireframe** e **Show Checker** si trovano prima dello **STEP 1**.

Sono strumenti di preview usati per controllare topologia e leggibilità UV senza cambiare il workflow di bake.

<div style="flex:0 0 320px; text-align:center;">
  <img src="../../img/step1-preview-reduce_optimize.png" alt="Pannello Step 1 Preview Reduce di ScanReady con pulsante Create Low-poly Preview" style="width:320px; max-width:100%;">
  </div>

</div>
---

## Show Wireframe

Mostra la topologia dell'oggetto preview.

Usalo per controllare se la mesh è ancora troppo densa o se è stata ridotta troppo aggressivamente.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-wireframe.gif" alt="Preview Show Wireframe di ScanReady su una scansione ottimizzata" style="max-width:820px;width:100%;">
</div>

---

## Show Checker

Mostra una texture checker sulla mesh preview.

Aiuta a controllare densità UV e distorsione texture.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-checker.gif" alt="Preview Show Checker di ScanReady su una scansione ottimizzata" style="max-width:820px;width:100%;">
</div>

---

## Checker Mix / Checker UV Scale

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-bottom:24px;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Checker Mix</h3>

<p>
Controlla quanto forte appare l'overlay checker sulla superficie del modello.
</p>

<h3>Checker UV Scale</h3>

<p>
Cambia la dimensione dei quadrati checker.
</p>

<p>
Quadrati più piccoli rendono più facile vedere stretching e distorsione UV.
</p>

<p>
Quadrati più grandi sono utili per controlli generali rapidi.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <img src="../../img/step1-checker-mix-scale.png" alt="Controlli Checker Mix e Checker UV Scale di ScanReady" style="width:320px; max-width:100%;">
</div>

</div>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img src="../../img/step1-checker-mix.gif" alt="Controllo Checker Mix di ScanReady che regola la forza dell'overlay checker" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
Checker Mix regola quanto è visibile l'overlay checker sopra la superficie del modello.
</p>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img src="../../img/step1-checker-scale.gif" alt="Controllo Checker UV Scale di ScanReady che cambia la dimensione dei quadrati checker" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
Checker UV Scale cambia la dimensione del pattern checker per rendere più facile controllare lo stretching UV.
</p>

---

## Quando rifare la preview

Usa di nuovo **Create Low-poly Preview** quando cambi densità o vuoi testare una riduzione diversa.

Se la preview è troppo pesante o troppo semplificata, regola **Optimize / Reduce** o **Final Faces** e crea di nuovo la preview.

Puoi tornare allo Step 1 in qualsiasi momento. Se sei già nello Step 2 o nello Step 3 e decidi che il modello deve essere più leggero o più dettagliato, cambia qui le impostazioni di riduzione, clicca di nuovo **Create Low-poly Preview**, poi continua generando UV e bake di nuovo.

ScanReady pulisce la scansione high-poly selezionata, rimuove rumore mesh comune come poligoni staccati o vertici isolati, poi crea un oggetto preview ottimizzato.

Prima che venga aggiunto il modificatore Decimate, ScanReady può eseguire anche una pulizia **Pre-Decimate Merge** sulla mesh preview duplicata.
Questo aiuta a ridurre poligoni sovrapposti della scansione prima dell'ottimizzazione.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-cleaner.gif" alt="Pulizia mesh di ScanReady prima della preview low-poly" style="max-width:820px;width:100%;">
</div>

Quando la preview è corretta, continua con:

[Step 2 - UV / Cage](step2.md)

---

## Cosa controllare

Dopo aver creato la preview, controlla:

- silhouette generale;
- bordi importanti e dettagli della forma;
- densità dei poligoni;
- leggibilità del wireframe;
- se la scansione è abbastanza leggera per la piattaforma target;
- se è stata persa troppa informazione visiva.

Se la preview è troppo pesante, riducila di più.

Se la preview perde dettagli importanti della forma, aumenta la densità target e creala di nuovo.

---

## Obiettivi di ottimizzazione realtime

Per workflow VR e videogame, l'obiettivo non è solo la qualità visiva.

L'asset deve restare abbastanza leggero per performance realtime fluide.

Una buona preview dovrebbe:

- preservare la forma riconoscibile della scansione originale;
- rimuovere densità inutile della scansione;
- migliorare la risposta del viewport di Blender;
- essere adatta alla generazione UV;
- essere pronta per il texture bake nello step successivo.
