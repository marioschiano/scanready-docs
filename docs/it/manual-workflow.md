# Guida manuale

Usa questa guida quando vuoi seguire ScanReady passo dopo passo, invece di usare **One Click Bake**.

Il workflow manuale ti permette di controllare separatamente riduzione, UV, cage e bake. È utile quando vuoi decidere con più precisione quanto ottimizzare la mesh, come generare le UV e quali texture creare.

---

## Step 1 - Crea la preview low-poly

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Seleziona la scansione high-poly nel viewport di Blender.</li>
    <li>Apri <strong>STEP 1 Preview / Reduce</strong>.</li>
    <li>Regola <strong>Optimize / Reduce</strong> o <strong>Final Faces</strong> se vuoi una mesh più leggera o più dettagliata.</li>
    <li>Clicca <strong>Create Low-poly Preview</strong>.</li>
  </ol>

  <p>ScanReady pulisce la scansione, crea una copia ottimizzata e genera una preview low-poly non distruttiva. La scansione high-poly originale resta intatta e viene usata come sorgente per UV, cage e bake.</p>

  <p>Quando la preview ti sembra corretta, passa a <strong>Step 2 - UV / Cage</strong>.</p>
</div>

<div style="flex:0 0 260px; max-width:260px;">
  <img src="../../img/manual-step1.jpg" alt="Pannello STEP 1 Preview Reduce con pulsante Create Low-poly Preview" style="width:100%;">
</div>

</div>

---

## Step 2 - Genera UV e controlla il cage

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Parti dalla preview low-poly creata nello Step 1.</li>
    <li>Apri <strong>STEP 2 UV / Cage</strong>.</li>
    <li>Clicca <strong>Generate UVs</strong>.</li>
  </ol>

  <p>ScanReady crea un nuovo layout UV sulla mesh ottimizzata. Questo prepara l'asset per ricevere le texture bake sulla nuova superficie low-poly.</p>

  <p>Dopo le UV, controlla il cage:</p>

  <ul>
    <li>abilita <strong>Show Cage</strong>;</li>
    <li>verifica che il cage copra la superficie high-poly;</li>
    <li>usa <strong>Auto Cage Extrusion</strong> se vuoi una stima automatica;</li>
    <li>regola <strong>Cage Extrusion</strong> se devi correggere manualmente la distanza.</li>
  </ul>

  <p>Quando UV e cage sono pronti, passa a <strong>Step 3 - Bake / Output</strong>.</p>
</div>

<div style="flex:0 0 320px; max-width:320px; display:flex; flex-direction:column; gap:14px;">
  <img src="../../img/manual-step2.jpg" alt="Interfaccia STEP 2 UV Cage con pulsante Generate UVs" style="width:100%;">
  <img src="../../img/manual-step2_cage.jpg" alt="Interfaccia STEP 2 UV Cage con Show Cage e controlli cage" style="width:100%;">
</div>

</div>

---

## Step 3 - Esegui il bake

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Apri <strong>STEP 3 Bake / Output</strong>.</li>
    <li>Scegli <strong>Texture Preset / Texture Size</strong>.</li>
    <li>Imposta <strong>Bake Materials</strong>.</li>
    <li>Attiva le mappe che vuoi generare, per esempio <strong>Bake Base Color</strong>, <strong>Bake Normal</strong>, <strong>Bake Roughness</strong> o <strong>Bake Occlusion</strong>.</li>
    <li>Clicca <strong>Bake Textures</strong>.</li>
  </ol>

  <p>ScanReady esegue il bake una texture alla volta, collega le texture generate al materiale finale e crea un asset più leggero pronto per realtime, VR, videogame, AR e scene interattive.</p>

  <p>Prima di cliccare <strong>Bake Textures</strong>, controlla che il cage copra la scansione high-poly. Se il cage è troppo piccolo, possono comparire aree nere, dettagli mancanti o proiezioni errate.</p>
</div>

<div style="flex:0 0 260px; max-width:260px;">
  <img src="../../img/manual-step3.jpg" alt="Pannello ScanReady con gli step del workflow e Bake Output" style="width:100%;">
</div>

</div>

---

## Se vuoi ottimizzare di più

Puoi tornare indietro in qualsiasi momento.

Se sei già nello Step 2 o nello Step 3 e ti accorgi che la mesh è ancora troppo pesante, torna a **Step 1 - Preview / Reduce**, abbassa **Final Faces** o **Optimize / Reduce**, poi clicca di nuovo **Create Low-poly Preview**.

Dopo aver ricreato la preview, continua di nuovo in avanti:

1. torna a **Step 2 - UV / Cage**;
2. clicca di nuovo **Generate UVs**;
3. controlla il cage;
4. torna a **Step 3 - Bake / Output**;
5. clicca **Bake Textures**.

Il bake dovrebbe sempre usare la mesh UV ottimizzata più recente.

---

## Quando usare le pagine Step dettagliate

Questa pagina ti dice cosa premere e in quale ordine.

Per capire meglio ogni fase, usa le pagine dedicate:

- [Step 1 - Preview / Reduce](step1.md) per Adaptive Reduce, Optimize / Reduce, Final Faces e preview.
- [Step 2 - UV / Cage](step2.md) per Smart UV Project, checker, cage e Auto Cage Extrusion.
- [Step 3 - Bake / Output](step3.md) per texture size, bake materials, mappe bake, output e salvataggio immagini.
