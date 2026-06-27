# One Click Bake

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-bottom:32px;">

  <div style="flex:1 1 300px; min-width:260px;">
    <p>
      <strong>ONE CLICK BAKE</strong> è il workflow più veloce di ScanReady.
    </p>
    <p>
      È pensato per convertire una scansione high-poly pesante in un asset più leggero con texture bake, con il minimo setup.
      È utile quando prepari modelli scansionati per <strong>VR, AR, videogame, visualizzazione realtime o scene interattive</strong>.
    </p>
  </div>

  <div style="flex:0 0 240px; text-align:center;">
    <img src="../../img/quick-start-one-click.png" alt="Pulsante One Click Bake di ScanReady in Blender" style="width:240px; max-width:100%;">
  </div>

</div>

<p align="center">
  <img src="../../img/one-click-bake.gif" alt="Workflow animato One Click Bake in Blender" style="max-width:820px;width:100%;">
</p>

Invece di ridurre manualmente la mesh, generare UV, preparare il cage e configurare il bake, ScanReady esegue automaticamente il processo principale.

Di default ScanReady parte da un valore **Optimize / Reduce** di **0.10**. Questo significa che la preview low-poly mantiene circa il **10% dei poligoni originali**, producendo circa **90% di poligoni in meno**.

Questo valore funziona bene per molti asset VR, game e realtime. Se il risultato deve avere più o meno dettaglio, regola manualmente il valore in **Step 1 - Preview / Reduce** dopo aver creato la preview low-poly.

One Click Bake è automatico, ma il risultato può comunque essere rifinito dopo.

Se il modello finale risulta troppo pesante, oppure se è stato ottimizzato troppo e perde dettagli importanti della forma, torna a **Step 1 - Preview / Reduce**. Regola **Optimize / Reduce** o **Final Faces**, poi clicca di nuovo **Create Low-poly Preview**.

ScanReady ricostruirà la preview ottimizzata con le nuove impostazioni, così puoi provare una versione più leggera o più dettagliata prima di continuare con UV e bake.

Il workflow è flessibile: anche se sei già in **Step 2 - UV / Cage** o **Step 3 - Bake / Output**, puoi tornare allo Step 1, regolare la riduzione, cliccare **Create Low-poly Preview**, poi continuare di nuovo in avanti.

---

## Cosa fa One Click Bake

Quando clicchi **ONE CLICK BAKE**, ScanReady esegue il workflow completo da scansione ad asset:

1. Pulisce la scansione selezionata rimuovendo rumore comune della mesh, come poligoni staccati, frammenti sospesi e vertici isolati.
2. Crea una preview low-poly dalla scansione high-poly pulita.
3. Esegue la pulizia pre-decimate merge sulla mesh preview duplicata quando serve.
4. Riduce la geometria per rendere il modello più leggero.
5. Genera UV per l'oggetto ottimizzato.
6. Crea o stima il cage per il bake.
7. Cuoce i dettagli texture dalla scansione originale.
8. Costruisce il setup dei materiali finali.
9. Salva le texture bake se **Save Images** è attivo, come da impostazione predefinita.

L'obiettivo è preservare l'identità visiva della scansione originale rendendo il modello più facile da usare nei progetti realtime.

<p align="center">
  <img src="../../img/one_click_before_after.jpg" alt="Confronto prima e dopo di una scansione high-poly ottimizzata con One Click Bake" style="max-width:820px;width:100%;">
</p>

---

## Perché è importante

Le scansioni possono essere troppo pesanti per una produzione realtime.

Una scansione può sembrare buona, ma può essere difficile da usare perché può avere:

- troppi poligoni;
- texture troppo grandi;
- troppi materiali;
- performance lente nel viewport;
- nessuna UV ottimizzata;
- setup di bake complesso;
- uso elevato di memoria;
- densità della mesh non adatta a VR o videogame.

One Click Bake aiuta a ridurre questa complessità.

Ti offre un modo più veloce per trasformare la geometria catturata in un asset più pulito, leggero e con texture bake.

---

## Fasi del workflow

Durante l'operazione, ScanReady passa attraverso le stesse fasi principali usate dal workflow manuale.

### Cleanup

Rimuove le imperfezioni della scansione prima della riduzione, inclusi poligoni staccati, frammenti di geometria sospesi e vertici isolati.

### Preview

Pulisce la scansione selezionata e crea la preview low-poly ottimizzata.

### UV Mapping

Genera le UV per la mesh ottimizzata.

### Cage

Stima la cage extrusion così il bake può proiettare i dettagli dalla scansione originale.

### Bake

Cuoce le texture selezionate e prepara il risultato finale.

Il pannello mostra lo stato del workflow e il progresso globale mentre il processo è in esecuzione.

---

## Interrompere il processo

Se avvii **ONE CLICK BAKE** per errore, puoi premere **Esc** per fermare il workflow.

ScanReady interrompe il processo appena lo step corrente è terminato. In questo modo puoi fermare un avvio accidentale senza aspettare minuti inutili, evitando allo stesso tempo di lasciare la scena in uno stato incompleto durante operazioni delicate come pulizia mesh, generazione UV o setup del cage.

Quando la fase **Step 3 - Bake** è già iniziata, ScanReady lascia completare il bake e la finalizzazione in modo sicuro. Questo riduce il rischio di texture parziali, materiali non collegati o mesh finale non completata.

Dopo uno stop, puoi avviare di nuovo **ONE CLICK BAKE**: ScanReady controlla gli step già validi e riparte dal punto utile del workflow.

---

## Quando usare One Click Bake

Usa One Click Bake quando:

- vuoi il percorso più veloce da scansione ad asset ottimizzato;
- stai lavorando su scansioni fotogrammetriche standard;
- ti serve un asset più leggero per VR, videogame o visualizzazione realtime;
- non hai bisogno di controllare manualmente ogni passaggio;
- vuoi una prima versione rapida prima di rifinire manualmente.

---

## Prima di cliccare

Per ottenere risultati migliori:

- seleziona un solo oggetto high-poly nel 3D Viewport;
- imposta **Optimize / Reduce** oppure **Final Faces** se conosci la densità numerica target della mesh;
- scegli **Texture Size** in base al livello di dettaglio necessario: 512, 1K, 2K, 4K o 8K;
- abilita **Bake Base Color**, **Bake Normal**, **Bake Roughness** o **Bake Occlusion** in base alle mappe che vuoi;
- imposta la **Output Folder** se vuoi salvare le texture in una cartella specifica del disco.

Per scansioni con grandi superfici continue, il preset **Flat Surfaces** di Adaptive Reduce può essere utile prima del bake perché permette di semplificare in modo più aggressivo le aree semplici.

Per veicoli e scansioni hard-surface, **Hard Surface** offre un passaggio approssimato più veloce che protegge meglio gli angoli ortogonali e i cambi di normale più forti.

---

## Dopo il bake

Dopo il completamento del workflow, controlla:

- la densità della mesh finale;
- la silhouette dell'oggetto;
- il materiale bake;
- i file texture salvati;
- il collegamento **Bake Folder** nello Step 3, che apre l'ultima cartella di output texture;
- le mappe Normal, Roughness e AO se abilitate;
- eventuali dettagli mancanti causati dalla distanza del cage o dalle impostazioni di bake.

Se il risultato va regolato, usa il workflow manuale:

- **Step 1 - Preview / Reduce**
- **Step 2 - UV / Cage**
- **Step 3 - Bake / Output**

Gli step manuali danno più controllo sullo stesso processo.
