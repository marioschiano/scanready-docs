# Impostazioni avanzate

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Le impostazioni avanzate danno controllo preciso su pulizia mesh, riduzione adattiva, generazione UV, qualità bake, output immagini, preset, diagnostica e sicurezza memoria.
</p>

<p>
Advanced è la parte più tecnica di ScanReady. Qui puoi modificare il cuore del workflow quando vuoi andare oltre il risultato automatico, rifinire una scansione difficile o adattare il processo a un asset pensato per VR, videogame o realtime.
</p>

<p>
Non serve cambiare ogni impostazione per usare ScanReady. Per la maggior parte delle scansioni, parti dai valori predefiniti e intervieni solo quando hai bisogno di più controllo su qualità, performance, accuratezza del bake o protezione dei dettagli.
</p>

<p>
Il pannello Advanced raccoglie le impostazioni che influenzano le fasi principali del processo: cleanup della scansione, riduzione adattiva, generazione UV, bake delle texture, gestione memoria, preset e diagnostica.
</p>

<p>
Usalo in modo graduale: prima crea una preview low-poly con i valori predefiniti, poi torna in Advanced solo se vuoi correggere qualcosa o migliorare il risultato. Se cambi impostazioni che influenzano mesh, Adaptive Reduce o UV, rigenera lo step corrispondente prima di continuare.
</p>

<p>
Le sezioni principali seguono l'ordine del workflow. Mesh Settings prepara e pulisce la scansione prima della preview low-poly. Adaptive Reduce controlla come ScanReady protegge dettagli, bordi e cambi di normale durante la riduzione. UV Settings gestisce l'apertura UV usata dal bake.
</p>

<p>
Bake Settings e Occlusion Settings regolano qualità, margini, normal map, roughness e occlusion. Memory Safety, Preset, Diagnostics e Utilities aiutano nei workflow pesanti, nei test, nel riuso delle impostazioni e nel ripristino rapido di una configurazione pulita.
</p>
</div>

<div style="flex:0 0 320px; text-align:center;">
  <p style="margin-top:0;"><strong>Advanced</strong></p>
  <!-- Sostituire con ../../img/advanced-overview.png -->
  <img src="../../img/advanced_global.jpg" alt="Panoramica impostazioni Advanced di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

# Mesh Settings

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

Queste impostazioni controllano pulizia scansione e preparazione mesh prima di generare la preview low-poly.

</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Mesh Settings</strong></p>
  <!-- Sostituire con ../../img/advanced-mesh-settings.png -->
  <img src="../../img/advanced_mesh_settings.jpg" alt="Placeholder screenshot Mesh Settings di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Pre-Decimate Merge</h3>

<p>
Esegue una pulizia Merge by Distance sulla mesh preview duplicata prima che venga aggiunto il modificatore Decimate.
</p>

<p>
È il singolo controllo esplicito di weld in ScanReady. Può aiutare a ridurre poligoni sovrapposti della scansione prima dell'ottimizzazione. Se dopo l'ottimizzazione compaiono buchi nel modello o vengono colpiti dettagli sottili, abbassa il valore e crea di nuovo la preview low-poly.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Pre-Decimate Merge</strong></p>
  <!-- Sostituire con ../../img/advanced-pre-decimate-merge.png -->
  <img src="../../img/advanced_pre_decimate.jpg" alt="Placeholder screenshot Pre-Decimate Merge di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Fix Normals</h3>

<p>
Ricalcola automaticamente le normali della mesh high-poly prima di creare la preview low-poly.
</p>

<p>
Attivalo quando la scansione ha normali invertite, shading rotto o artefatti di bake causati da direzioni normali errate.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Fix Normals</strong></p>
  <!-- Sostituire con ../../img/advanced-auto-fix-normals.png -->
  <img src="../../img/advanced_autofix_normals.jpg" alt="Placeholder screenshot Auto Fix Normals di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-auto-fix-normals-detail.png -->
  <img src="../../img/advanced_autofix_normals.gif" alt="Placeholder dettaglio Auto Fix Normals di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Clear Sharp Edges</h3>

