# Step 2 - UV / Cage

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;" decoding="async" fetchpriority="high">
</p>

<p align="center">
  <b>UV della scansione originale vs packing UV ottimizzato generato da ScanReady.</b>
</p>

---

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-top:16px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">

<p>Step 2 genera un nuovo layout UV e prepara il cage per il bake.</p>

<p>Dopo che la scansione è stata semplificata nello Step 1, la mesh ottimizzata ha bisogno di UV pulite per ricevere correttamente le texture sulla nuova superficie low-poly.</p>

<p>Questo step prepara l'asset al trasferimento delle texture, permettendo alla mesh ottimizzata di mantenere gran parte della ricchezza visiva della scansione high-poly originale, restando abbastanza leggera per <strong>VR, videogame, AR, visualizzazione in tempo reale e ambienti interattivi</strong>.</p>

</div>

<div style="flex:0 0 280px; text-align:center;">
  <p style="margin-top:0;"><strong>STEP 2 UV / Cage</strong></p>
  <img src="../../img/step2-uv-cage-panel.png" alt="Pannello Step 2 UV e Cage con Smart UV, Show Cage, Cage Extrusion e Generate UVs" style="max-width:280px;width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## Da quattro materiali a un unico layout UV

Quando una scansione è composta da più materiali, ogni materiale può avere il proprio layout UV. Nell'esempio seguente il modello high-poly usa quattro materiali e quattro layout UV separati.

ScanReady semplifica il workflow creando sulla mesh ottimizzata un unico materiale e un unico layout UV, più semplice da gestire e pronto per il bake.

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../../img/step2-uv-four-materials.jpg" alt="UV originali separate per quattro materiali" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay">
      <img src="../../img/step2-uv-one-material.jpg" alt="Layout UV unico della mesh ottimizzata ScanReady" class="sr-uv-compare__top" loading="lazy" decoding="async">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">4 materiali · 4 layout UV</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">1 materiale · 1 layout UV</span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Confronta UV separate e layout UV unico" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Sposta il cursore per confrontare le UV originali con il layout unico generato da ScanReady.</strong></p>

Il vantaggio non è solo visivo: un unico materiale e un unico atlas semplificano il bake, l'esportazione e la gestione dell'asset nei motori realtime.

---

## Perché rifare le UV della scansione

Le UV create dalla scansione originale non sono sempre adatte a una mesh ottimizzata. Spesso sono molto frammentate, con un numero elevato di piccole isole, e non sfruttano in modo efficiente tutto lo spazio texture **0-1**.

Questo può lasciare grandi aree vuote nell'atlas, distribuire male la densità dei texel e rendere il bake più difficile da controllare. Dopo la riduzione della mesh, inoltre, il vecchio layout non descrive più in modo ideale la nuova superficie low-poly.

ScanReady genera quindi un nuovo layout UV più ordinato e compatto. Le isole vengono ridotte e impacchettate in modo più efficiente, così la superficie ottimizzata può utilizzare meglio la texture e ricevere il dettaglio trasferito dalla scansione high-poly.

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../../img/step2-uv-original-fragmented.jpg" alt="Layout UV originale frammentato" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay">
      <img src="../../img/step2-uv-scanready-packed.jpg" alt="Layout UV ScanReady ordinato e compatto" class="sr-uv-compare__top" loading="lazy" decoding="async">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">UV originale</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">ScanReady</span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Confronta UV originale e UV ScanReady" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Usa il cursore per confrontare direttamente le due versioni.</strong></p>

Il confronto con la checker texture rende visibile il risultato: nella scansione originale il pattern è spezzato da molte piccole isole e da una densità poco uniforme; dopo **Generate UVs**, il pattern segue la superficie in modo più regolare e il layout è più adatto al bake.

Rifare le UV non aggiunge dettaglio geometrico alla mesh. Permette però di organizzare meglio la superficie che riceverà le texture, migliorando l'efficienza dell'atlas e la qualità del trasferimento dal modello high-poly.

---



Una mesh semplificata è più leggera e più facile da gestire, ma ha comunque bisogno di coordinate texture coerenti.

Le UV definiscono come la superficie del modello 3D viene aperta nello spazio texture 2D.

Dopo la riduzione, le UV originali della scansione non dovrebbero più essere considerate affidabili sulla mesh ottimizzata.

Poiché la geometria è stata unita e semplificata, il layout UV originale può diventare:

- stirato;
- distorto;
- sovrapposto;
- sporco;
- non allineato alla nuova superficie low-poly.

Nel workflow ScanReady, usa **Generate UVs** per preparare la mesh destinata al bake. Il nuovo layout deve avere isole ben separate e uno spazio texture adeguato: controllalo prima di procedere.

<p align="center">
  <img src="../../img/step2-uv-02.jpg" alt="Confronto checker texture con UV stirate e UV pulite" style="max-width:1000px;width:100%;" loading="lazy" decoding="async">
