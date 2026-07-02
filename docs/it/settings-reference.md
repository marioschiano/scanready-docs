# Riferimento impostazioni

<style>
.scanready-settings-list {
  display: grid;
  gap: 1rem;
  margin: 1.25rem 0 2rem;
}
.scanready-setting {
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 1rem 1.1rem;
  background: rgba(255, 255, 255, 0.025);
}
.scanready-setting h3 {
  margin: 0 0 0.65rem;
  font-size: 1.05rem;
}
.scanready-setting p {
  margin: 0.45rem 0 0;
  line-height: 1.65;
}
.scanready-setting strong {
  white-space: nowrap;
}
</style>

Questa pagina riassume le impostazioni principali di ScanReady e cosa fanno.

Usala come riferimento rapido quando regoli scansioni per VR, videogame, visualizzazione realtime o ottimizzazione generale in Blender.

---

## Pannello e stato

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Mesh Stats</h3>
<p><strong>Descrizione:</strong> Mostra facce e triangoli dell'oggetto selezionato o dell'ultima preview creata.</p>
<p><strong>Quando usarla:</strong> Usalo per controllare rapidamente quanto è pesante la mesh prima e dopo la riduzione.</p>
</div>

<div class="scanready-setting">
<h3>Refresh Stats</h3>
<p><strong>Descrizione:</strong> Aggiorna manualmente le statistiche mesh mostrate nel pannello.</p>
<p><strong>Quando usarla:</strong> Usalo dopo aver cambiato selezione o dopo modifiche esterne alla mesh.</p>
</div>

<div class="scanready-setting">
<h3>Workflow Status</h3>
<p><strong>Descrizione:</strong> Mostra progresso globale, step completato, messaggi di stato, mappe bake completate e tempi quando i diagnostics sono attivi.</p>
<p><strong>Quando usarla:</strong> Usalo per capire dove si trova ScanReady durante One Click Bake o durante gli step manuali.</p>
</div>

<div class="scanready-setting">
<h3>Global Progress</h3>
<p><strong>Descrizione:</strong> Percentuale di avanzamento del workflow corrente.</p>
<p><strong>Quando usarla:</strong> Utile durante operazioni lunghe come preview, UV, cage e bake.</p>
</div>

<div class="scanready-setting">
<h3>ONE CLICK BAKE</h3>
<p><strong>Descrizione:</strong> Avvia il workflow automatico completo: preview, UV, cage, bake e materiali finali.</p>
<p><strong>Quando usarla:</strong> Usalo quando vuoi una conversione rapida da scansione high-poly ad asset ottimizzato.</p>
</div>

</div>

---

## Azioni principali

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Create Lowpoly Preview</h3>
<p><strong>Descrizione:</strong> Crea o aggiorna la mesh preview ottimizzata usando le impostazioni dello Step 1 e di Adaptive Reduce.</p>
<p><strong>Quando usarla:</strong> Usalo ogni volta che cambi densità, preset Adaptive Reduce o impostazioni mesh che influenzano la riduzione.</p>
</div>

<div class="scanready-setting">
<h3>Generate UVs</h3>
<p><strong>Descrizione:</strong> Crea la mesh UV dalla preview e genera il layout Smart UV Project.</p>
<p><strong>Quando usarla:</strong> Usalo dopo la preview o quando cambi Smart UV Preset, Smart UV Angle o UV Padding.</p>
</div>

<div class="scanready-setting">
<h3>Auto Cage Extrusion</h3>
<p><strong>Descrizione:</strong> Calcola una cage extrusion di partenza campionando la distanza tra mesh ottimizzata e sorgente high-poly.</p>
<p><strong>Quando usarla:</strong> Usalo prima del bake quando vuoi evitare di stimare manualmente la distanza del cage.</p>
</div>

<div class="scanready-setting">
<h3>Bake Textures</h3>
<p><strong>Descrizione:</strong> Esegue il bake delle mappe selezionate e costruisce la mesh/materiali finali.</p>
<p><strong>Quando usarla:</strong> Usalo dopo aver generato UV e verificato cage/output.</p>
</div>

</div>

---

## Mesh e riduzione

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Final Faces</h3>
<p><strong>Descrizione:</strong> Numero target di facce per la mesh low-poly ottimizzata.</p>
<p><strong>Quando regolarla:</strong> Abbassalo per asset VR/game più leggeri. Alzalo per preservare più dettaglio nella silhouette.</p>
</div>

