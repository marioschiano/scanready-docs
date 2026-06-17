# Step 1 - Preview / Reduce

Crea in pochi secondi una preview ottimizzata e leggera dalla scansione high-poly.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-reduce.gif" alt="Controllo Optimize Reduce di ScanReady che aggiorna la densita della preview lowpoly" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
Optimize / Reduce controlla quanta geometria viene mantenuta nella preview lowpoly. Il valore predefinito 0.10 crea una preview con circa 90% di poligoni in meno.
</p>

---

## Ottimizzazione adattiva

L'ottimizzazione non viene applicata in modo uniforme su tutto il modello.

ScanReady preserva il dettaglio importante della superficie mentre semplifica in modo piu aggressivo le regioni piatte o meno dettagliate.

Questo aiuta a creare asset lowpoly piu puliti ed efficienti per workflow realtime.

### Adaptive Reduce

Adaptive Reduce e attivo di default e aiuta ScanReady a distribuire la riduzione dei poligoni in modo piu intelligente sulla scansione.

Invece di trattare ogni superficie allo stesso modo, permette alle aree piatte di essere ridotte di piu e protegge le regioni dove il dettaglio della superficie e piu importante.

Questa e la differenza principale tra un semplice passaggio Blender Decimate e il workflow ScanReady. Una decimazione standard puo ridurre bordi utili e regioni piatte rumorose con la stessa priorita. ScanReady crea prima pesi adattivi, poi li usa per ridurre le superfici ampie in modo piu aggressivo mantenendo piu protetti cambi di normale forti, silhouette, bordi e transizioni importanti della forma.

Usa il preset Adaptive Reduce come punto di partenza rapido:

- **Balanced** per la maggior parte delle scansioni e degli asset realtime generici.
- **Preserve Details** quando la scansione contiene pieghe importanti, forme scultoree, incisioni o dettagli ravvicinati.
- **Flat Surfaces** quando l'oggetto contiene ampie aree semplici che possono essere semplificate in modo piu aggressivo.
- **Hard Surface** per veicoli e scansioni hard-surface dove un passaggio approssimato piu veloce deve proteggere solo rotture di normale piu forti.

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
  <span style="font-size:0.9em; opacity:0.75;">Qui andra un render comparativo reale in Blender: stessa scansione, densita finale simile, Decimate standard da un lato e ScanReady Adaptive Reduce dall'altro.</span>
</p>

### Show Adaptive Weights

Show Adaptive Weights mostra direttamente sul modello i pesi di riduzione.

Usalo prima di creare la preview finale quando vuoi capire come ScanReady sta leggendo la scansione:

- le aree **rosse** sono regioni piatte che possono essere ridotte di piu;
- le aree **blu / verdi** sono regioni protette per il dettaglio.

La visualizzazione e solo un aiuto di preview. Serve a scegliere il preset e capire il comportamento della riduzione; non e una texture esportata o baked.

I pesi Adaptive Reduce vengono calcolati quando clicchi **Create Lowpoly Preview**. Dopo che la preview esiste, cambiare **Optimize / Reduce** o **Final Faces** aggiorna la quantita di Decimate usando i pesi esistenti. Se cambi il preset Adaptive Reduce o i valori dettagliati di Adaptive Reduce, clicca di nuovo **Create Lowpoly Preview** per ricostruire i pesi con le nuove impostazioni.

<!-- Sostituire il placeholder con ../../img/step1-adaptive-weights.gif -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Visualizzazione Show Adaptive Weights di ScanReady" style="max-width:820px;width:100%;">
</p>

---

## Miglioramento performance

Le scansioni pesanti possono diventare rapidamente difficili da gestire dentro Blender.

### Esempio

- Scansione originale -> 1M+ poligoni
- Preview ottimizzata -> 20K poligoni

Questo aiuta a migliorare la risposta del viewport e rende l'asset piu facile da elaborare nei workflow realtime.

---

