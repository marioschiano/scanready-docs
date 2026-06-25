# Step 2 - UV / Cage

<p align="center">
  <img src="../../img/step2-uv-01.jpg" alt="Layout UV generato da ScanReady dalla mesh ottimizzata" style="max-width:760px;width:100%;">
</p>

<p align="center">
  <b>UV della scansione originale vs packing UV ottimizzato generato da ScanReady.</b>
</p>

---

Step 2 genera un nuovo layout UV e prepara il cage per il bake.

Dopo che la scansione è stata semplificata nello Step 1, la mesh ottimizzata ha bisogno di UV pulite per ricevere correttamente le texture sulla nuova superficie lowpoly.

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
- non allineato alla nuova superficie lowpoly.

Senza UV nuove, ScanReady non può trasferire correttamente le informazioni texture dalla scansione originale alla mesh ottimizzata.

Creare UV nuove garantisce bake più puliti e una proiezione texture più affidabile.

<p align="center">
  <img src="../../img/step2-uv-02.png" alt="Confronto checker texture con UV stirate e UV pulite" style="max-width:1000px;width:100%;">
</p>

<p align="center">
  <b>La preview checker aiuta a vedere stretching, densità texel irregolare e distorsioni UV prima del bake.</b>
</p>

---