<div class="scanready-setting">
<h3>Optimize / Reduce</h3>
<p><strong>Descrizione:</strong> Controlla quanto la mesh viene ridotta.</p>
<p><strong>Quando regolarla:</strong> Valori più bassi creano una riduzione più forte. Valori più alti mantengono più geometria.</p>
</div>

<div class="scanready-setting">
<h3>Pre-Decimate Merge</h3>
<p><strong>Descrizione:</strong> Esegue Merge by Distance sulla mesh preview duplicata prima di Decimate. È il singolo controllo esplicito di weld in ScanReady.</p>
<p><strong>Quando regolarla:</strong> Aumentalo per ridurre poligoni sovrapposti prima dell'ottimizzazione. Abbassalo se vengono colpiti dettagli sottili.</p>
</div>

<div class="scanready-setting">
<h3>Auto Clear Sharp Edges</h3>
<p><strong>Descrizione:</strong> Rimuove marcature sharp edge non desiderate durante la preparazione.</p>
<p><strong>Quando regolarla:</strong> Tienilo attivo quando la scansione mostra bordi o shading marcati in modo errato.</p>
</div>

<div class="scanready-setting">
<h3>Auto Combine Mesh Parts</h3>
<p><strong>Descrizione:</strong> Attivo di default. Rileva automaticamente gerarchie con più mesh e le combina quando serve; se la scansione è già una mesh unica non esegue nessuna unione.</p>
<p><strong>Quando regolarla:</strong> Lascialo attivo per GLB, FBX o scansioni fotogrammetriche divise in più parti. Disattivalo solo se l'unione automatica crea problemi o se vuoi mantenere parti separate.</p>
</div>

<div class="scanready-setting">
<h3>Auto Clean Scan Debris</h3>
<p><strong>Descrizione:</strong> Rimuove piccoli frammenti, poligoni sospesi e vertici isolati.</p>
<p><strong>Quando regolarla:</strong> Tienilo attivo per scansioni fotogrammetriche grezze.</p>
</div>

<div class="scanready-setting">
<h3>Convert Source Materials</h3>
<p><strong>Descrizione:</strong> Disattivo di default. Controlla i materiali sorgente: lascia invariati quelli già standard e converte solo shader importati complessi in un setup più prevedibile per il bake.</p>
<p><strong>Quando regolarla:</strong> Attivalo se il bake non esce bene, per esempio Base Color nera/incompleta, o se i materiali importati non vengono letti correttamente.</p>
</div>

<div class="scanready-setting">
<h3>Show Face Orientation</h3>
<p><strong>Descrizione:</strong> Mostra l'overlay Face Orientation di Blender.</p>
<p><strong>Quando regolarla:</strong> Usalo per controllare normali invertite prima di preview, UV o bake.</p>
</div>

<div class="scanready-setting">
<h3>Backface Culling</h3>
<p><strong>Descrizione:</strong> Nasconde nel viewport le facce viste dal lato posteriore. È una modalità di preview e non modifica mesh o bake.</p>
<p><strong>Quando regolarla:</strong> Usalo per individuare superfici a una sola faccia, buchi, parti aperte o orientamenti sospetti. Si disattiva automaticamente quando attivi Show Face Orientation, e viceversa.</p>
</div>

<div class="scanready-setting">
<h3>Adaptive Reduce</h3>
<p><strong>Descrizione:</strong> Usa pesi basati sulla scansione per ridurre di più le superfici piatte e proteggere dettagli importanti.</p>
<p><strong>Quando regolarla:</strong> Tienilo attivo per la maggior parte delle scansioni. Disattivalo solo se vuoi un risultato di riduzione uniforme più semplice.</p>
</div>

<div class="scanready-setting">
<h3>Adaptive Reduce Preset</h3>
<p><strong>Descrizione:</strong> Sceglie il comportamento della riduzione adattiva.</p>
<p><strong>Quando regolarla:</strong> Usa Balanced per la maggior parte delle scansioni, Preserve Details per superfici complesse, Flat Surfaces per superfici semplici ampie, Hard Surface per veicoli e scansioni hard-surface.</p>
</div>