<p>
Rimuove automaticamente marcature sharp edge dalla mesh durante la preparazione.
</p>

<p>
È utile quando una scansione importata contiene edge marcati come sharp in modo non desiderato, causando shading duro o bake meno puliti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Clear Sharp Edges</strong></p>
  <!-- Sostituire con ../../img/advanced-auto-clear-sharp-edges.png -->
  <img src="../../img/advanced_autoclear_sharp.jpg" alt="Placeholder screenshot Auto Clear Sharp Edges di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-auto-clear-sharp-edges-detail.png -->
  <img src="../../img/advanced_autoclear_sharp_edge.gif" alt="Placeholder dettaglio Auto Clear Sharp Edges di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Combine Mesh Parts</h3>

<p>
Combina automaticamente più parti mesh della scansione quando lavori con import composti da molti oggetti separati. È attivo di default.
</p>

<p>
ScanReady controlla da solo se la selezione contiene una gerarchia con tante mesh da unire. Se la scansione è già una mesh unica, non esegue nessuna unione.
</p>

<p>
Lascialo attivo nella maggior parte dei casi, soprattutto con scansioni da fotogrammetria, GLB o FBX divisi in più elementi. Disattivalo solo se l'unione automatica crea problemi o se vuoi mantenere intenzionalmente parti mesh separate.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Combine Mesh Parts</strong></p>
  <!-- Sostituire con ../../img/advanced-auto-combine-mesh-parts.png -->
  <img src="../../img/advanced_autocombine_mesh.jpg" alt="Placeholder screenshot Auto Combine Mesh Parts di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-auto-combine-mesh-parts-detail.png -->
  <img src="../../img/advanced_autocombine_mesh.gif" alt="Placeholder dettaglio Auto Combine Mesh Parts di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Clean Scan Debris</h3>

<p>
Rimuove detriti comuni della scansione, come frammenti isolati, poligoni sospesi e vertici non utili prima della riduzione.
</p>

<p>
È attivo di default perché molte scansioni grezze contengono piccole parti volanti che possono rallentare ottimizzazione, UV e bake.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Clean Scan Debris</strong></p>
  <!-- Sostituire con ../../img/advanced-auto-clean-scan-debris.png -->
  <img src="../../img/advanced_autoclean_scan.jpg" alt="Placeholder screenshot Auto Clean Scan Debris di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-auto-clean-scan-debris-detail.png -->
  <img src="../../img/advanced_auto_clean_scan.gif" alt="Placeholder dettaglio Auto Clean Scan Debris di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Convert Source Materials</h3>

<p>
Converte i materiali sorgente della scansione in una configurazione più pulita e prevedibile per il workflow di ScanReady.
</p>

<p>
Alcuni modelli importati, soprattutto da file GLB, Sketchfab o librerie online, possono usare materiali complessi o collegamenti poco adatti al bake. Per esempio, una texture diffuse può essere collegata all'Emission invece che al Base Color.
</p>

<p>
Quando questa opzione è attiva, ScanReady ricostruisce i materiali usando uno shader standard <strong>Principled BSDF</strong> di Blender. Questo rende il bake più coerente e aiuta a evitare risultati strani causati da shader importati troppo complessi.
</p>

<p>
Lascialo disattivato se vuoi mantenere i materiali sorgente il più possibile invariati. Attivalo quando i materiali importati sono complessi, non vengono letti correttamente, oppure producono un bake poco prevedibile.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Convert Source Materials</strong></p>
  <!-- Sostituire con ../../img/advanced-convert-source-materials.png -->
  <img src="../../img/advanced_convert_source.jpg" alt="Placeholder screenshot Convert Source Materials di ScanReady" style="width:260px; max-width:100%;">
</div>
<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-auto-clean-scan-debris-detail.png -->
  <img src="../../img/advanced_convert_source_materials.gif" alt="Placeholder dettaglio Auto Clean Scan Debris di ScanReady" style="width:760px; max-width:100%;">
