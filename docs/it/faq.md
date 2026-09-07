# FAQ

Risposte rapide ai dubbi più comuni. Per i controlli completi consulta [Risoluzione problemi](troubleshooting.md).

## Quale versione di Blender serve?

ScanReady è una Blender Extension e richiede **Blender 4.2 o successivo**. Scarica il pacchetto dalla piattaforma di acquisto e segui la pagina [Installazione](installation.md).

## ScanReady modifica la scansione originale?

La riduzione avviene su una preview separata. La preparazione, però, può intervenire sulla high-poly: unire parti, applicare la scala, correggere normali, pulire frammenti o convertire materiali in base alle opzioni attive.

Salva una copia del file originale prima dello Step 1, soprattutto per scansioni destinate all’archivio.

## Devo impostare sia Final Faces sia Optimize / Reduce?

No. Sono due controlli collegati della stessa riduzione: **Final Faces** indica il target di facce, **Optimize / Reduce** la proporzione di geometria da mantenere. Usa quello più comodo; un rapporto di `0.10` mantiene circa il 10% dei poligoni.

## Perché le UV si sovrappongono?

Controlla il layout della mesh UV, non quello della sorgente high-poly. Frammenti molto piccoli o geometria problematica possono rendere più difficile l’unwrap.

1. Verifica la preview e rimuovi solo i frammenti indesiderati.
2. Prova un altro **Smart UV Preset** o regola **Smart UV Angle**.
3. Controlla **UV Padding** e premi di nuovo **Generate UVs**.

Il padding separa le isole; non corregge da solo la distorsione al loro interno.

## Perché il bake appare sfocato, rumoroso o sporco?

La soluzione dipende dal difetto:

| Problema | Primo controllo |
|---|---|
| Texture sfocata | Risoluzione di output, qualità della sorgente e uso dello spazio UV. |
| Rumore nell’AO | **AO Samples** in **Advanced > Bake Settings > Occlusion Settings**. |
| Zone nere o dettagli proiettati male | **Show Cage**, distanza del cage, normali e materiali sorgente. |
| Silhouette troppo semplificata | **Final Faces**, **Optimize / Reduce** e preset adattivo. |

Aumentare i sample non aggiunge dettaglio a una texture sorgente poco definita. Cambia un parametro alla volta e confronta il risultato.

## Perché il bake GPU è ancora lento?

Risoluzione, numero di materiali, mappe abilitate e complessità della sorgente influiscono sui tempi. Controlla anche **Force CPU Baking**: ScanReady lo abilita automaticamente quando imposti **Bake Materials** a `2` o più.

Per i test usa texture più piccole e solo le mappe necessarie. Riduci i sample della mappa interessata; aumenta la qualità dopo aver verificato il workflow.

## Perché la mesh low-poly sembra troppo liscia?

Se manca dettaglio nella forma, aumenta **Final Faces** oppure **Optimize / Reduce**, o prova il preset **Preserve Details**. Poi aggiorna la preview.

Una Normal Map può riprodurre l’aspetto di piccoli dettagli, ma non ricostruisce una silhouette eliminata dalla riduzione.

## Ho usato One Click Bake, ma il modello finale è ancora troppo pesante. Cosa devo fare?

Puoi tornare allo Step 1 anche dopo UV e bake:

1. Regola **Final Faces** oppure **Optimize / Reduce**.
2. Premi **Create Lowpoly Preview** e controlla silhouette e wireframe.
3. Premi **Generate UVs** nello Step 2.
4. Controlla il cage.
5. Ripeti **Bake Textures** nello Step 3.

!!! tip "Scegli il preset in base alla forma"
    Prova **Flat Surfaces** per superfici ampie e semplici, **Hard Surface** per oggetti meccanici. Usa **Fast Adaptive Reduce** per un’analisi più rapida e approssimata delle scansioni dense.

## Perché compaiono seam visibili nella texture bake?

Controlla sia **UV Padding**, che separa le isole, sia **Bake Margin**, che estende i pixel del bake oltre i bordi delle isole. Anche risoluzione, compressione e illuminazione già presente nella texture sorgente possono rendere visibili le cuciture.

Se modifichi UV Padding, rigenera le UV e ripeti il bake. Se cambi solo Bake Margin, ripeti il bake sul layout esistente.

## Perché ScanReady consiglia più materiali bake?

Più materiali possono fornire più spazio texture per scansioni grandi. Il consiglio di **Analyze Texture Detail** è una stima basata sulle texture sorgente e sul layout UV, non una garanzia del risultato.

Considera il costo in memoria e il numero di materiali richiesto dalla piattaforma finale. Più poligoni, da soli, non risolvono una texture poco definita.

## Quando devo attivare Convert Source Materials?

Lascialo disattivato se il bake è corretto. Provalo se la Base Color è nera, incompleta o incoerente e il problema dipende dai materiali importati.

Attiva **Convert Source Materials** in **Advanced > Mesh Settings**, premi **Create Lowpoly Preview** e controlla i materiali prima di ripetere il bake. I materiali già standard vengono mantenuti.

## Save Preset salva anche il modello?

No. Salva i parametri del workflow, inclusa la cartella di output, ma non gli oggetti o le immagini della scena. Usa il file `.blend` per conservare il progetto.

Dopo **Reload Preset**, verifica Output Folder e rigenera gli step interessati dalle nuove impostazioni.

## Perché la mesh ottimizzata sembra diversa dalla scansione originale?

La riduzione elimina geometria: alcune differenze sono inevitabili. Controlla il modello alla distanza di osservazione prevista e confronta anche materiali e illuminazione.

Se le differenze riguardano la forma, aumenta la densità. Se riguardano il colore o il dettaglio superficiale, controlla UV, cage e texture prima di aggiungere poligoni.

## Come posso contattare il supporto?

Scrivi a <support.marioschiano3d@gmail.com> indicando versioni di Blender e ScanReady, passaggi per riprodurre il problema e uno screenshot. Per problemi di memoria, aggiungi RAM e modello della GPU.

Consulta [Supporto](support.md) per i dettagli.