<div class="scanready-setting">
<h3>Show Adaptive Weights</h3>
<p><strong>Descrizione:</strong> Mostra i pesi di riduzione adattiva come colori sul modello.</p>
<p><strong>Quando regolarla:</strong> Usalo per vedere quali aree verranno ridotte di più prima di creare la preview low-poly finale.</p>
</div>

<div class="scanready-setting">
<h3>Adaptive Strength</h3>
<p><strong>Descrizione:</strong> Regola quanto fortemente Adaptive Reduce favorisce la riduzione delle aree piatte.</p>
<p><strong>Quando regolarla:</strong> Alzalo per semplificare di più le superfici regolari, abbassalo se vuoi un comportamento più uniforme.</p>
</div>

<div class="scanready-setting">
<h3>Adaptive Reduce Angle</h3>
<p><strong>Descrizione:</strong> Controlla la sensibilità ai cambi di normale durante il calcolo dei pesi.</p>
<p><strong>Quando regolarla:</strong> Usalo per decidere quanto un cambio di direzione deve essere considerato dettaglio.</p>
</div>

<div class="scanready-setting">
<h3>Detail Preserve</h3>
<p><strong>Descrizione:</strong> Protegge maggiormente le zone lette come dettaglio.</p>
<p><strong>Quando regolarla:</strong> Alzalo se la preview perde pieghe, bordi o dettagli importanti.</p>
</div>

<div class="scanready-setting">
<h3>Smooth Weights</h3>
<p><strong>Descrizione:</strong> Smussa i pesi Adaptive Reduce per transizioni più omogenee.</p>
<p><strong>Quando regolarla:</strong> Aumentalo quando la preview pesi appare troppo puntinata o frastagliata.</p>
</div>

<div class="scanready-setting">
<h3>Fast Adaptive Reduce</h3>
<p><strong>Descrizione:</strong> Usa un calcolo più approssimato e veloce per scansioni dense.</p>
<p><strong>Quando regolarla:</strong> Attivalo per test rapidi o scansioni molto pesanti.</p>
</div>

<div class="scanready-setting">
<h3>Protect Feature Edges</h3>
<p><strong>Descrizione:</strong> Protegge i bordi con differenze di normale forti.</p>
<p><strong>Quando regolarla:</strong> Tienilo attivo per asset hard-surface, veicoli, architettura e silhouette importanti.</p>
</div>

<div class="scanready-setting">
<h3>Feature Edge Angle</h3>
<p><strong>Descrizione:</strong> Angolo minimo per considerare un bordo come feature edge.</p>
<p><strong>Quando regolarla:</strong> Abbassalo per proteggere più bordi, alzalo per proteggere solo rotture più nette.</p>
</div>

<div class="scanready-setting">
<h3>Feature Edge Rings</h3>
<p><strong>Descrizione:</strong> Numero di anelli vicini protetti attorno ai feature edge.</p>
<p><strong>Quando regolarla:</strong> Aumentalo se i bordi netti perdono supporto durante la riduzione.</p>
</div>

<div class="scanready-setting">
<h3>Auto Fix Normals</h3>
<p><strong>Descrizione:</strong> Ricalcola le normali della mesh high prima della creazione della preview.</p>
<p><strong>Quando regolarla:</strong> Attivalo quando la scansione ha normali invertite o artefatti di shading.</p>
</div>

<div class="scanready-setting">
<h3>Recalculate Outside Normals</h3>
<p><strong>Descrizione:</strong> Ricalcola manualmente le normali verso l'esterno.</p>
<p><strong>Quando regolarla:</strong> Usalo quando la mesh appare rovesciata o ha shading rotto.</p>
</div>

</div>

I pesi Adaptive Reduce vengono calcolati quando premi **Create Lowpoly Preview**. Cambiare **Optimize / Reduce** o **Final Faces** dopo quel momento aggiorna la quantità di riduzione, ma cambiare preset o valori dettagliati di Adaptive Reduce richiede di creare di nuovo la preview low-poly per ricostruire i pesi.

Se sei già nello Step 2 o nello Step 3 e ti serve un modello più leggero o più dettagliato, torna allo Step 1, regola **Final Faces** o **Optimize / Reduce**, clicca **Create Lowpoly Preview**, poi rigenera UV e bake.

---

