# Guida rapida

Questa pagina mostra il modo più veloce per usare ScanReady.

<p align="center">
  <img src="../../img/hero.png" alt="Panoramica del workflow ScanReady" style="max-width:620px;width:100%;">
</p>

---

## Workflow base

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

  <div style="flex:1 1 360px; min-width:260px;">

    <p>Per una prima prova veloce e automatica:</p>

    <ol>
      <li>Seleziona la mesh high-poly della scansione.</li>
      <li>Imposta <strong>Final Faces</strong> se vuoi un target specifico.</li>
      <li>Lascia <strong>Optimize / Reduce</strong> a <strong>0.10</strong> per una riduzione di circa il 90%.</li>
      <li>Scegli la dimensione texture.</li>
      <li>Attiva le mappe che vuoi cuocere.</li>
      <li>Clicca <strong>ONE CLICK BAKE</strong>.</li>
    </ol>

  </div>

  <div style="flex:0 0 260px; text-align:center;">
    <img src="../../img/quick-start-one-click.png" alt="Pulsante One Click Bake di ScanReady in Blender" style="width:260px; max-width:100%;">
  </div>

</div>

---

## Cosa succede automaticamente

Quando usi **ONE CLICK BAKE**, ScanReady esegue il workflow principale:

1. Pulisce la scansione selezionata.
2. Crea una preview low-poly ottimizzata.
3. Genera le UV.
4. Prepara il cage.
5. Esegue il bake delle texture selezionate.
6. Crea il materiale finale.
7. Salva le immagini se **Save Images** è attivo, come da impostazione predefinita.

Il modello viene quindi ottimizzato, riceve nuove UV e può ottenere il bake delle texture selezionate in un unico workflow.

<p align="center">
  <img src="../../img/one-click-bake.gif" alt="Workflow One Click Bake di ScanReady in Blender" style="max-width:820px;width:100%;">
</p>

---

## Impostazioni consigliate per la prima prova

Per una scansione standard:

- **Optimize / Reduce:** `0.10`
- **Final Faces:** `4000` oppure un target adatto al tuo asset
- **Adaptive Reduce:** attivo
- **Adaptive Preset:** `Balanced`
- **Texture Size:** `2048`
- **Bake Base Color:** attivo
- **Bake Normal Map:** attivo se ti serve dettaglio di superficie
- **Save Images:** attivo se vuoi salvare le texture su disco

---

## Risultato rapido

Dopo il bake dovresti ottenere:

- una mesh finale più leggera;
- UV generate automaticamente;
- texture bake collegate al materiale;
- file immagine salvati nella cartella di output, se abilitato.

Controlla il risultato nel viewport e nella sezione **Step 3 - Bake / Output**.

Se il modello finale risulta ancora troppo pesante, oppure se è stato ottimizzato troppo e perde dettagli importanti della forma, torna a **Step 1 - Preview / Reduce**. Regola **Optimize / Reduce** o **Final Faces** e osserva l'aggiornamento della preview. Quando il risultato ti convince, passa allo Step 2 e clicca di nuovo **Generate UVs**.

Il workflow è flessibile: anche se sei già in **Step 2 - UV / Cage** oppure **Step 3 - Bake / Output**, puoi tornare allo Step 1, regolare la riduzione dei poligoni e poi proseguire di nuovo verso UV e bake.

---

## Quando usare gli step manuali

Usa il workflow manuale se vuoi più controllo:

- [Step 1 - Preview / Reduce](step1.md) per regolare la densità della mesh.
- [Step 2 - UV / Cage](step2.md) per controllare UV e cage.
- [Step 3 - Bake / Output](step3.md) per gestire texture, materiali e output.