</p>

<p align="center">
  <b>La preview checker aiuta a vedere stretching, densità texel irregolare e distorsioni UV prima del bake.</b>
</p>

---

## Migliore uso dello spazio UV

Le nuove UV migliorano anche l'efficienza dello spazio texture.

Molte scansioni fotogrammetriche contengono layout UV che sprecano grandi porzioni dello spazio texture 0-1.

Dopo l'ottimizzazione, ScanReady può generare un layout UV più pulito, con packing migliore e uso più efficiente delle texture.

<p align="center">
  <img src="../../img/step2-uv-packing-efficient.jpg" alt="Packing UV ottimizzato in un unico atlas per ridurre draw call e semplificare l'esportazione" style="max-width:1000px;width:100%;" loading="lazy" decoding="async">
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
  <img src="../../img/cage_01_red.jpg" alt="Avviso cage rosso con setup non valido per il bake" style="max-width:1000px;width:100%;" loading="lazy" decoding="async">
</p>

!!! warning "Cage rosso"
    Il rosso segnala che il controllo automatico rileva una copertura insufficiente: alcune zone potrebbero non essere raggiunte dai raggi del bake.

    Abilita **Show Cage**, poi aumenta leggermente **Cage Extrusion** oppure usa **Auto Cage Extrusion** prima di continuare.

<p align="center">
  <img src="../../img/step2-uv-03.jpg" alt="Confronto cage troppo piccolo, corretto e troppo grande" style="max-width:1100px;width:100%;" loading="lazy" decoding="async">
</p>

<p align="center">
  <b>Cage troppo piccoli perdono dettagli. Cage troppo grandi possono catturare superfici vicine indesiderate.</b>
</p>

<p align="center">
  <img src="../../img/step2-uv-04.jpg" alt="Confronto di come la dimensione del cage influenza la normal map baked" style="max-width:1100px;width:100%;" loading="lazy" decoding="async">
</p>

<p align="center">
  <b>La dimensione del cage influenza direttamente il bake: un cage corretto cattura i dettagli in modo pulito senza proiettare geometria indesiderata.</b>
</p>


---

## Cage e risultato del bake

Il cage controlla la distanza entro cui Blender cerca i dettagli della scansione high-poly durante il bake. Il confronto seguente mostra prima la copertura della cage e poi il risultato ottenuto sulla texture.

### 1. Copertura della cage

<div class="sr-uv-compare" data-cage-compare>
  <div class="sr-uv-compare__image">
    <img src="../../img/step2-cage-insufficient.png" alt="Cage insufficiente con aree rosse non coperte" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay">
      <img src="../../img/step2-cage-correct.png" alt="Cage corretta con copertura verde della superficie" class="sr-uv-compare__top" loading="lazy" decoding="async">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Cage insufficiente</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">Cage corretta</span>
    <span class="sr-uv-compare__material sr-uv-compare__material--left"><strong>Rosso</strong><small>Copertura incompleta</small></span>
    <span class="sr-uv-compare__material sr-uv-compare__material--right"><strong>Verde</strong><small>Copertura completa</small></span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Confronta cage insufficiente e cage corretta" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Sposta il cursore per confrontare la copertura della cage.</strong></p>

La superficie rossa indica che la cage è troppo bassa e non copre completamente la mesh high-poly. La superficie verde indica invece una cage che avvolge correttamente il modello e può raggiungere i dettagli durante la proiezione.

### 2. Risultato del bake

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../../img/step2-bake-insufficient.png" alt="Bake con cage insufficiente, macchie nere e dettagli persi" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay">
      <img src="../../img/step2-bake-correct.png" alt="Bake con cage corretta e dettagli trasferiti correttamente" class="sr-uv-compare__top" loading="lazy" decoding="async">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Bake con errori</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">Bake corretto</span>
    <span class="sr-uv-compare__material sr-uv-compare__material--left"><strong>Cage troppo bassa</strong><small>Dettagli persi</small></span>
    <span class="sr-uv-compare__material sr-uv-compare__material--right"><strong>Cage corretta</strong><small>Texture pulita</small></span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Confronta bake con cage insufficiente e bake con cage corretta" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Sposta il cursore per vedere come la cage influenza il risultato del bake.</strong></p>

<p class="sr-cage-warning">Un cage troppo piccolo impedisce ai raggi del bake di raggiungere tutta la superficie. Possono comparire macchie nere, dettagli mancanti e artefatti, soprattutto sui bordi e sulla curva dell’arco.</p>
---

## Metodo UV

ScanReady usa **Smart UV Project** per generare UV sulla mesh ottimizzata.

Smart UV Project è il metodo automatico di unwrap UV di Blender.

È utile per gli oggetti scansionati perché può generare rapidamente isole UV senza richiedere seam manuali.

ScanReady espone i controlli Smart UV così puoi regolare il comportamento dell'unwrap prima del bake.

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;" loading="lazy" decoding="async">
</p>

