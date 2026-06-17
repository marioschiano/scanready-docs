# Impostazioni avanzate

Le impostazioni avanzate danno controllo preciso su pulizia mesh, generazione UV, qualita bake, output immagini, preset, utility e sicurezza memoria.

Non serve cambiare ogni impostazione per usare ScanReady.

Per la maggior parte delle scansioni, parti dai valori predefiniti. Regola le impostazioni avanzate solo quando hai bisogno di piu controllo su performance, qualita o accuratezza del bake.

<!-- Sostituire il placeholder con ../../img/advanced-overview.png -->
<p align="center">
  <img src="../../img/placeholder-image.svg" alt="Placeholder panoramica impostazioni Advanced di ScanReady" style="max-width:820px;width:100%;">
</p>

# Mesh Settings

Queste impostazioni controllano pulizia scansione e preparazione mesh prima di generare la preview lowpoly.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Pre-Decimate Merge</h3>

<p>
Esegue una pulizia Merge by Distance sulla mesh preview duplicata prima che venga aggiunto il modificatore Decimate.
</p>

<p>
E il singolo controllo esplicito di weld in ScanReady 1.0. Puo aiutare a ridurre poligoni sovrapposti della scansione prima dell'ottimizzazione. Se vengono colpiti dettagli sottili, abbassa il valore e crea di nuovo la preview lowpoly.
</p>

<hr>

<h3>Auto Fix Normals</h3>

<p>
Ricalcola automaticamente le normali della mesh high-poly prima di creare la preview lowpoly.
</p>

<p>
Attivalo quando la scansione ha normali invertite, shading rotto o artefatti di bake causati da direzioni normali errate.
</p>

<hr>

<h3>Use Texture View</h3>

<p>
Mostra il modello in una visualizzazione piatta orientata alla texture, senza illuminazione di scena.
</p>

<p>
E utile per ispezionare piu chiaramente risultati texture bake o preview.
</p>

<hr>

<h3>Recalculate Outside Normals</h3>

<p>
Esegue manualmente il ricalcolo delle normali sulla mesh high-poly selezionata.
</p>

<p>
Usalo quando la scansione appare rovesciata o ha shading incoerente.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-mesh-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Mesh Settings di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Adaptive Reduce

Adaptive Reduce controlla come ScanReady distribuisce la riduzione sulla scansione selezionata.

E attivo di default ed e progettato per proteggere il dettaglio visivamente importante, permettendo alle superfici piatte di essere semplificate di piu.

I pesi Adaptive Reduce vengono calcolati quando clicchi **Create Lowpoly Preview**. Cambiare **Optimize / Reduce** o **Final Faces** dopo quel momento aggiorna la quantita di riduzione, ma non ricalcola i pesi adattivi. Per applicare un preset Adaptive Reduce diverso o valori adattivi dettagliati, crea di nuovo la preview lowpoly.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Adaptive Reduce Preset</h3>

<p>
Scegli il preset piu adatto alla scansione e all'asset target.
</p>

<ul>
<li><strong>Balanced</strong> e il preset predefinito per la maggior parte delle scansioni.</li>
<li><strong>Preserve Details</strong> protegge piu fortemente regioni complesse o importanti della superficie.</li>
<li><strong>Flat Surfaces</strong> riduce in modo piu aggressivo le aree ampie e semplici.</li>
<li><strong>Hard Surface</strong> e un preset approssimato piu veloce per veicoli e scansioni hard-surface; protegge solo rotture di normale piu forti.</li>
</ul>

<hr>

<h3>Show Adaptive Weights</h3>

<p>
Mostra una preview a colori di come ScanReady distribuira la riduzione sulla scansione.
</p>

<p>
Le aree rosse rappresentano superfici piu piatte che possono essere ridotte di piu. Le aree blu e verdi rappresentano regioni protette per il dettaglio.
</p>

<p>
Usa questa preview quando una scansione ha superfici miste, come pannelli architettonici piatti insieme a dettagli scultorei o danneggiati.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-adaptive-reduce.png -->
  <img src="../../img/placeholder-image.svg" alt="Impostazioni avanzate Adaptive Reduce di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# UV Settings