## View e preview

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Show Wireframe</h3>
<p><strong>Descrizione:</strong> Mostra l'overlay wireframe sull'oggetto preview.</p>
<p><strong>Quando regolarla:</strong> Usalo per controllare densità topologica e qualità della riduzione.</p>
</div>

<div class="scanready-setting">
<h3>Show Checker</h3>
<p><strong>Descrizione:</strong> Mostra una texture checker per l'ispezione.</p>
<p><strong>Quando regolarla:</strong> Usalo per controllare distorsione e stretching UV.</p>
</div>

<div class="scanready-setting">
<h3>Checker Mix</h3>
<p><strong>Descrizione:</strong> Controlla la forza dell'overlay checker.</p>
<p><strong>Quando regolarla:</strong> Abbassalo quando vuoi vedere di più la texture originale.</p>
</div>

<div class="scanready-setting">
<h3>Checker UV Scale</h3>
<p><strong>Descrizione:</strong> Cambia la dimensione dei quadrati checker.</p>
<p><strong>Quando regolarla:</strong> Usa quadrati più piccoli per vedere meglio la distorsione.</p>
</div>

<div class="scanready-setting">
<h3>Use Texture View</h3>
<p><strong>Descrizione:</strong> Porta il viewport in modalità Material Preview/Texture View durante i controlli.</p>
<p><strong>Quando regolarla:</strong> Utile per vedere materiali, checker e cage con una visualizzazione più leggibile.</p>
</div>

</div>

**Use Texture View** è disponibile in **Advanced > Mesh Settings** perché di solito non viene regolato durante il workflow principale.

---

## Impostazioni UV

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Smart UV Preset</h3>
<p><strong>Descrizione:</strong> Applica un angolo Smart UV consigliato. I preset includono Detailed, Balanced, Large Islands e Continuous.</p>
<p><strong>Quando regolarla:</strong> Usalo come punto di partenza rapido per tipi comuni di scansione.</p>
</div>

<div class="scanready-setting">
<h3>Smart UV Angle</h3>
<p><strong>Descrizione:</strong> Controlla quanto aggressivamente Smart UV Project divide le isole.</p>
<p><strong>Quando regolarla:</strong> Valori più bassi creano più tagli. Valori più alti creano isole più grandi.</p>
</div>

<div class="scanready-setting">
<h3>UV Padding</h3>
<p><strong>Descrizione:</strong> Aggiunge spazio tra le isole UV.</p>
<p><strong>Quando regolarla:</strong> Aumentalo per ridurre texture bleeding e seam visibili.</p>
</div>

</div>

### Generazione UV

ScanReady usa **Smart UV Project** per generare le UV.

I preset **Adaptive Reduce** sono separati dalle impostazioni UV: controllano come viene semplificata la mesh prima della generazione UV e del bake.

Se modifichi una di queste impostazioni dopo che le UV sono già state create:

- **Smart UV Preset**
- **Smart UV Angle**
- **UV Padding**

clicca di nuovo **Generate UVs** prima di eseguire il bake.

In questo modo ScanReady ricrea il layout UV sulla mesh ottimizzata usando i nuovi valori.

---

## Impostazioni cage

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Show Cage</h3>
<p><strong>Descrizione:</strong> Mostra la preview del cage.</p>
<p><strong>Quando regolarla:</strong> Usalo prima del bake per controllare la copertura della proiezione.</p>
</div>

<div class="scanready-setting">
<h3>Auto Cage Extrusion</h3>
<p><strong>Descrizione:</strong> Stima automaticamente la cage extrusion.</p>
<p><strong>Quando regolarla:</strong> Usalo quando vuoi un setup cage veloce.</p>
</div>

<div class="scanready-setting">
<h3>Cage Extrusion</h3>
<p><strong>Descrizione:</strong> Distanza manuale del cage.</p>
<p><strong>Quando regolarla:</strong> Aumentala se mancano dettagli. Abbassala se vengono catturate aree sbagliate.</p>
</div>

<div class="scanready-setting">
<h3>Cage Opacity</h3>
<p><strong>Descrizione:</strong> Controlla l'opacità della preview cage.</p>
<p><strong>Quando regolarla:</strong> Regolala solo per la visibilità nel viewport. Non influenza il bake.</p>
</div>

</div>

---