</div>
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Show Face Orientation</h3>

<p>
Mostra l'overlay <strong>Face Orientation</strong> di Blender per controllare rapidamente se le facce del modello sono orientate nel verso corretto.
</p>

<p>
In Blender le facce hanno una direzione: un lato è considerato esterno e l'altro interno. Se alcune facce sono invertite, il modello può sembrare corretto nella viewport, ma durante il bake può creare problemi come zone nere, dettagli mancanti, ombre sbagliate o texture trasferite male.
</p>

<p>
Usa <strong>Show Face Orientation</strong> prima di creare la preview low-poly o prima del bake per verificare che la scansione non abbia normali invertite. Le facce evidenziate in rosso indicano normalmente superfici orientate al contrario e possono causare problemi durante il bake.
</p>

<p>
Quando attivi <strong>Show Face Orientation</strong>, ScanReady disattiva automaticamente <strong>Backface Culling</strong> per evitare controlli visivi sovrapposti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Show Face Orientation</strong></p>
  <!-- Sostituire con ../../img/advanced-show-face-orientation.png -->
  <img src="../../img/advanced_showface_orientation.jpg" alt="Placeholder screenshot Show Face Orientation di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-show-face-orientation-detail.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder dettaglio Show Face Orientation di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Backface Culling</h3>

<p>
Attiva il <strong>Backface Culling</strong> del viewport per controllare come si comportano le facce quando vengono viste dal lato posteriore.
</p>

<p>
È una modalità di visualizzazione utile per individuare possibili problemi nella scansione, come facce invertite, superfici a una sola faccia, buchi, parti aperte o aree con orientamento sospetto.
</p>

<p>
Questo controllo è importante prima del bake: anche se il modello può sembrare corretto nella viewport, facce orientate male o parti aperte possono causare texture nere, dettagli mancanti, ombre errate o trasferimenti non corretti dalla mesh high-poly alla mesh ottimizzata.
</p>

<p>
<strong>Backface Culling</strong> è solo una modalità di preview: non modifica la mesh e non cambia direttamente il bake. Serve a controllare meglio la scansione prima di procedere.
</p>

<p>
Backface Culling e Show Face Orientation sono collegati: se attivi uno, ScanReady disattiva automaticamente l'altro. In questo modo controlli la scansione con una sola modalità diagnostica alla volta.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Backface Culling</strong></p>
  <!-- Sostituire con ../../img/advanced-backface-culling.png -->
  <img src="../../img/advanced_backface_culling .jpg" alt="Placeholder screenshot Backface Culling di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-backface-culling-detail.png -->
  <img src="../../img/advanced_backface_culling_2.jpg" alt="Placeholder dettaglio Backface Culling di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Use Texture View</h3>

<p>
Mostra il modello in una visualizzazione piatta senza illuminazione di scena.
</p>

<p>
È utile per ispezionare più chiaramente risultati texture bake o preview.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Use Texture View</strong></p>
  <!-- Sostituire con ../../img/advanced-use-texture-view.png -->
  <img src="../../img/advanced_usetexture_view.jpg" alt="Placeholder screenshot Use Texture View di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-use-texture-view-detail.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder dettaglio Use Texture View di ScanReady" style="width:760px; max-width:100%;">
</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Recalculate Outside Normals</h3>

<p>
Esegue manualmente il ricalcolo delle normali sulla mesh high-poly selezionata.
</p>

<p>
Usalo quando la scansione appare rovesciata o ha shading incoerente.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Recalculate Outside Normals</strong></p>
  <!-- Sostituire con ../../img/advanced-recalculate-outside-normals.png -->
  <img src="../../img/advanced_recalculate_outside_normals.jpg" alt="Placeholder screenshot Recalculate Outside Normals di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <!-- Sostituire con ../../img/advanced-recalculate-outside-normals-detail.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder dettaglio Recalculate Outside Normals di ScanReady" style="width:760px; max-width:100%;">