Queste impostazioni controllano come Smart UV Project apre la mesh ottimizzata.

Le impostazioni Smart UV vengono applicate quando ScanReady genera le UV. Se cambi Smart UV Preset, Smart UV Angle, UV Padding o Auto Pack UV dopo che le UV esistono gia, clicca di nuovo **Generate UVs**, oppure esegui **One Click Bake** dall'inizio cosi il suo step di generazione UV usa le nuove impostazioni. **Bake Textures** usa il layout UV gia esistente.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Smart UV Angle</h3>

<p>
Controlla quanto aggressivamente Smart UV Project divide la mesh in isole UV.
</p>

<p>
Valori piu bassi creano piu tagli e piu isole UV.
</p>

<p>
Valori piu alti creano isole piu grandi.
</p>

<p>
Puoi regolare manualmente questo valore per un controllo piu preciso. I preset Adaptive Reduce sono separati dalla generazione UV: Adaptive Reduce controlla la semplificazione della mesh, mentre Smart UV Project controlla l'unwrap usato per il bake.
</p>

<p>
ScanReady 1.0 usa Smart UV Project come metodo UV per il workflow corrente.
</p>

<hr>

<h3>UV Padding</h3>

<p>
Imposta lo spazio tra le isole UV.
</p>

<p>
Aumenta il padding per ridurre texture bleeding, soprattutto a risoluzioni texture piu basse.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-uv-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot UV Settings di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Bake Settings

Queste impostazioni controllano qualita bake, padding texture, qualita formato immagine, analisi Texture Detail, opzioni Occlusion e sicurezza memoria.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Bake Samples</h3>

<p>
Imposta il numero di sample Cycles usati per il bake.
</p>

<p>
Valori piu alti possono ridurre il rumore, soprattutto per Ambient Occlusion, ma aumentano anche il tempo di bake.
</p>

<hr>

<h3>Bake Margin</h3>

<p>
Aggiunge padding in pixel attorno alle isole UV bake.
</p>

<p>
Aiuta a ridurre seam visibili e texture bleeding.
</p>

<hr>

<h3>Texture Detail</h3>

<p>
Analizza la sorgente high-poly e la mesh UV ottimizzata per stimare se texture size e numero di materiali bake correnti possono preservare abbastanza dettaglio della scansione.
</p>

<p>
Usa <strong>Analyze Texture Detail</strong> dopo aver generato le UV, prima del bake, quando vuoi aiuto per decidere se aumentare la risoluzione texture, aumentare i materiali bake o migliorare il packing UV.
</p>

<hr>

<h3>Normal Strength</h3>

<p>
Appare quando <strong>Bake Normal</strong> e abilitato.
</p>

<p>
Controlla la forza del nodo Normal Map nel materiale finale. Cambia solo l'aspetto del materiale; non cambia la texture normal bake.
</p>

<hr>

<h3>JPG Quality</h3>

<p>
Controlla la qualita di compressione JPG quando il formato immagine selezionato e JPG.
</p>

<p>
Valori piu alti preservano piu dettaglio immagine ma creano file piu grandi.
</p>

<hr>

<h3>TIFF 16-bit</h3>

<p>
Abilita output TIFF a precisione piu alta quando il formato selezionato e TIFF.
</p>

<p>
Puo essere utile per asset dettagliati, workflow archivio o output texture tecnico.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-bake-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Bake Settings di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Occlusion Settings

Queste opzioni appaiono quando **Bake Occlusion** e abilitato.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>AO Source</h3>

<p>
Controlla se Ambient Occlusion viene cotta dalla sorgente high-poly al target lowpoly, oppure calcolata solo dalla mesh lowpoly.
</p>

<hr>

<h3>AO Auto Distance</h3>

<p>
Calcola automaticamente la distanza AO in base alla dimensione del modello.
</p>

<hr>

<h3>AO Distance</h3>

<p>
Distanza manuale dei raggi AO quando la distanza automatica e disattivata.
</p>

<hr>

<h3>AO Samples</h3>

<p>
Controlla la qualita del bake Ambient Occlusion.
</p>

<p>
Valori piu alti producono AO piu pulita ma aumentano il tempo di bake.
</p>

