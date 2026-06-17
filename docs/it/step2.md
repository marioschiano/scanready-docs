# Step 2 - UV / Cage

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;">
</p>

<p align="center">
<b>UV della scansione originale vs packing UV ottimizzato generato da ScanReady.</b>
</p>

---

Step 2 genera un nuovo layout UV e prepara il cage per il bake.

Dopo che la scansione e stata semplificata nello Step 1, la mesh ottimizzata ha bisogno di UV pulite per ricevere correttamente le texture sulla nuova superficie lowpoly.

Questo step prepara l'asset al trasferimento delle texture, permettendo alla mesh ottimizzata di mantenere gran parte della ricchezza visiva della scansione high-poly originale, restando abbastanza leggera per **VR, videogame, AR, visualizzazione realtime e ambienti interattivi**.

---

## Perche servono le UV

Una mesh semplificata e piu leggera e piu facile da gestire, ma ha comunque bisogno di coordinate texture coerenti.

Le UV definiscono come la superficie del modello 3D viene aperta nello spazio texture 2D.

Dopo la riduzione, le UV originali della scansione non dovrebbero piu essere considerate affidabili sulla mesh ottimizzata.

Poiche la geometria e stata unita e semplificata, il layout UV originale puo diventare:

- stirato;
- distorto;
- sovrapposto;
- sporco;
- non allineato alla nuova superficie lowpoly.

Senza UV nuove, ScanReady non puo trasferire correttamente le informazioni texture dalla scansione originale alla mesh ottimizzata.

Creare UV nuove garantisce bake piu puliti e una proiezione texture piu affidabile.

<p align="center">
  <img src="../../img/step2-uv-02.png" alt="Confronto checker texture con UV stirate e UV pulite" style="max-width:1000px;width:100%;">
</p>

<p align="center">
<b>La preview checker aiuta a vedere stretching, densita texel irregolare e distorsioni UV prima del bake.</b>
</p>

---

## Migliore uso dello spazio UV

Le nuove UV migliorano anche l'efficienza dello spazio texture.

Molte scansioni fotogrammetriche contengono layout UV che sprecano grandi porzioni dello spazio texture 0-1.

Dopo l'ottimizzazione, ScanReady puo generare un layout UV piu pulito, con packing migliore e uso piu efficiente delle texture.

<!-- Sostituire il placeholder con ../../img/step2-uv-packing.png -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot efficienza packing UV" style="max-width:1000px;width:100%;">
</p>

Questo permette all'asset ottimizzato di conservare piu dettaglio usando meno materiali e meno memoria texture.

UV buone aiutano a ottenere:

- texture bake piu pulite;
- migliore nitidezza delle texture;
- meno seam visibili;
- migliori performance realtime;
- risultati piu affidabili nei game engine.

---

## Le texture sostituiscono la geometria

L'obiettivo del bake e conservare la ricchezza visiva della scansione originale riducendo la densita dei poligoni.

Invece di mantenere milioni di poligoni, ScanReady trasferisce le informazioni visive della superficie nelle texture.

Questo permette alla mesh ottimizzata di restare leggera pur conservando gran parte dell'aspetto originale.

---

## Perche serve il cage

Il cage controlla come Blender proietta i dettagli dalla scansione high-poly alla mesh ottimizzata durante il bake.

Se il cage e troppo piccolo:

- alcuni dettagli possono non essere catturati;
- possono comparire aree nere;
- possono apparire errori di proiezione.

Se il cage e troppo grande:

- il bake puo catturare superfici vicine indesiderate;
- possono apparire artefatti di proiezione.

ScanReady include strumenti per rendere questo processo piu veloce e piu semplice.

<p align="center">
  <img src="../../img/cage_01_red.png" alt="Avviso cage rosso con setup non valido per il bake" style="max-width:1000px;width:100%;">
</p>

<p align="center">
<b>Se il cage appare rosso, il bake non proiettera correttamente. Abilita Show Cage, poi aumenta leggermente Cage Extrusion oppure usa Auto Cage Extrusion prima di continuare.</b>
</p>

<p align="center">
  <img src="../../img/step2-uv-03.png" alt="Confronto cage troppo piccolo, corretto e troppo grande" style="max-width:1100px;width:100%;">
</p>

<p align="center">
<b>Cage troppo piccoli perdono dettagli. Cage troppo grandi possono catturare superfici vicine indesiderate.</b>
</p>

<p align="center">
  <img src="../../img/step2-uv-04.png" alt="Confronto di come la dimensione del cage influenza la normal map baked" style="max-width:1100px;width:100%;">
</p>

<p align="center">
<b>La dimensione del cage influenza direttamente il bake: un cage corretto cattura i dettagli in modo pulito senza proiettare geometria indesiderata.</b>
</p>

---

## Metodo UV

ScanReady usa **Smart UV Project** per generare UV sulla mesh ottimizzata.

Smart UV Project e il metodo automatico di unwrap UV di Blender.

E utile per gli oggetti scansionati perche puo generare rapidamente isole UV senza richiedere seam manuali.

ScanReady espone i controlli Smart UV cosi puoi regolare il comportamento dell'unwrap prima del bake.

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;">
</p>

---

## Impostazioni UV

Queste impostazioni controllano come Smart UV Project apre la mesh ottimizzata.

<!-- Sostituire il placeholder con ../../img/step2-ui-panel.png -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Placeholder pannello impostazioni UV e Cage di ScanReady" style="max-width:1000px;width:100%;">
</p>

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Smart UV Preset</h3>

