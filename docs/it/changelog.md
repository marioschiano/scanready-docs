# Changelog

Questa pagina raccoglie le note di rilascio di ScanReady.

Consulta le novità e i problemi noti prima di aggiornare l’addon.

## 1.0.0 - Release iniziale

### Aggiunto

- Supporto pacchetto Blender Extension.
- Workflow One Click Bake per creare asset game-ready da scansioni.
- Workflow Step 1 Preview / Reduce.
- Adaptive Reduce per ottimizzazione mesh consapevole della scansione.
- Selettore Adaptive Method con Best Quality e modalità Legacy per compatibilità.
- Best Quality combina rilevamento delle grandi aree planari e protezione di curvature persistenti, rilievi e decorazioni.
- Preset Adaptive Reduce: Balanced, Preserve Details e Flat Surfaces.
- Controlli avanzati Best Quality per sensibilità alla complessità, contrasto piatto/dettaglio, espansione del dettaglio, rifiuto del rumore, scala di analisi e influenza Decimate.
- Visualizzazione Show Adaptive Weights.
- Auto combine mesh parts per scansioni importate con gerarchia.
- Opzione Auto clean scan debris.
- Workflow Smart UV Project.
- Workflow UV / Cage.
- Bake di Base Color, Normal Map, Roughness Map e Occlusion Map.
- Controllo AO Mix in Advanced > Bake Settings > Occlusion Settings per regolare quanto l'Ambient Occlusion bake influenza il materiale finale.
- Analisi Texture Detail per stimare necessità di texture/materiali.
- Setup mesh finale con modificatori Edge Split e Weighted Normal.
- Opzioni Safe Memory Bake e Force CPU Baking.
- Collegamento Bake Folder nello Step 3 per aprire l'ultima cartella texture salvata.
- Link documentazione e release notes nelle preferenze addon.
- Messaggio di notifica aggiornamento per marketplace e Blender Extensions.

### Modificato

- Il flusso aggiornamenti ora indirizza gli utenti verso Blender Extensions o marketplace invece di installare aggiornamenti direttamente dentro l'addon.
- Le impostazioni Adaptive Reduce sono state spostate in Advanced.
- Show Adaptive Reduce è stato rinominato Show Adaptive Weights.
- Il comportamento predefinito Adaptive Reduce ora usa il preset Balanced.
- Balanced usa i valori Best Quality verificati e Adaptive Decimate Factor 2.
- Show Adaptive Weights nasconde temporaneamente il wireframe e ripristina la preferenza precedente quando viene disattivato.
- Adaptive Strength viene mostrato soltanto con Legacy; Best Quality usa Adaptive Decimate Factor.
- Il valore predefinito Detail Preserve è stato cambiato per proteggere meglio le aree dettagliate delle scansioni.
- Rimossi Auto Weld Distance e Weld Distance; Pre-Decimate Merge è ora il singolo controllo esplicito di weld.
- Rimosso il modificatore Weld live dallo stack preview; il vertex welding ora viene gestito dal Pre-Decimate Merge applicato prima di Decimate.
- Normal Strength spostato in Advanced > Bake Settings.
- Texture Detail / Analyze Texture Detail spostato in Advanced.
- Manifest extension ripulito per la validazione Blender Extension.

### Corretto

- Corretti errori di validazione del manifest Blender Extension causati da punteggiatura alla fine delle stringhe manifest.
- Migliorato il calcolo dei pesi Adaptive Reduce, così le aree piatte ampie vengono rilevate più chiaramente e le decorazioni coerenti restano protette.
- Migliorata la leggibilità della preview colori Adaptive Reduce.
- Ridotto il ricalcolo continuo delle mesh stats, così l'interfaccia Blender resta più reattiva.

### Problemi noti

- Scansioni molto pesanti possono richiedere ancora tempo per analisi, riduzione, UV o bake.
- La qualità bake dipende da qualità della scansione, layout UV, impostazioni cage/extrusion e risoluzione texture.
- Adaptive Reduce è un aiuto per distribuire meglio i poligoni, non un sostituto perfetto della retopology.