<hr>

<h3>AO Mix</h3>

<p>
Controlla quanto la texture Ambient Occlusion bake scurisce il materiale Base Color finale.
</p>

<p>
Il valore predefinito e <strong>1.0</strong>, che usa tutta la texture AO bake nel materiale finale. Valori piu bassi rendono l'effetto AO piu sottile.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-occlusion-settings.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Occlusion Settings di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Memory Safety

Queste opzioni aiutano a ridurre problemi di memoria durante operazioni di bake pesanti.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Safe Memory Bake</h3>

<p>
Usa un workflow bake piu sicuro pensato per ridurre la pressione sulla memoria in scansioni grandi e scene Blender pesanti.
</p>

<p>
Lascialo attivo quando lavori con asset fotogrammetrici densi o alte risoluzioni texture.
</p>

<hr>

<h3>Force CPU Baking</h3>

<p>
Forza il bake sulla CPU per evitare limiti di memoria GPU.
</p>

<p>
Di solito e piu lento, ma puo essere piu sicuro su sistemi con poca VRAM.
</p>

<p>
ScanReady 1.0 puo abilitarlo automaticamente quando viene usato il bake multi-materiale.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-memory-safety.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Memory Safety di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Preset

ScanReady 1.0 puo salvare, ricaricare ed eliminare preset con nome.

I preset salvano le impostazioni correnti del workflow cosi puoi riutilizzarle in seguito.

Usa i preset quando lavori su piu scansioni con requisiti simili, come:

- asset VR;
- game prop;
- oggetti museali;
- impostazioni bake ripetute;
- workflow standard di studio.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Preset Name</h3>

<p>
Definisce il nome del preset da salvare.
</p>

<hr>

<h3>Save Preset</h3>

<p>
Salva le impostazioni correnti di ScanReady come preset riutilizzabile.
</p>

<hr>

<h3>Preset Selector</h3>

<p>
Permette di scegliere un preset esistente.
</p>

<hr>

<h3>Reload Preset</h3>

<p>
Carica il preset selezionato.
</p>

<hr>

<h3>Delete Preset</h3>

<p>
Elimina il preset selezionato.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-presets.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Presets di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Utilities

Gli strumenti utility aiutano a resettare o ripristinare la configurazione dell'addon.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Reset Defaults</h3>

<p>
Ripristina le impostazioni di ScanReady ai valori predefiniti.
</p>

<p>
Usalo se le impostazioni correnti producono risultati inattesi o se vuoi tornare a una configurazione pulita.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-utilities.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Utilities di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Addon Preferences / Updates

ScanReady include preferenze aggiornamenti nel pannello Blender Add-on Preferences.

Queste opzioni aiutano a controllare nuove versioni, aprire release notes e configurare link di pubblicazione.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Check for Updates</h3>

<p>
Controlla se e disponibile una versione piu recente di ScanReady leggendo il manifest aggiornamenti configurato.
</p>

<hr>

<h3>Release Notes</h3>

<p>
Apre la pagina changelog e release notes di ScanReady.
</p>

<hr>

<h3>Update Source</h3>

<p>
Memorizza l'URL del manifest aggiornamenti usato dal checker.
</p>

<hr>

<h3>Publishing Links</h3>

<p>
Questi link vengono usati per configurare il manifest aggiornamenti e l'URL release notes dopo la pubblicazione.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <!-- Sostituire il placeholder con ../../img/advanced-addon-preferences.png -->
  <img src="../../img/placeholder-image.svg" alt="Placeholder screenshot Addon Preferences di ScanReady" style="width:340px; max-width:100%;">
</div>

</div>

---

# Consiglio pratico

Per VR, videogame e workflow realtime, bilancia sempre qualita e performance.

Usa le impostazioni avanzate per trovare il compromesso giusto tra:

- pulizia mesh;
- qualita UV;
- qualita bake;
- risoluzione texture;
- dimensione file;
- uso memoria;
- performance realtime.

L'obiettivo non e preservare ogni poligono della scansione originale.

L'obiettivo e preservare l'identita visiva della scansione in un asset piu leggero e piu facile da usare.