<p>
ScanReady usa Blender Smart UV Project per la generazione UV automatica.
</p>

<p>
I preset Smart UV disponibili includono <strong>Detailed</strong>, <strong>Balanced</strong>, <strong>Large Islands</strong> e <strong>Continuous</strong>.
</p>

<p>
I controlli UV influenzano come la mesh ottimizzata viene aperta prima del bake. Sono separati da Adaptive Reduce, che controlla come la mesh viene semplificata nello Step 1.
</p>

<p>
Cambiare Smart UV Preset, Smart UV Angle, UV Padding o Auto Pack UV non ricostruisce subito il layout UV corrente. Le nuove impostazioni UV vengono usate la prossima volta che clicchi <strong>Generate UVs</strong>, oppure quando <strong>One Click Bake</strong> esegue lo step di generazione UV. <strong>Bake Textures</strong> usa il layout UV gia esistente.
</p>

<h3>Smart UV Angle</h3>

<p>
Controlla quanto aggressivamente Smart UV Project divide la mesh in isole.
</p>

<p>
Valori piu bassi creano piu tagli e piu isole UV.
</p>

<p>
Valori piu alti creano isole UV piu grandi.
</p>

<h3>UV Padding</h3>

<p>
Imposta lo spazio tra le isole UV.
</p>

<p>
Aumenta il padding per ridurre il texture bleeding, soprattutto a risoluzioni texture piu basse.
</p>

<h3>Auto Pack UV</h3>

<p>
Impacchetta automaticamente le isole UV dopo l'unwrap.
</p>

<p>
Lascialo attivo a meno che tu voglia sistemare manualmente le isole UV.
</p>

<p>
Un packing UV migliore aiuta a sfruttare al massimo la risoluzione texture e a conservare piu dettaglio.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/step2-uv-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder pannello impostazioni UV di ScanReady" style="width:320px; max-width:100%;">
</div>

</div>

---

## Preview Checker

Usa **Show Checker** per controllare lo stretching UV prima del bake.

La checker texture aiuta a vedere:

- stretching UV;
- distorsione;
- densita texel irregolare;
- isole UV problematiche.

Un pattern checker pulito di solito indica un layout UV piu sano per il bake.

<!-- Sostituire il placeholder con ../../img/step2-checker-preview.png -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot preview checker" style="max-width:1000px;width:100%;">
</p>

---

## Controlli Cage

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Show Cage</h3>

<p>
Mostra la preview del cage.
</p>

<p>
Usalo prima del bake per controllare che il cage circondi completamente la mesh ottimizzata.
</p>

<h3>Auto Cage Extrusion</h3>

<p>
Stima automaticamente la cage extrusion campionando la distanza tra la mesh ottimizzata e la scansione high-poly originale.
</p>

<p>
E utile per generare un punto di partenza rapido senza indovinare manualmente la distanza del cage.
</p>

<h3>Cage Extrusion</h3>

<p>
Controlla manualmente la distanza del cage.
</p>

<p>
Aumentala se il bake perde dettagli, crea aree nere o produce errori di proiezione.
</p>

<p>
Usa il valore piu piccolo che copre correttamente la superficie della scansione.
</p>

<!-- Sostituire il placeholder con ../../img/step2-cage-extrusion.png -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Placeholder esempi Cage Extrusion" style="max-width:1100px;width:100%;">
</p>

<h3>Cage Alpha</h3>

<p>
Controlla l'opacita della preview del cage.
</p>

<p>
Influenza solo la visualizzazione nel viewport e non cambia il risultato del bake.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/step2-cage-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder pannello impostazioni cage di ScanReady" style="width:320px; max-width:100%;">
</div>

</div>

---

## Azione

Clicca **Generate UVs** dopo aver creato la preview lowpoly.

Se cambi **Smart UV Preset**, **Smart UV Angle**, **UV Padding** o **Auto Pack UV** dopo aver gia generato le UV, clicca di nuovo **Generate UVs** per applicare le nuove impostazioni UV. **Bake Textures** usa il layout UV esistente al momento del bake.

Se sei nello Step 2 e decidi che la mesh ottimizzata e ancora troppo pesante, torna a **Step 1 - Preview / Reduce**. Abbassa **Final Faces** o **Optimize / Reduce**, clicca di nuovo **Create Lowpoly Preview**, poi torna allo Step 2 e clicca di nuovo **Generate UVs** in modo che la mesh UV corrisponda alla nuova ottimizzazione.

Poi controlla:

- layout UV;
- preview checker;
- copertura del cage;

prima di continuare con:

[Step 3 - Bake / Output](step3.md)

---

## Cosa controllare

Prima del bake, verifica che:

- le UV siano generate sulla mesh ottimizzata;
- le isole UV siano impacchettate correttamente;
- il pattern checker non mostri stretching estremo;
- le isole UV abbiano abbastanza padding;
- il cage copra completamente le aree che devono ricevere dettaglio bake;
- il cage non sia cosi grande da catturare superfici vicine indesiderate.

---

## Ottimizzazione realtime

Per workflow VR e videogame, UV e bake permettono a un modello leggero di apparire comunque molto dettagliato.

La mesh ottimizzata dovrebbe conservare le informazioni visive importanti tramite texture, invece che tramite milioni di poligoni.

UV buone e un cage configurato correttamente aiutano a mantenere l'asset:

- piu leggero;
- piu facile da renderizzare;
- piu facile da esportare;
- piu affidabile nei motori realtime;
- visivamente piu vicino alla scansione originale.
