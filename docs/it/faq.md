# FAQ

## Come posso contattare il supporto?

Per supporto, bug report o domande sul workflow, contatta:

<a href="mailto:support.marioschiano3d@gmail.com"><strong>support.marioschiano3d@gmail.com</strong></a>

## Perché le UV si sovrappongono?

La sovrapposizione UV può succedere quando la mesh è estremamente densa oppure quando le isole UV non hanno abbastanza spazio.

Per migliorare il risultato:

- aumenta **UV Padding**;
- prova un valore diverso di **Smart UV Angle**;
- genera di nuovo le UV;
- riduci frammenti mesh molto piccoli prima dell'unwrap.

Isole UV ben distanziate aiutano a prevenire texture bleeding e artefatti di bake.

## Perché il bake appare rumoroso o sporco?

Texture bake rumorose sono di solito causate da risoluzione texture insufficiente, impostazioni cage errate o ottimizzazione troppo aggressiva.

Prova:

- aumentare **Texture Size**;
- aumentare **Bake Samples**;
- aumentare leggermente la densità low-poly;
- abilitare **Show Cage** e controllare la preview cage prima del bake;
- aumentare leggermente **Cage Extrusion** oppure usare **Auto Cage Extrusion**.

Scansioni molto dense possono richiedere anche più materiali bake per una qualità texture più pulita.

## Perché il bake GPU è ancora lento?

Scansioni grandi e texture ad alta risoluzione possono richiedere molto tempo anche su GPU potenti.

La velocità di bake dipende da:

- risoluzione texture;
- numero di materiali bake;
- complessità della scansione;
- VRAM GPU;
- mappe bake abilitate.

Per migliorare le performance:

- abbassa la risoluzione texture;
- disattiva mappe bake non necessarie;
- riduci i materiali bake quando possibile;
- usa meno bake samples per test di preview.

## Perché la mesh low-poly sembra troppo liscia?

Se la mesh ottimizzata perde troppo dettaglio della forma:

- aumenta **Final Faces**;
- usa un valore **Optimize / Reduce** più alto;
- evita riduzioni molto aggressive su asset dettagliati.

Alcune scansioni richiedono più geometria per preservare correttamente silhouette importanti.

## Ho usato One Click Bake, ma il modello finale è ancora troppo pesante. Cosa devo fare?

One Click Bake usa le impostazioni correnti dello Step 1. Se il modello finale non è abbastanza ottimizzato, puoi rifinirlo manualmente senza ripartire da zero.

Questo vale anche se stai già lavorando nello Step 2 o nello Step 3. Puoi sempre tornare allo Step 1, cambiare la riduzione e continuare di nuovo in avanti.

Prova questo workflow:

- torna a **Step 1 - Preview / Reduce**;
- abbassa **Final Faces**, oppure abbassa **Optimize / Reduce**;
- clicca di nuovo **Create Lowpoly Preview**;
- controlla la preview con **Show Wireframe** o **Show Adaptive Weights**;
- vai a **Step 2 - UV / Cage** e clicca di nuovo **Generate UVs**;
- vai a **Step 3 - Bake / Output** ed esegui di nuovo **Bake Textures**.

Se l'oggetto è un veicolo, un asset meccanico, una scansione architettonica o un altro oggetto hard-surface, prova il preset Adaptive Reduce **Hard Surface**. Per test più rapidi su scansioni molto dense, abilita **Fast Adaptive Reduce** in Advanced prima di creare di nuovo la preview.

Valori più bassi creano asset più leggeri, ma una riduzione troppo aggressiva può danneggiare silhouette o dettagli importanti. Usa lo step preview per trovare il miglior equilibrio prima del bake.

## Perché compaiono seam visibili nella texture bake?

I seam visibili possono comparire quando le isole UV hanno padding insufficiente o quando la risoluzione texture è troppo bassa.

Prova:

- aumentare **UV Padding**;
- aumentare la risoluzione texture;
- controllare la preview checker prima del bake;
- rigenerare le UV con impostazioni diverse.

Packing e padding UV corretti aiutano a ridurre seam visibili.

## Perché ScanReady consiglia più materiali bake?

Le scansioni grandi spesso contengono più dettaglio di quanto una singola texture possa preservare in modo efficiente.

Usare più materiali bake aumenta lo spazio texture disponibile e aiuta a preservare più dettaglio sull'asset.

ScanReady può consigliare automaticamente un numero adeguato di materiali in base alla complessità della scansione e ai requisiti di dettaglio texture.

## Perché la mesh ottimizzata sembra diversa dalla scansione originale?

L'ottimizzazione riduce la densità dei poligoni per migliorare le performance realtime.

Alcune differenze visive sono normali perché la geometria non necessaria viene semplificata.

Però ScanReady usa ottimizzazione adattiva per preservare dettagli importanti della superficie mentre semplifica in modo più aggressivo le regioni piatte o meno dettagliate.