## Texture e bake

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Texture Preset / Texture Size</h3>
<p><strong>Descrizione:</strong> Imposta la risoluzione delle texture bake.</p>
<p><strong>Quando regolarla:</strong> Alzala per asset ravvicinati. Abbassala per asset VR/game leggeri.</p>
</div>

<div class="scanready-setting">
<h3>Bake Materials</h3>
<p><strong>Descrizione:</strong> Divide il bake in più gruppi di materiali.</p>
<p><strong>Quando regolarla:</strong> Aumentalo per scansioni grandi che richiedono più dettaglio texture. Valori sopra <code>1</code> abilitano automaticamente Force CPU Baking.</p>
</div>

<div class="scanready-setting">
<h3>Texture Detail</h3>
<p><strong>Descrizione:</strong> Sezione avanzata dedicata all'analisi del dettaglio texture e dello spazio UV.</p>
<p><strong>Quando regolarla:</strong> Usala quando vuoi capire se texture size e numero materiali sono bilanciati.</p>
</div>

<div class="scanready-setting">
<h3>Analyze Texture Detail</h3>
<p><strong>Descrizione:</strong> Avvia l'analisi high-to-UV e mostra raccomandazioni su texture/materiali.</p>
<p><strong>Quando regolarla:</strong> Usalo in Advanced prima del bake quando non sei sicuro della risoluzione o del numero di materiali.</p>
</div>

<div class="scanready-setting">
<h3>Bake Samples</h3>
<p><strong>Descrizione:</strong> Imposta il numero di sample Cycles per il bake.</p>
<p><strong>Quando regolarla:</strong> Alzalo per bake più puliti, soprattutto AO. Abbassalo per test più rapidi.</p>
</div>

<div class="scanready-setting">
<h3>Bake Margin</h3>
<p><strong>Descrizione:</strong> Aggiunge padding attorno alle isole UV bake.</p>
<p><strong>Quando regolarla:</strong> Aumentalo per ridurre seam e texture bleeding.</p>
</div>

<div class="scanready-setting">
<h3>Bake Base Color</h3>
<p><strong>Descrizione:</strong> Cuoce la texture colore principale.</p>
<p><strong>Quando regolarla:</strong> Tienilo attivo quando vuoi preservare il colore originale della scansione.</p>
</div>

<div class="scanready-setting">
<h3>Bake Normal Map</h3>
<p><strong>Descrizione:</strong> Cuoce o trasferisce una normal map.</p>
<p><strong>Quando regolarla:</strong> Se il materiale high ha una normal texture collegata, ScanReady la trasferisce. Altrimenti esegue un bake normal geometrico high-to-low.</p>
</div>

<div class="scanready-setting">
<h3>Bake Roughness Map</h3>
<p><strong>Descrizione:</strong> Trasferisce roughness dal materiale high quando è collegata una roughness texture.</p>
<p><strong>Quando regolarla:</strong> Attivalo quando l'asset finale deve mantenere variazione roughness dal materiale originale.</p>
</div>

<div class="scanready-setting">
<h3>Bake Occlusion Map</h3>
<p><strong>Descrizione:</strong> Cuoce una mappa Ambient Occlusion.</p>
<p><strong>Quando regolarla:</strong> Attivalo per aggiungere profondità e ombre di contatto.</p>
</div>

<div class="scanready-setting">
<h3>Normal Strength</h3>
<p><strong>Descrizione:</strong> Controllo avanzato della forza del nodo Normal Map.</p>
<p><strong>Quando regolarla:</strong> Regolalo in Advanced > Bake Settings se il dettaglio normal appare troppo debole o troppo forte.</p>
</div>

</div>

---

## Ambient Occlusion

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>AO Source</h3>
<p><strong>Descrizione:</strong> Sceglie come viene cotta AO.</p>
<p><strong>Quando regolarla:</strong> Usa high-to-low per trasferire dettaglio dalla scansione, oppure low-only per AO più semplice.</p>
</div>

<div class="scanready-setting">
<h3>AO Auto Distance</h3>
<p><strong>Descrizione:</strong> Calcola automaticamente la distanza AO dalla dimensione del modello.</p>
<p><strong>Quando regolarla:</strong> Lascialo attivo per la maggior parte degli asset.</p>
</div>

