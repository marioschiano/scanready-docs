# Guida manuale

Usa questa guida quando vuoi seguire ScanReady passo dopo passo, invece di usare **One Click Bake**.

Il workflow manuale ti permette di controllare separatamente riduzione, UV, cage e bake. È utile quando vuoi decidere con più precisione quanto ottimizzare la mesh, come generare le UV e quali texture creare.

---

## Step 1 - Crea la preview low-poly

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 360px; min-width:260px;">

1. Seleziona la scansione high-poly nel viewport di Blender.
2. Apri **STEP 1 Preview / Reduce**.
3. Regola **Optimize / Reduce** o **Final Faces** se vuoi una mesh più leggera o più dettagliata.
4. Clicca **Create Low-poly Preview**.

ScanReady pulisce la scansione, crea una copia ottimizzata e genera una preview low-poly non distruttiva. La scansione high-poly originale resta intatta e viene usata come sorgente per UV, cage e bake.

Quando la preview ti sembra corretta, passa a **Step 2 - UV / Cage**.

</div>

<div style="flex:0 1 300px; min-width:240px;">
  <img src="../../img/step1-preview-reduce.png" alt="Pannello STEP 1 Preview Reduce con pulsante Create Low-poly Preview" style="width:100%; max-width:300px;">
</div>

</div>

---

## Step 2 - Genera UV e controlla il cage

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 360px; min-width:260px;">

1. Parti dalla preview low-poly creata nello Step 1.
2. Apri **STEP 2 UV / Cage**.
3. Clicca **Generate UVs**.

ScanReady crea un nuovo layout UV sulla mesh ottimizzata. Questo prepara l'asset per ricevere le texture bake sulla nuova superficie low-poly.

Dopo le UV, controlla il cage:

- abilita **Show Cage**;
- verifica che il cage copra la superficie high-poly;
- usa **Auto Cage Extrusion** se vuoi una stima automatica;
- regola **Cage Extrusion** se devi correggere manualmente la distanza.

Quando UV e cage sono pronti, passa a **Step 3 - Bake / Output**.

</div>

<div style="flex:0 1 460px; min-width:260px;">
  <img src="../../img/step2_cage_extrusion.gif" alt="Interfaccia STEP 2 UV Cage con Generate UVs e controlli cage" style="width:100%; max-width:460px;">
</div>

</div>

---

## Step 3 - Esegui il bake

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 360px; min-width:260px;">

1. Apri **STEP 3 Bake / Output**.
2. Scegli **Texture Preset / Texture Size**.
3. Imposta **Bake Materials**.
4. Attiva le mappe che vuoi generare, per esempio **Bake Base Color**, **Bake Normal**, **Bake Roughness** o **Bake Occlusion**.
5. Clicca **Bake Textures**.

ScanReady esegue il bake una texture alla volta, collega le texture generate al materiale finale e crea un asset più leggero pronto per realtime, VR, videogame, AR e scene interattive.

Prima di cliccare **Bake Textures**, controlla che il cage copra la scansione high-poly. Se il cage è troppo piccolo, possono comparire aree nere, dettagli mancanti o proiezioni errate.

</div>

<div style="flex:0 1 300px; min-width:240px;">
  <img src="../../img/quick-start-one-click.png" alt="Pannello ScanReady con gli step del workflow e Bake Output" style="width:100%; max-width:300px;">
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
