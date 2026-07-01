# Step 2 - UV / Cage

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;">
</p>

<p align="center">
  <b>UV della scansione originale vs packing UV ottimizzato generato da ScanReady.</b>
</p>

---

Step 2 genera un nuovo layout UV e prepara il cage per il bake.

Dopo che la scansione è stata semplificata nello Step 1, la mesh ottimizzata ha bisogno di UV pulite per ricevere correttamente le texture sulla nuova superficie low-poly.

Questo step prepara l'asset al trasferimento delle texture, permettendo alla mesh ottimizzata di mantenere gran parte della ricchezza visiva della scansione high-poly originale, restando abbastanza leggera per **VR, videogame, AR, visualizzazione realtime e ambienti interattivi**.

---

## Perché servono le UV

Una mesh semplificata è più leggera e più facile da gestire, ma ha comunque bisogno di coordinate texture coerenti.

Le UV definiscono come la superficie del modello 3D viene aperta nello spazio texture 2D.

Dopo la riduzione, le UV originali della scansione non dovrebbero più essere considerate affidabili sulla mesh ottimizzata.

Poiché la geometria è stata unita e semplificata, il layout UV originale può diventare:

- stirato;
- distorto;
- sovrapposto;
- sporco;
- non allineato alla nuova superficie low-poly.

Senza UV nuove, ScanReady non può trasferire correttamente le informazioni texture dalla scansione originale alla mesh ottimizzata.

Creare UV nuove garantisce bake più puliti e una proiezione texture più affidabile.

<p align="center">
  <img src="../../img/step2-uv-02.png" alt="Confronto checker texture con UV stirate e UV pulite" style="max-width:1000px;width:100%;">
</p>

<p align="center">
  <b>La preview checker aiuta a vedere stretching, densità texel irregolare e distorsioni UV prima del bake.</b>
</p>

---

## Migliore uso dello spazio UV

Le nuove UV migliorano anche l'efficienza dello spazio texture.

Molte scansioni fotogrammetriche contengono layout UV che sprecano grandi porzioni dello spazio texture 0-1.

Dopo l'ottimizzazione, ScanReady può generare un layout UV più pulito, con packing migliore e uso più efficiente delle texture.

<!-- Sostituire il placeholder con ../../img/step2-uv-packing.png -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot efficienza packing UV" style="max-width:1000px;width:100%;">
</p>

Questo permette all'asset ottimizzato di conservare più dettaglio usando meno materiali e meno memoria texture.

UV buone aiutano a ottenere:

- texture bake più pulite;
- migliore nitidezza delle texture;
- meno seam visibili;
- migliori performance realtime;
- risultati più affidabili nei game engine.

---

## Le texture sostituiscono la geometria

L'obiettivo del bake è conservare la ricchezza visiva della scansione originale riducendo la densità dei poligoni.

Invece di mantenere milioni di poligoni, ScanReady trasferisce le informazioni visive della superficie nelle texture.

Questo permette alla mesh ottimizzata di restare leggera pur conservando gran parte dell'aspetto originale.

---

## Perché serve il cage

Il cage controlla come Blender proietta i dettagli dalla scansione high-poly alla mesh ottimizzata durante il bake.

Se il cage è troppo piccolo:

- alcuni dettagli possono non essere catturati;
- possono comparire aree nere;
- possono apparire errori di proiezione.

Se il cage è troppo grande:

- il bake può catturare superfici vicine indesiderate;
- possono apparire artefatti di proiezione.

ScanReady include strumenti per rendere questo processo più veloce e più semplice.

<p align="center">
  <img src="../../img/cage_01_red.png" alt="Avviso cage rosso con setup non valido per il bake" style="max-width:1000px;width:100%;">
</p>

<p align="center">
  <b>Se il cage appare rosso, il bake non proietterà correttamente. Abilita Show Cage, poi aumenta leggermente Cage Extrusion oppure usa Auto Cage Extrusion prima di continuare.</b>
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

Smart UV Project è il metodo automatico di unwrap UV di Blender.

È utile per gli oggetti scansionati perché può generare rapidamente isole UV senza richiedere seam manuali.

ScanReady espone i controlli Smart UV così puoi regolare il comportamento dell'unwrap prima del bake.

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;">
</p>

---

## Impostazioni UV

Queste impostazioni controllano come Smart UV Project apre la mesh ottimizzata.

### Smart UV Preset

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">

ScanReady usa Blender Smart UV Project per la generazione UV automatica.