</div>

---

# Adaptive Reduce

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Adaptive Reduce controlla come ScanReady distribuisce la riduzione sulla scansione selezionata.
</p>

<p>
È attivo di default ed è progettato per proteggere il dettaglio visivamente importante, permettendo alle superfici piatte di essere semplificate di più.
</p>

<p>
I pesi Adaptive Reduce vengono calcolati quando clicchi <strong>Create Low-poly Preview</strong>. Cambiare <strong>Optimize / Reduce</strong> o <strong>Final Faces</strong> dopo quel momento aggiorna la quantità di riduzione, ma non ricalcola i pesi adattivi. Per applicare un preset Adaptive Reduce diverso o valori adattivi dettagliati, crea di nuovo la preview low-poly.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Adaptive Reduce</strong></p>
  <!-- Sostituire con ../../img/advanced-adaptive-reduce.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Adaptive Reduce di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Reduce</h3>

<p>
Abilita o disabilita il sistema di riduzione adattiva.
</p>

<p>
Quando è attivo, ScanReady analizza la mesh e crea pesi per proteggere dettagli importanti, bordi e cambi di normale, semplificando di più le aree piatte o meno rilevanti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce</strong></p>
  <!-- Sostituire con ../../img/advanced-adaptive-reduce.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Adaptive Reduce di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Reduce Preset</h3>

<p>
Scegli il preset più adatto alla scansione e all'asset target.
</p>

<ul>
<li><strong>Balanced</strong> è il preset predefinito per la maggior parte delle scansioni.</li>
<li><strong>Preserve Details</strong> protegge più fortemente regioni complesse o importanti della superficie.</li>
<li><strong>Flat Surfaces</strong> riduce in modo più aggressivo le aree ampie e semplici.</li>
<li><strong>Hard Surface</strong> è un preset approssimato più veloce per veicoli e scansioni hard-surface; protegge solo rotture di normale più forti.</li>
</ul>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce Preset</strong></p>
  <!-- Sostituire con ../../img/advanced-adaptive-reduce-preset.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Adaptive Reduce Preset di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Show Adaptive Weights</h3>

<p>
Mostra una preview a colori di come ScanReady distribuirà la riduzione sulla scansione.
</p>

<p>
Le aree rosse rappresentano superfici più piatte che possono essere ridotte di più. Le aree blu e verdi rappresentano regioni protette per il dettaglio.
</p>

<p>
La visualizzazione è solo un aiuto di preview. Serve a scegliere il preset e capire il comportamento della riduzione; non è una texture esportata o baked.
</p>

<p>
I pesi Adaptive Reduce vengono calcolati quando clicchi <strong>Create Low-poly Preview</strong>. Dopo che la preview esiste, cambiare <strong>Optimize / Reduce</strong> o <strong>Final Faces</strong> aggiorna la quantità di riduzione usando i pesi esistenti. Se cambi preset o valori dettagliati di Adaptive Reduce, clicca di nuovo <strong>Create Low-poly Preview</strong> per ricostruire i pesi con le nuove impostazioni.
</p>

<p>
Usa questa preview quando una scansione ha superfici miste, come pannelli architettonici piatti insieme a dettagli scultorei o danneggiati.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Show Adaptive Weights</strong></p>
  <!-- Sostituire con ../../img/advanced-show-adaptive-weights.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Show Adaptive Weights di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Reduce Strength</h3>

<p>
Controlla quanto fortemente i pesi adattivi influenzano la riduzione.
</p>

<p>
Valori più alti rendono più marcata la differenza tra aree protette e aree semplificate. Valori più bassi producono un comportamento più vicino a una riduzione uniforme.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce Strength</strong></p>
  <!-- Sostituire con ../../img/advanced-adaptive-reduce-strength.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Adaptive Reduce Strength di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Reduce Angle</h3>

<p>
Controlla la sensibilità ai cambi di normale usati per distinguere aree piatte, curvature e dettagli.
</p>