## Workflow non distruttivo

ScanReady non modifica mai la scansione high-poly originale.

Una mesh ottimizzata duplicata viene generata automaticamente per il workflow, mantenendo intatta la scansione originale.

---

## Perche la riduzione e importante

Le scansioni high-poly sono spesso troppo pesanti per l'uso diretto.

Possono causare:

- performance lente nel viewport;
- scene Blender pesanti;
- esportazioni difficili;
- performance realtime scarse;
- asset VR troppo densi per essere visualizzati fluidamente;
- oggetti game troppo costosi per la produzione.

Preview / Reduce crea una versione piu leggera della scansione prima di continuare con UV e bake.

Aiuta anche a rimuovere piccoli artefatti mesh generati da fotogrammetria o acquisizione 3D, come poligoni staccati, vertici isolati e frammenti sospesi.

---

Step 1 crea una preview lowpoly ottimizzata dalla scansione high-poly selezionata.

Questo e il primo passaggio importante quando prepari un oggetto scansionato per **VR, AR, videogame, visualizzazione realtime o scene interattive**.

ScanReady prima pulisce i frammenti indesiderati comuni della scansione, poi riduce il modello preservando la forma generale e l'identita visiva della scansione originale.

---

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-top:24px; margin-bottom:28px;">

<div style="flex:1 1 320px; min-width:260px;">

<h3>Optimize / Reduce</h3>

<p>
Il valore predefinito e <strong>0.10</strong>.
</p>

<p>
Mantiene circa <strong>10% dei poligoni originali</strong>, creando una preview lowpoly piu leggera con circa <strong>90% di poligoni in meno</strong>.
</p>

<p>
Dopo aver cliccato <strong>Create Lowpoly Preview</strong>, puoi ancora regolare questo valore per provare risultati piu leggeri o piu dettagliati.
</p>

<p>
Scansioni molto dense con milioni di poligoni possono comunque richiedere tempo di elaborazione.
</p>

<p>
Gli aggiornamenti realtime dipendono dalla complessita della scansione e dalle performance di Blender.
</p>

</div>

<div style="flex:0 0 360px; text-align:center;">
  <img src="../../img/step1-slider_reduce.gif" alt="Slider Optimize Reduce di ScanReady che aggiorna il valore della preview lowpoly" style="width:360px; max-width:100%;">
</div>

</div>

---

## Impostazioni principali

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Final Faces</h3>

<p>
Imposta il numero target di facce per la mesh lowpoly ottimizzata.
</p>

<p>
Usa valori piu bassi per asset VR o game leggeri.
</p>

<p>
Usa valori piu alti quando l'oggetto deve conservare piu dettaglio nella silhouette.
</p>

<h3>Optimize / Reduce</h3>

<p>
Controlla quanto ScanReady riduce la scansione high-poly selezionata.
</p>

<p>
Il valore predefinito e <strong>0.10</strong>, che mantiene circa <strong>10% dei poligoni originali</strong>.
</p>

<p>
Valori piu bassi generano asset piu leggeri.
</p>

<p>
Valori piu alti preservano piu dettaglio della forma.
</p>

<h3>Reduction</h3>

<p>
Mostra la percentuale di riduzione corrente in base alle impostazioni di ottimizzazione selezionate.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <img src="../../img/step1-preview-reduce.png" alt="Pannello Step 1 Preview Reduce di ScanReady con pulsante Create Lowpoly Preview" style="width:320px; max-width:100%;">
</div>

</div>

---

## View Options

Nel pannello attuale di ScanReady, **Show Wireframe** e **Show Checker** si trovano prima dello **STEP 1**.

Sono strumenti di preview usati per controllare topologia e leggibilita UV senza cambiare il workflow di bake.

---

## Show Wireframe

Mostra la topologia dell'oggetto preview.