---

## Impostazioni UV

**Smart UV Preset** è nello **Step 2** (etichetta compatta **Smart UV**). **Smart UV Angle** e **UV Padding** sono in **Advanced > UV Settings**.

### Smart UV Preset

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-top:16px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">

<p>ScanReady usa Blender Smart UV Project per la generazione UV automatica.</p>

<p>I preset Smart UV disponibili includono <strong>Detailed</strong>, <strong>Balanced</strong>, <strong>Large Islands</strong> e <strong>Continuous</strong>.</p>

<ul>
<li><strong>Balanced</strong>: compromesso tra dimensione delle isole, densità texel e uso dello spazio UV. È il preset consigliato nella maggior parte dei casi.</li>
<li><strong>Detailed</strong>: crea più isole e segue la superficie in modo più preciso, utile quando vuoi preservare meglio le variazioni locali della mesh.</li>
<li><strong>Large Islands</strong>: privilegia isole UV più grandi e meno frammentate. Può sembrare simile a Balanced, ma tende a ridurre maggiormente il numero di isole anche quando il packing è meno uniforme.</li>
<li><strong>Continuous</strong>: favorisce isole più continue e coerenti lungo la superficie, utile quando vuoi limitare interruzioni e frammentazione del layout.</li>
</ul>

<p>I controlli UV influenzano come la mesh ottimizzata viene aperta prima del bake. Sono separati da Adaptive Reduce, che controlla come la mesh viene semplificata nello Step 1.</p>


</div>

<div style="flex:0 0 280px; text-align:center;">
  <p style="margin-top:0;"><strong>Smart UV Preset</strong></p>
  <img src="../../img/step2-smart-uv-preset-panel.png" alt="Menu Smart UV Preset con opzioni Detailed, Balanced, Large Islands e Continuous" style="max-width:280px;width:100%;" loading="lazy" decoding="async">
</div>

</div>

<p align="center">
  <img src="../../img/step2-smart-uv-presets.jpg" alt="Confronto dei preset Smart UV Balanced, Detailed, Large Islands e Continuous" style="max-width:1100px;width:100%;" loading="lazy" decoding="async">
</p>

<div class="admonition note">
  <p class="admonition-title">Le UV si aggiornano quando le rigeneri</p>
  <p>Cambiare <strong>Smart UV Preset</strong>, <strong>Smart UV Angle</strong> o <strong>UV Padding</strong> non ricostruisce subito il layout UV corrente.</p>
  <p>Le nuove impostazioni UV vengono usate la prossima volta che clicchi <strong>Generate UVs</strong>, oppure quando <strong>One Click Bake</strong> esegue lo step di generazione UV. <strong>Bake Textures</strong> usa il layout UV già esistente.</p>
</div>


### Smart UV Angle

Controlla quanto aggressivamente Smart UV Project divide la mesh in isole.

Valori più bassi creano più tagli e più isole UV.

Valori più alti creano isole UV più grandi.

### UV Padding

Imposta lo spazio tra le isole UV.

Aumenta il padding per ridurre il texture bleeding, soprattutto a risoluzioni texture più basse.

<p align="center">
  <img src="../../img/step2_UV padding.jpg" alt="Pannello impostazioni UV di ScanReady" style="max-width:760px;width:100%;" loading="lazy" decoding="async">
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

<!-- Esempio condiviso con Step 1. -->
<p align="center">
  <img src="../../img/step2-checker-preview.jpg" alt="Confronto tra UV stirate e UV pulite tramite la checker texture" style="max-width:1000px;width:100%;" loading="lazy" decoding="async">
</p>

---

## Controlli Cage

### Show Cage

Mostra la preview del cage.

Usalo prima del bake per controllare che il cage, generato dalla mesh ottimizzata, copra la superficie high-poly da campionare.

### Auto Cage Extrusion

Stima automaticamente la cage extrusion campionando la distanza tra la mesh ottimizzata e la scansione high-poly originale.

È utile per generare un punto di partenza rapido senza indovinare manualmente la distanza del cage.

### Cage Extrusion

Controlla manualmente la distanza del cage.

Aumentala se il bake perde dettagli, crea aree nere o produce errori di proiezione.

Usa il valore più piccolo che copre correttamente la superficie della scansione.

<p align="center">
  <img src="../../img/step2_cage_extrusion.gif" alt="Esempio Cage Extrusion in ScanReady" style="max-width:1100px;width:100%;" loading="lazy" decoding="async">
</p>

### Cage Opacity

Controlla l'opacità della preview del cage.

Influenza solo la visualizzazione nel viewport e non cambia il risultato del bake.

<p align="center">
  <img src="../../img/step2_cage_opacity.gif" alt="Esempio Cage Opacity in ScanReady" style="max-width:1100px;width:100%;" loading="lazy" decoding="async">
</p>

---

## Quando rigenerare le UV

!!! note "Quando cliccare Generate UVs"
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