<p>
Valori più bassi rendono ScanReady più sensibile alle variazioni di superficie. Valori più alti tendono a considerare più aree come relativamente uniformi.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce Angle</strong></p>
  <!-- Sostituire con ../../img/advanced-adaptive-reduce-angle.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Adaptive Reduce Angle di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Detail Preserve</h3>

<p>
Regola quanta protezione viene data ai dettagli della superficie durante il calcolo dei pesi.
</p>

<p>
Aumentalo quando la scansione contiene dettagli fini che non vuoi perdere. Abbassalo quando vuoi una riduzione più aggressiva.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Detail Preserve</strong></p>
  <!-- Sostituire con ../../img/advanced-detail-preserve.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Detail Preserve di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Smooth Weights</h3>

<p>
Smussa i pesi Adaptive Reduce per rendere la transizione tra aree protette e aree ridotte più omogenea.
</p>

<p>
Valori più alti possono produrre una distribuzione meno frastagliata, utile su scansioni rumorose o superfici irregolari.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Smooth Weights</strong></p>
  <!-- Sostituire con ../../img/advanced-smooth-weights.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Smooth Weights di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Fast Adaptive Reduce</h3>

<p>
Usa una modalità più veloce e approssimata del calcolo adattivo.
</p>

<p>
È utile per preview rapide o asset hard-surface, perché riduce il tempo di analisi saltando parte della rifinitura regionale. I bordi con normali molto diverse restano comunque protetti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Fast Adaptive Reduce</strong></p>
  <!-- Sostituire con ../../img/advanced-fast-adaptive-reduce.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Fast Adaptive Reduce di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Protect Feature Edges</h3>

<p>
Protegge bordi importanti e rotture nette della superficie durante la riduzione.
</p>

<p>
È consigliato per scansioni hard-surface, veicoli, architettura, oggetti con spigoli visibili o silhouette importanti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Protect Feature Edges</strong></p>
  <!-- Sostituire con ../../img/advanced-protect-feature-edges.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Protect Feature Edges di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Feature Edge Angle</h3>

<p>
Definisce l'angolo minimo usato per considerare un bordo come feature edge da proteggere.
</p>

<p>
Valori più bassi proteggono più bordi. Valori più alti proteggono solo cambi di direzione più netti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Feature Edge Angle</strong></p>
  <!-- Sostituire con ../../img/advanced-feature-edge-angle.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Feature Edge Angle di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Feature Edge Rings</h3>

<p>
Estende la protezione dei feature edge anche agli anelli di geometria vicini.
</p>

<p>
Può aiutare a mantenere più stabile la forma attorno a bordi netti, cornici, pannelli o separazioni evidenti della scansione.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Feature Edge Rings</strong></p>
  <!-- Sostituire con ../../img/advanced-feature-edge-rings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Feature Edge Rings di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# UV Settings

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Queste impostazioni controllano come Smart UV Project apre la mesh ottimizzata.
</p>

<blockquote>
<p><strong>Nota:</strong> le impostazioni UV vengono applicate quando ScanReady genera le UV.</p>
<p>Se cambi valori UV dopo aver già creato il layout, clicca di nuovo <strong>Generate UVs</strong> oppure esegui <strong>One Click Bake</strong> dall'inizio.</p>
<p><strong>Bake Textures</strong> usa sempre il layout UV già esistente al momento del bake.</p>
</blockquote>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>UV Settings</strong></p>
  <!-- Sostituire con ../../img/advanced-uv-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot UV Settings di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Smart UV Angle</h3>

<p>
Controlla quanto Smart UV Project divide la mesh in isole UV.
</p>

<ul>
<li>Valori più bassi creano più tagli e più isole UV.</li>
<li>Valori più alti creano isole più grandi.</li>
</ul>

<p>
Puoi regolare manualmente questo valore quando vuoi più controllo sull'unwrap usato per il bake.
</p>