Usalo per controllare se la mesh e ancora troppo densa o se e stata ridotta troppo aggressivamente.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-wireframe.gif" alt="Preview Show Wireframe di ScanReady su una scansione ottimizzata" style="max-width:820px;width:100%;">
</div>

---

## Show Checker

Mostra una texture checker sulla mesh preview.

Aiuta a controllare densita UV e distorsione texture.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-checker.gif" alt="Preview Show Checker di ScanReady su una scansione ottimizzata" style="max-width:820px;width:100%;">
</div>

---

## Checker Mix / Checker Scale

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-bottom:24px;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Checker Mix</h3>

<p>
Controlla quanto forte appare l'overlay checker sulla superficie del modello.
</p>

<h3>Checker Scale</h3>

<p>
Cambia la dimensione dei quadrati checker.
</p>

<p>
Quadrati piu piccoli rendono piu facile vedere stretching e distorsione UV.
</p>

<p>
Quadrati piu grandi sono utili per controlli generali rapidi.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <img src="../../img/step1-checker-mix-scale.png" alt="Controlli Checker Mix e Checker Scale di ScanReady" style="width:320px; max-width:100%;">
</div>

</div>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img src="../../img/step1-checker-mix.gif" alt="Controllo Checker Mix di ScanReady che regola la forza dell'overlay checker" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
Checker Mix regola quanto e visibile l'overlay checker sopra la superficie del modello.
</p>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img src="../../img/step1-checker-scale.gif" alt="Controllo Checker Scale di ScanReady che cambia la dimensione dei quadrati checker" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
Checker Scale cambia la dimensione del pattern checker per rendere piu facile controllare lo stretching UV.
</p>

---

## Azione

Clicca **Create Lowpoly Preview**.

Se la preview e troppo pesante o troppo semplificata, regola **Optimize / Reduce** o **Final Faces** e crea di nuovo la preview.

Puoi tornare allo Step 1 in qualsiasi momento. Se sei gia nello Step 2 o nello Step 3 e decidi che il modello deve essere piu leggero o piu dettagliato, cambia qui le impostazioni di riduzione, clicca di nuovo **Create Lowpoly Preview**, poi continua generando UV e bake di nuovo.

ScanReady pulisce la scansione high-poly selezionata, rimuove rumore mesh comune come poligoni staccati o vertici isolati, poi crea un oggetto preview ottimizzato.

Prima che venga aggiunto il modificatore Decimate, ScanReady puo eseguire anche una pulizia **Pre-Decimate Merge** sulla mesh preview duplicata.
Questo aiuta a ridurre poligoni sovrapposti della scansione prima dell'ottimizzazione.

In **Advanced > Mesh Settings**, **Pre-Decimate Merge** e il singolo controllo esplicito di weld. Abbassalo se vengono colpiti dettagli sottili.

<div style="width:100%; text-align:left;">
  <img src="../../img/step1-cleaner.gif" alt="Pulizia mesh di ScanReady prima della preview lowpoly" style="max-width:820px;width:100%;">
</div>

Quando la preview e corretta, continua con:

[Step 2 - UV / Cage](step2.md)

---

## Cosa controllare

Dopo aver creato la preview, controlla:

- silhouette generale;
- bordi importanti e dettagli della forma;
- densita dei poligoni;
- leggibilita del wireframe;
- se la scansione e abbastanza leggera per la piattaforma target;
- se e stata persa troppa informazione visiva.

Se la preview e troppo pesante, riducila di piu.

Se la preview perde dettagli importanti della forma, aumenta la densita target e creala di nuovo.

---

## Obiettivi di ottimizzazione realtime

Per workflow VR e videogame, l'obiettivo non e solo la qualita visiva.

L'asset deve restare abbastanza leggero per performance realtime fluide.

Una buona preview dovrebbe:

- preservare la forma riconoscibile della scansione originale;
- rimuovere densita inutile della scansione;
- migliorare la risposta del viewport di Blender;
- essere adatta alla generazione UV;
- essere pronta per il texture bake nello step successivo.