<div class="scanready-setting">
<h3>AO Distance</h3>
<p><strong>Descrizione:</strong> Distanza manuale dei raggi AO.</p>
<p><strong>Quando regolarla:</strong> Regolalo quando la distanza automatica produce AO troppo forte o troppo debole.</p>
</div>

<div class="scanready-setting">
<h3>AO Samples</h3>
<p><strong>Descrizione:</strong> Controlla il numero di sample per il bake AO.</p>
<p><strong>Quando regolarla:</strong> Alzalo per AO più pulita. Abbassalo per bake più rapidi.</p>
</div>

<div class="scanready-setting">
<h3>AO Mix</h3>
<p><strong>Descrizione:</strong> Controlla quanto la AO bake scurisce il materiale Base Color finale.</p>
<p><strong>Quando regolarla:</strong> Il default è <code>1.0</code>. Abbassalo se il materiale finale sembra troppo scuro o contrastato.</p>
</div>

</div>

---

## Impostazioni output

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Save Images</h3>
<p><strong>Descrizione:</strong> Salva le texture bake su disco.</p>
<p><strong>Quando regolarla:</strong> Attivalo quando esporti verso game engine, archivi o tool esterni.</p>
</div>

<div class="scanready-setting">
<h3>Open Folder After Bake</h3>
<p><strong>Descrizione:</strong> Apre automaticamente la cartella del bake quando il salvataggio texture è completato.</p>
<p><strong>Quando regolarla:</strong> Utile durante test e produzione, soprattutto quando vuoi controllare subito i file generati.</p>
</div>

<div class="scanready-setting">
<h3>Image Format</h3>
<p><strong>Descrizione:</strong> Sceglie JPG, PNG o TIFF.</p>
<p><strong>Quando regolarla:</strong> Usa JPG per color map compatte, PNG per output lossless, TIFF per alta precisione.</p>
</div>

<div class="scanready-setting">
<h3>JPG Quality</h3>
<p><strong>Descrizione:</strong> Controlla la qualità di compressione JPG.</p>
<p><strong>Quando regolarla:</strong> Alzalo per migliore qualità. Abbassalo per file più piccoli.</p>
</div>

<div class="scanready-setting">
<h3>TIFF 16-bit</h3>
<p><strong>Descrizione:</strong> Salva texture TIFF con precisione più alta.</p>
<p><strong>Quando regolarla:</strong> Usalo per asset ravvicinati, workflow archivio o mappe dettagliate.</p>
</div>

<div class="scanready-setting">
<h3>Output Folder</h3>
<p><strong>Descrizione:</strong> Cartella dove vengono salvate le texture bake.</p>
<p><strong>Quando regolarla:</strong> Impostala prima del bake se vuoi i file in una cartella specifica del progetto.</p>
</div>

<div class="scanready-setting">
<h3>Bake Folder</h3>
<p><strong>Descrizione:</strong> Mostra la cartella usata dall'ultimo bake e fornisce un pulsante per aprirla.</p>
<p><strong>Quando regolarla:</strong> Usalo dopo il bake per controllare o copiare rapidamente i file texture salvati.</p>
</div>

</div>

---

## Sicurezza memoria

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Safe Memory Bake</h3>
<p><strong>Descrizione:</strong> Usa un workflow bake più sicuro per scene pesanti.</p>
<p><strong>Quando regolarla:</strong> Tienilo attivo per scansioni grandi o alte risoluzioni texture.</p>
</div>

<div class="scanready-setting">
<h3>Force CPU Baking</h3>
<p><strong>Descrizione:</strong> Forza il bake su CPU invece che GPU.</p>
<p><strong>Quando regolarla:</strong> Disattivo di default con un materiale. Abilitato automaticamente quando Bake Materials è <code>2</code> o superiore, e disattivabile manualmente.</p>
</div>

</div>

---

## Preset

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Preset Name</h3>
<p><strong>Descrizione:</strong> Nome usato quando salvi le impostazioni correnti.</p>
<p><strong>Quando usarlo:</strong> Usa un nome chiaro per un workflow o tipo di asset.</p>
</div>

<div class="scanready-setting">
<h3>Save Preset</h3>
<p><strong>Descrizione:</strong> Salva le impostazioni correnti.</p>
<p><strong>Quando usarlo:</strong> Usalo prima di processare scansioni simili.</p>
</div>