<p>
I preset Adaptive Reduce sono separati dalla generazione UV: Adaptive Reduce controlla la semplificazione della mesh, mentre Smart UV Project controlla l'apertura UV.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Smart UV Angle</strong></p>
  <!-- Sostituire con ../../img/advanced-smart-uv-angle.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Smart UV Angle di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>UV Padding</h3>

<p>
Imposta lo spazio tra le isole UV.
</p>

<p>
Aumenta il padding per ridurre texture bleeding, soprattutto a risoluzioni texture più basse.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>UV Padding</strong></p>
  <!-- Sostituire con ../../img/advanced-uv-padding.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot UV Padding di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Bake Settings

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Queste impostazioni controllano qualità bake, padding texture, qualità formato immagine, analisi Texture Detail, opzioni Occlusion e sicurezza memoria.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Bake Settings</strong></p>
  <!-- Sostituire con ../../img/advanced-bake-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Bake Settings di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Bake Samples</h3>

<p>
Imposta il numero di sample Cycles usati per il bake.
</p>

<p>
Valori più alti possono ridurre il rumore, soprattutto per Ambient Occlusion, ma aumentano anche il tempo di bake.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Bake Samples</strong></p>
  <!-- Sostituire con ../../img/advanced-bake-samples.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Bake Samples di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Bake Margin</h3>

<p>
Aggiunge padding in pixel attorno alle isole UV bake.
</p>

<p>
Aiuta a ridurre seam visibili e texture bleeding.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Bake Margin</strong></p>
  <!-- Sostituire con ../../img/advanced-bake-margin.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Bake Margin di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Texture Detail</h3>

<p>
Analizza la sorgente high-poly e la mesh UV ottimizzata per stimare se texture size e numero di materiali bake correnti possono preservare abbastanza dettaglio della scansione.
</p>

<p>
Usa <strong>Analyze Texture Detail</strong> dopo aver generato le UV, prima del bake, quando vuoi aiuto per decidere se aumentare la risoluzione texture, aumentare i materiali bake o migliorare il packing UV.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Texture Detail</strong></p>
  <!-- Sostituire con ../../img/advanced-texture-detail.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Texture Detail di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Normal Strength</h3>

<p>
Appare quando <strong>Bake Normal</strong> è abilitato.
</p>

<p>
Controlla la forza del nodo Normal Map nel materiale finale. Cambia solo l'aspetto del materiale; non cambia la texture normal bake.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Normal Strength</strong></p>
  <!-- Sostituire con ../../img/advanced-normal-strength.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Normal Strength di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>JPG Quality</h3>

<p>
Controlla la qualità di compressione JPG quando il formato immagine selezionato è JPG.
</p>

<p>
Valori più alti preservano più dettaglio immagine ma creano file più grandi.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>JPG Quality</strong></p>
  <!-- Sostituire con ../../img/advanced-jpg-quality.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot JPG Quality di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>TIFF 16-bit</h3>

<p>
Abilita output TIFF a precisione più alta quando il formato selezionato è TIFF.
</p>

<p>
Può essere utile per asset dettagliati, workflow archivio o output texture tecnico.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>TIFF 16-bit</strong></p>
  <!-- Sostituire con ../../img/advanced-tiff-16-bit.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot TIFF 16-bit di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Occlusion Settings

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Queste opzioni appaiono quando <strong>Bake Occlusion</strong> è abilitato.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Occlusion Settings</strong></p>
  <!-- Sostituire con ../../img/advanced-occlusion-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Occlusion Settings di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>AO Source</h3>

<p>
Controlla se Ambient Occlusion viene cotta dalla sorgente high-poly al target low-poly, oppure calcolata solo dalla mesh low-poly.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Source</strong></p>
  <!-- Sostituire con ../../img/advanced-ao-source.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot AO Source di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>AO Auto Distance</h3>

<p>
Calcola automaticamente la distanza AO in base alla dimensione del modello.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Auto Distance</strong></p>
  <!-- Sostituire con ../../img/advanced-ao-auto-distance.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot AO Auto Distance di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>AO Distance</h3>

