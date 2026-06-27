# Changelog

Tutte le modifiche importanti di ScanReady saranno documentate in questo file.

Usa questa pagina come sorgente pubblica delle release notes per Superhive, Blender Extensions e i link di aggiornamento dell'addon.

## 1.0.0 - Release iniziale

### Aggiunto

- Supporto pacchetto Blender Extension.
- Workflow One Click Bake per creare asset game-ready da scansioni.
- Workflow Step 1 Preview / Reduce.
- Adaptive Reduce per ottimizzazione mesh consapevole della scansione.
- Sezioni Home e Step 1 della documentazione che spiegano perché ScanReady Adaptive Reduce differisce dal Decimate standard di Blender, con placeholder per immagini comparative.
- Preset Adaptive Reduce: Balanced, Preserve Details, Flat Surfaces e Hard Surface.
- Preset Hard Surface Adaptive Reduce per veicoli e scansioni hard-surface, impostato come passaggio approssimato più veloce che protegge solo rotture di normale più forti.
- Visualizzazione Show Adaptive Weights.
- Auto combine mesh parts per scansioni importate con gerarchia.
- Opzione Auto clean scan debris.
- Workflow Smart UV Project.
- Workflow UV / Cage.
- Bake di Base Color, Normal, Roughness e Ambient Occlusion.
- Controllo AO Mix in Advanced > Occlusion Settings per regolare quanto l'Ambient Occlusion bake influenza il materiale finale.
- Analisi Texture Detail per stimare necessità di texture/materiali.
- Setup mesh finale con modificatori Edge Split e Weighted Normal.
- Opzioni Safe Memory Bake e Force CPU Baking.
- Collegamento Bake Folder nello Step 3 per aprire l'ultima cartella texture salvata.
- Link documentazione e release notes nelle preferenze addon.
- Messaggio di notifica aggiornamento per marketplace e Blender Extensions.
- Guida FAQ per rifinire un risultato One Click Bake quando il modello finale è ancora troppo pesante.
- Guida workflow attraverso Step 1, Step 2, Step 3, Quick Start, One Click e FAQ che spiega che gli utenti possono tornare allo Step 1, regolare la riduzione, ricreare la preview low-poly, poi rigenerare UV e bake.

### Modificato

- Il flusso aggiornamenti ora indirizza gli utenti verso Blender Extensions o marketplace invece di installare aggiornamenti direttamente dentro l'addon.
- Le impostazioni Adaptive Reduce sono state spostate in Advanced.
- Show Adaptive Reduce è stato rinominato Show Adaptive Weights.
- Il comportamento predefinito Adaptive Reduce ora usa il preset Balanced.
- Il valore predefinito Detail Preserve è stato cambiato per proteggere meglio le aree dettagliate delle scansioni.
- Rimossi Auto Weld Distance e Weld Distance; Pre-Decimate Merge è ora il singolo controllo esplicito di weld.
- Rimosso il modificatore Weld live dallo stack preview; il vertex welding ora viene gestito dal Pre-Decimate Merge applicato prima di Decimate.
- Normal Strength spostato in Advanced > Bake Settings.
- Texture Detail / Analyze Texture Detail spostato in Advanced.
- Manifest extension ripulito per la validazione Blender Extension.

### Corretto

- Corretti errori di validazione del manifest Blender Extension causati da punteggiatura alla fine delle stringhe manifest.
- Migliorato il calcolo dei pesi Adaptive Reduce, così le aree piatte ampie vengono rilevate più chiaramente.
- Migliorata la leggibilità della preview colori Adaptive Reduce.
- Ridotto il ricalcolo continuo delle mesh stats, così l'interfaccia Blender resta più reattiva.

### Problemi noti

- Scansioni molto pesanti possono richiedere ancora tempo per analisi, riduzione, UV o bake.
- La qualità bake dipende da qualità della scansione, layout UV, impostazioni cage/extrusion e risoluzione texture.
- Adaptive Reduce è un aiuto per distribuire meglio i poligoni, non un sostituto perfetto della retopology.