<div class="scanready-setting">
<h3>Preset Selector</h3>
<p><strong>Descrizione:</strong> Menu con i preset salvati disponibili.</p>
<p><strong>Quando usarlo:</strong> Usalo per scegliere quale preset ricaricare o eliminare.</p>
</div>

<div class="scanready-setting">
<h3>Reload Preset</h3>
<p><strong>Descrizione:</strong> Ricarica il preset selezionato.</p>
<p><strong>Quando usarlo:</strong> Usalo per ripetere un setup noto o tornare rapidamente a un preset salvato.</p>
</div>

<div class="scanready-setting">
<h3>Delete Preset</h3>
<p><strong>Descrizione:</strong> Elimina il preset selezionato.</p>
<p><strong>Quando usarlo:</strong> Usalo per rimuovere setup vecchi o inutilizzati.</p>
</div>

</div>

---

## Diagnostics

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Show Diagnostic Timing Report</h3>
<p><strong>Descrizione:</strong> Mostra un report dettagliato dei tempi dopo One Click Bake, con sotto-report per Adaptive/Decimate e Bake/Finalize.</p>
<p><strong>Quando usarlo:</strong> Tienilo disattivato per video e uso normale. Abilitalo quando vuoi analizzare performance o confrontare test.</p>
</div>

</div>

---

## Addon Preferences / Updates

<div class="scanready-settings-list">

<div class="scanready-setting">
<h3>Installed version</h3>
<p><strong>Descrizione:</strong> Mostra la versione di ScanReady installata.</p>
<p><strong>Quando usarlo:</strong> Usalo per controllare rapidamente quale build è attiva in Blender.</p>
</div>

<div class="scanready-setting">
<h3>Updates are managed by Blender Extensions / Superhive</h3>
<p><strong>Descrizione:</strong> Ricorda che gli aggiornamenti pubblici vengono gestiti dalla piattaforma di distribuzione.</p>
<p><strong>Quando usarlo:</strong> Utile per capire dove cercare l'aggiornamento ufficiale dell'addon.</p>
</div>

<div class="scanready-setting">
<h3>Open Documentation</h3>
<p><strong>Descrizione:</strong> Apre la documentazione online di ScanReady.</p>
<p><strong>Quando usarlo:</strong> Usalo quando vuoi consultare guida rapida, workflow, FAQ o troubleshooting.</p>
</div>

<div class="scanready-setting">
<h3>Release Notes</h3>
<p><strong>Descrizione:</strong> Apre il changelog e la pagina release notes di ScanReady.</p>
<p><strong>Quando usarlo:</strong> Usalo per vedere cosa è cambiato prima di aggiornare.</p>
</div>

<div class="scanready-setting">
<h3>Video Tutorials</h3>
<p><strong>Descrizione:</strong> Apre il canale YouTube con i tutorial ScanReady.</p>
<p><strong>Quando usarlo:</strong> Usalo quando preferisci vedere il workflow in video.</p>
</div>

</div>

---

## Punti di partenza consigliati

### Asset VR leggero

|Impostazione|Direzione consigliata|
|---||---|
|**Final Faces**|Più basso|
|**Texture Size**|1024 o 2048|
|**Bake Normal Map**|Attivo se il dettaglio superficie è importante|
|**Bake Occlusion Map**|Opzionale|
|**Safe Memory Bake**|Attivo|
|**Bake Materials**|Mantienilo basso|

### Game prop

|Impostazione|Direzione consigliata|
|---||---|
|**Final Faces**|Medio|
|**Texture Size**|2048|
|**Bake Base Color**|Attivo|
|**Bake Normal Map**|Attivo|
|**Bake Occlusion Map**|Opzionale|
|**Image Format**|PNG o JPG in base alla pipeline|

### Asset da presentazione ravvicinata

|Impostazione|Direzione consigliata|
|---||---|
|**Final Faces**|Più alto|
|**Texture Size**|4096 o superiore|
|**Bake Normal Map**|Attivo|
|**Bake Occlusion Map**|Attivo|
|**Bake Samples**|Più alto|
|**Image Format**|PNG o TIFF|

---

## Regola generale

Per il realtime, non conservare il dettaglio solo come geometria.

Usa la geometria per la forma principale e usa texture bake per il dettaglio visivo.

Questo equilibrio rende gli asset scansionati più facili da usare in VR, videogame, viewer realtime e scene interattive.