<p>
Distanza manuale dei raggi AO quando la distanza automatica è disattivata.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Distance</strong></p>
  <!-- Sostituire con ../../img/advanced-ao-distance.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot AO Distance di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>AO Samples</h3>

<p>
Controlla la qualità del bake Ambient Occlusion.
</p>

<p>
Valori più alti producono AO più pulita ma aumentano il tempo di bake.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Samples</strong></p>
  <!-- Sostituire con ../../img/advanced-ao-samples.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot AO Samples di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>AO Mix</h3>

<p>
Controlla quanto la texture Ambient Occlusion bake scurisce il materiale Base Color finale.
</p>

<p>
Il valore predefinito è <strong>1.0</strong>, che usa tutta la texture AO bake nel materiale finale. Valori più bassi rendono l'effetto AO più sottile.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Mix</strong></p>
  <!-- Sostituire con ../../img/advanced-ao-mix.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot AO Mix di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Memory Safety

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Queste opzioni aiutano a ridurre problemi di memoria durante operazioni di bake pesanti.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Memory Safety</strong></p>
  <!-- Sostituire con ../../img/advanced-memory-safety.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Memory Safety di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Safe Memory Bake</h3>

<p>
Usa un workflow bake più sicuro pensato per ridurre la pressione sulla memoria in scansioni grandi e scene Blender pesanti.
</p>

<p>
Lascialo attivo quando lavori con asset fotogrammetrici densi o alte risoluzioni texture.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Safe Memory Bake</strong></p>
  <!-- Sostituire con ../../img/advanced-safe-memory-bake.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Safe Memory Bake di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Force CPU Baking</h3>

<p>
Forza il bake sulla CPU per evitare limiti di memoria GPU.
</p>

<p>
Di solito è più lento, ma può essere più sicuro su sistemi con poca VRAM.
</p>

<p>
ScanReady può abilitarlo automaticamente quando viene usato il bake multi-materiale.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Force CPU Baking</strong></p>
  <!-- Sostituire con ../../img/advanced-force-cpu-baking.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Force CPU Baking di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Preset

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
ScanReady può salvare, ricaricare ed eliminare preset con nome.
</p>

<p>
I preset salvano le impostazioni correnti del workflow così puoi riutilizzarle in seguito.
</p>

<p>
Usa i preset quando lavori su più scansioni con requisiti simili, come:
</p>

<ul>
<li>asset VR;</li>
<li>game prop;</li>
<li>oggetti museali;</li>
<li>impostazioni bake ripetute;</li>
<li>workflow standard di studio.</li>
</ul>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Preset</strong></p>
  <!-- Sostituire con ../../img/advanced-preset.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Preset di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Preset Name</h3>

<p>
Definisce il nome del preset da salvare.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Preset Name</strong></p>
  <!-- Sostituire con ../../img/advanced-preset-name.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Preset Name di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Save Preset</h3>

<p>
Salva le impostazioni correnti di ScanReady come preset riutilizzabile.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Save Preset</strong></p>
  <!-- Sostituire con ../../img/advanced-save-preset.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Save Preset di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Preset Selector</h3>

<p>
Permette di scegliere un preset esistente.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Preset Selector</strong></p>
  <!-- Sostituire con ../../img/advanced-preset-selector.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Preset Selector di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Reload Preset</h3>

<p>
Carica il preset selezionato.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Reload Preset</strong></p>
  <!-- Sostituire con ../../img/advanced-reload-preset.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Reload Preset di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Delete Preset</h3>

<p>
Elimina il preset selezionato.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Delete Preset</strong></p>
  <!-- Sostituire con ../../img/advanced-delete-preset.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Delete Preset di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Diagnostics

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Le opzioni di diagnostica servono per controllare meglio cosa sta facendo ScanReady durante i test o l'ottimizzazione delle prestazioni.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Diagnostics</strong></p>
  <!-- Sostituire con ../../img/advanced-diagnostics.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Diagnostics di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Show Diagnostic Timing Report</h3>