I preset Smart UV disponibili includono **Detailed**, **Balanced**, **Large Islands** e **Continuous**.

I controlli UV influenzano come la mesh ottimizzata viene aperta prima del bake. Sono separati da Adaptive Reduce, che controlla come la mesh viene semplificata nello Step 1.

Cambiare Smart UV Preset, Smart UV Angle o UV Padding non ricostruisce subito il layout UV corrente. Le nuove impostazioni UV vengono usate la prossima volta che clicchi **Generate UVs**, oppure quando **One Click Bake** esegue lo step di generazione UV. **Bake Textures** usa il layout UV già esistente.

</div>

<div style="flex:0 0 320px; text-align:center;">
  <p style="margin-top:0;"><strong>Smart UV Preset</strong></p>
  <!-- Sostituire il placeholder con ../../img/step2-ui-panel.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder pannello Smart UV Preset di ScanReady" style="width:320px; max-width:100%;">
</div>

</div>

### Smart UV Angle

Controlla quanto aggressivamente Smart UV Project divide la mesh in isole.

Valori più bassi creano più tagli e più isole UV.

Valori più alti creano isole UV più grandi.

### UV Padding

Imposta lo spazio tra le isole UV.

Aumenta il padding per ridurre il texture bleeding, soprattutto a risoluzioni texture più basse.

<!-- Sostituire il placeholder con ../../img/step2-uv-settings.png -->
<p align="center">
  <img src="../../img/step2_UV padding.png" alt="Placeholder pannello impostazioni UV di ScanReady" style="max-width:760px;width:100%;">
</p>

---

## Preview Checker

Usa **Show Checker** per controllare lo stretching UV prima del bake.

La checker texture aiuta a vedere:

- stretching UV;
- distorsione;
- densità texel irregolare;
- isole UV problematiche.

Un pattern checker pulito di solito indica un layout UV più sano per il bake.

<!-- Sostituire il placeholder con ../../img/step2-checker-preview.png -->
<p align="center">
  <img src="../../img/step1-checker.gif" alt="Placeholder screenshot preview checker" style="max-width:1000px;width:100%;">
</p>

---

## Controlli Cage

### Show Cage

Mostra la preview del cage.

Usalo prima del bake per controllare che il cage circondi completamente la mesh ottimizzata.

### Auto Cage Extrusion

Stima automaticamente la cage extrusion campionando la distanza tra la mesh ottimizzata e la scansione high-poly originale.

È utile per generare un punto di partenza rapido senza indovinare manualmente la distanza del cage.

### Cage Extrusion

Controlla manualmente la distanza del cage.

Aumentala se il bake perde dettagli, crea aree nere o produce errori di proiezione.

Usa il valore più piccolo che copre correttamente la superficie della scansione.

<p align="center">
  <img src="../../img/step2_cage_extrusion.gif" alt="Esempio Cage Extrusion in ScanReady" style="max-width:1100px;width:100%;">
</p>

### Cage Opacity

Controlla l'opacità della preview del cage.

Influenza solo la visualizzazione nel viewport e non cambia il risultato del bake.

<p align="center">
  <img src="../../img/step2_cage_opacity.gif" alt="Esempio Cage Opacity in ScanReady" style="max-width:1100px;width:100%;">
</p>

---

## Quando rigenerare le UV

Clicca **Generate UVs** dopo aver creato o aggiornato la preview low-poly.

Se cambi **Smart UV Preset**, **Smart UV Angle** o **UV Padding** dopo aver già generato le UV, clicca di nuovo **Generate UVs** per applicare le nuove impostazioni UV. **Bake Textures** usa il layout UV esistente al momento del bake.

Se sei nello Step 2 e decidi che la mesh ottimizzata è ancora troppo pesante, torna a **Step 1 - Preview / Reduce**. Abbassa **Final Faces** o **Optimize / Reduce**, poi torna allo Step 2 e clicca di nuovo **Generate UVs** in modo che la mesh UV corrisponda alla nuova ottimizzazione.

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
- il cage non sia così grande da catturare superfici vicine indesiderate.

---

## Ottimizzazione realtime

Per workflow VR e videogame, UV e bake permettono a un modello leggero di apparire comunque molto dettagliato.

La mesh ottimizzata dovrebbe conservare le informazioni visive importanti tramite texture, invece che tramite milioni di poligoni.

UV buone e un cage configurato correttamente aiutano a mantenere l'asset:

- più leggero;
- più facile da renderizzare;
- più facile da esportare;
- più affidabile nei motori realtime;
- visivamente più vicino alla scansione originale.