<p>
Mostra un report dettagliato dei tempi dopo <strong>ONE CLICK BAKE</strong>.
</p>

<p>
Il report può includere dettagli come tempo di Preview / Reduce, Generate UVs, Auto Cage, Bake / Finalize, Adaptive / Decimate e singole sottofasi del bake.
</p>

<p>
È disattivato di default per mantenere il pannello più pulito durante l'uso normale, le demo e i video. Abilitalo solo quando vuoi analizzare le prestazioni o confrontare impostazioni diverse.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Show Diagnostic Timing Report</strong></p>
  <!-- Sostituire con ../../img/advanced-show-diagnostic-timing-report.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Show Diagnostic Timing Report di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Utilities

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Gli strumenti utility aiutano a resettare o ripristinare la configurazione dell'addon.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Utilities</strong></p>
  <!-- Sostituire con ../../img/advanced-utilities.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Utilities di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Reset Defaults</h3>

<p>
Ripristina le impostazioni di ScanReady ai valori predefiniti.
</p>

<p>
Usalo se le impostazioni correnti producono risultati inattesi o se vuoi tornare a una configurazione pulita.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Reset Defaults</strong></p>
  <!-- Sostituire con ../../img/advanced-reset-defaults.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Reset Defaults di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Addon Preferences / Updates

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
ScanReady include preferenze aggiornamenti nel pannello Blender Add-on Preferences.
</p>

<p>
Queste opzioni aiutano a controllare nuove versioni, aprire release notes e configurare link di pubblicazione.
</p>
</div>

<div style="flex:0 0 260px; text-align:center; margin-top:-44px;">
  <p style="margin-top:0;"><strong>Addon Preferences / Updates</strong></p>
  <!-- Sostituire con ../../img/advanced-addon-preferences-updates.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Addon Preferences / Updates di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Check for Updates</h3>

<p>
Controlla se è disponibile una versione più recente di ScanReady leggendo il manifest aggiornamenti configurato.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Check for Updates</strong></p>
  <!-- Sostituire con ../../img/advanced-check-for-updates.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Check for Updates di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Open Documentation</h3>

<p>
Apre la documentazione online di ScanReady.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Open Documentation</strong></p>
  <!-- Sostituire con ../../img/advanced-open-documentation.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Open Documentation di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Release Notes</h3>

<p>
Apre la pagina changelog e release notes di ScanReady.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Release Notes</strong></p>
  <!-- Sostituire con ../../img/advanced-release-notes.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Release Notes di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Update Manifest URL</h3>

<p>
Memorizza l'URL del manifest aggiornamenti usato dal checker.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Update Manifest URL</strong></p>
  <!-- Sostituire con ../../img/advanced-update-manifest-url.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Update Manifest URL di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Release Notes URL</h3>

<p>
Memorizza l'indirizzo della pagina release notes usata dal pulsante Release Notes.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Release Notes URL</strong></p>
  <!-- Sostituire con ../../img/advanced-release-notes-url.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Release Notes URL di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

<hr>

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Publishing Links</h3>

<p>
Questi link vengono usati per configurare il manifest aggiornamenti e l'URL release notes dopo la pubblicazione.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Publishing Links</strong></p>
  <!-- Sostituire con ../../img/advanced-publishing-links.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Publishing Links di ScanReady" style="width:260px; max-width:100%;">
</div>

</div>

---

# Consiglio pratico

Per VR, videogame e workflow realtime, bilancia sempre qualità e performance.

Usa le impostazioni avanzate per trovare il compromesso giusto tra:

- pulizia mesh;
- qualità UV;
- qualità bake;
- risoluzione texture;
- dimensione file;
- uso memoria;
- performance realtime.

L'obiettivo non è preservare ogni poligono della scansione originale.

L'obiettivo è preservare l'identità visiva della scansione in un asset più leggero e più facile da usare.
