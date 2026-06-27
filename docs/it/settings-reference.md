# Riferimento impostazioni

Questa pagina riassume le impostazioni principali di ScanReady e cosa fanno.

Usala come riferimento rapido quando regoli scansioni per VR, videogame, visualizzazione realtime o ottimizzazione generale in Blender.

---

## Pannello e stato

| Voce | Descrizione | Quando usarla |
|---|---|---|
| **Mesh Stats** | Mostra facce e triangoli dell'oggetto selezionato o dell'ultima preview creata. | Usalo per controllare rapidamente quanto è pesante la mesh prima e dopo la riduzione. |
| **Refresh Stats** | Aggiorna manualmente le statistiche mesh mostrate nel pannello. | Usalo dopo aver cambiato selezione o dopo modifiche esterne alla mesh. |
| **Workflow Status** | Mostra progresso globale, step completato, messaggi di stato, mappe bake completate e tempi quando i diagnostics sono attivi. | Usalo per capire dove si trova ScanReady durante One Click Bake o durante gli step manuali. |
| **Global Progress** | Percentuale di avanzamento del workflow corrente. | Utile durante operazioni lunghe come preview, UV, cage e bake. |
| **ONE CLICK BAKE** | Avvia il workflow automatico completo: preview, UV, cage, bake e materiali finali. | Usalo quando vuoi una conversione rapida da scansione high-poly ad asset ottimizzato. |

---

## Azioni principali

| Azione | Descrizione | Quando usarla |
|---|---|---|
| **Create Lowpoly Preview** | Crea o aggiorna la mesh preview ottimizzata usando le impostazioni dello Step 1 e di Adaptive Reduce. | Usalo ogni volta che cambi densità, preset Adaptive Reduce o impostazioni mesh che influenzano la riduzione. |
| **Generate UVs** | Crea la mesh UV dalla preview e genera il layout Smart UV Project. | Usalo dopo la preview o quando cambi Smart UV Preset, Smart UV Angle o UV Padding. |
| **Auto Cage Extrusion** | Calcola una cage extrusion di partenza campionando la distanza tra mesh ottimizzata e sorgente high-poly. | Usalo prima del bake quando vuoi evitare di stimare manualmente la distanza del cage. |
| **Bake Textures** | Esegue il bake delle mappe selezionate e costruisce la mesh/materiali finali. | Usalo dopo aver generato UV e verificato cage/output. |

---

## Mesh e riduzione

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **Final Faces** | Numero target di facce per la mesh low-poly ottimizzata. | Abbassalo per asset VR/game più leggeri. Alzalo per preservare più dettaglio nella silhouette. |
| **Optimize / Reduce** | Controlla quanto la mesh viene ridotta. | Valori più bassi creano una riduzione più forte. Valori più alti mantengono più geometria. |
| **Pre-Decimate Merge** | Esegue Merge by Distance sulla mesh preview duplicata prima di Decimate. È il singolo controllo esplicito di weld in ScanReady. | Aumentalo per ridurre poligoni sovrapposti prima dell'ottimizzazione. Abbassalo se vengono colpiti dettagli sottili. |
| **Auto Clear Sharp Edges** | Rimuove marcature sharp edge non desiderate durante la preparazione. | Tienilo attivo quando la scansione mostra bordi o shading marcati in modo errato. |
| **Auto Combine Mesh Parts** | Combina parti mesh importate come oggetti separati. | Utile per scansioni composte da molte parti che devono diventare un unico asset. |
| **Auto Clean Scan Debris** | Rimuove piccoli frammenti, poligoni sospesi e vertici isolati. | Tienilo attivo per scansioni fotogrammetriche grezze. |
| **Convert Source Materials** | Converte i materiali sorgente in un setup più prevedibile per il bake. | Attivalo se i materiali importati sono complessi o poco compatibili con il trasferimento texture. |
| **Show Face Orientation** | Mostra l'overlay Face Orientation di Blender. | Usalo per controllare normali invertite prima di preview, UV o bake. |
| **Adaptive Reduce** | Usa pesi basati sulla scansione per ridurre di più le superfici piatte e proteggere dettagli importanti. | Tienilo attivo per la maggior parte delle scansioni. Disattivalo solo se vuoi un risultato di riduzione uniforme più semplice. |
| **Adaptive Reduce Preset** | Sceglie il comportamento della riduzione adattiva. | Usa Balanced per la maggior parte delle scansioni, Preserve Details per superfici complesse, Flat Surfaces per superfici semplici ampie, Hard Surface per veicoli e scansioni hard-surface. |
| **Show Adaptive Weights** | Mostra i pesi di riduzione adattiva come colori sul modello. | Usalo per vedere quali aree verranno ridotte di più prima di creare la preview low-poly finale. |
| **Adaptive Reduce Strength** | Regola quanto fortemente Adaptive Reduce favorisce la riduzione delle aree piatte. | Alzalo per semplificare di più le superfici regolari, abbassalo se vuoi un comportamento più uniforme. |
| **Adaptive Reduce Angle** | Controlla la sensibilità ai cambi di normale durante il calcolo dei pesi. | Usalo per decidere quanto un cambio di direzione deve essere considerato dettaglio. |
| **Detail Preserve** | Protegge maggiormente le zone lette come dettaglio. | Alzalo se la preview perde pieghe, bordi o dettagli importanti. |
| **Smooth Weights** | Smussa i pesi Adaptive Reduce per transizioni più omogenee. | Aumentalo quando la preview pesi appare troppo puntinata o frastagliata. |
| **Fast Adaptive Reduce** | Usa un calcolo più approssimato e veloce per scansioni dense. | Attivalo per test rapidi o scansioni molto pesanti. |
| **Protect Feature Edges** | Protegge i bordi con differenze di normale forti. | Tienilo attivo per asset hard-surface, veicoli, architettura e silhouette importanti. |
| **Feature Edge Angle** | Angolo minimo per considerare un bordo come feature edge. | Abbassalo per proteggere più bordi, alzalo per proteggere solo rotture più nette. |
| **Feature Edge Rings** | Numero di anelli vicini protetti attorno ai feature edge. | Aumentalo se i bordi netti perdono supporto durante la riduzione. |
| **Auto Fix Normals** | Ricalcola le normali della mesh high prima della creazione della preview. | Attivalo quando la scansione ha normali invertite o artefatti di shading. |
| **Recalculate Outside Normals** | Ricalcola manualmente le normali verso l'esterno. | Usalo quando la mesh appare rovesciata o ha shading rotto. |

I pesi Adaptive Reduce vengono calcolati quando premi **Create Lowpoly Preview**. Cambiare **Optimize / Reduce** o **Final Faces** dopo quel momento aggiorna la quantità di riduzione, ma cambiare preset o valori dettagliati di Adaptive Reduce richiede di creare di nuovo la preview low-poly per ricostruire i pesi.

Se sei già nello Step 2 o nello Step 3 e ti serve un modello più leggero o più dettagliato, torna allo Step 1, regola **Final Faces** o **Optimize / Reduce**, clicca **Create Lowpoly Preview**, poi rigenera UV e bake.

---

## View e preview

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **Show Wireframe** | Mostra l'overlay wireframe sull'oggetto preview. | Usalo per controllare densità topologica e qualità della riduzione. |
| **Show Checker** | Mostra una texture checker per l'ispezione. | Usalo per controllare distorsione e stretching UV. |
| **Checker Mix** | Controlla la forza dell'overlay checker. | Abbassalo quando vuoi vedere di più la texture originale. |
| **Checker UV Scale** | Cambia la dimensione dei quadrati checker. | Usa quadrati più piccoli per vedere meglio la distorsione. |
| **Use Texture View** | Porta il viewport in modalità Material Preview/Texture View durante i controlli. | Utile per vedere materiali, checker e cage con una visualizzazione più leggibile. |

**Use Texture View** è disponibile in **Advanced > Mesh Settings** perché di solito non viene regolato durante il workflow principale.

---

## Impostazioni UV

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **UV Method** | ScanReady usa Smart UV Project per generare le UV. | Questo è il metodo UV usato dal workflow dell'addon. |
| **Smart UV Preset** | Applica un angolo Smart UV consigliato. I preset includono Detailed, Balanced, Large Islands e Continuous. | Usalo come punto di partenza rapido per tipi comuni di scansione. |
| **Smart UV Angle** | Controlla quanto aggressivamente Smart UV Project divide le isole. | Valori più bassi creano più tagli. Valori più alti creano isole più grandi. |
| **UV Padding** | Aggiunge spazio tra le isole UV. | Aumentalo per ridurre texture bleeding e seam visibili. |

ScanReady usa **Smart UV Project** per generare le UV. I preset Adaptive Reduce sono separati dalle impostazioni UV e controllano la semplificazione della mesh prima di UV e bake.

Le impostazioni Smart UV vengono applicate quando le UV vengono generate. Se cambi **Smart UV Preset**, **Smart UV Angle** o **UV Padding** dopo che le UV esistono già, clicca di nuovo **Generate UVs** così la mesh ottimizzata usa il nuovo layout UV prima del bake.

---

## Impostazioni cage

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **Show Cage** | Mostra la preview del cage. | Usalo prima del bake per controllare la copertura della proiezione. |
| **Auto Cage Extrusion** | Stima automaticamente la cage extrusion. | Usalo quando vuoi un setup cage veloce. |
| **Cage Extrusion** | Distanza manuale del cage. | Aumentala se mancano dettagli. Abbassala se vengono catturate aree sbagliate. |
| **Cage Opacity** | Controlla l'opacità della preview cage. | Regolala solo per la visibilità nel viewport. Non influenza il bake. |

---

## Texture e bake

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **Texture Preset / Texture Size** | Imposta la risoluzione delle texture bake. | Alzala per asset ravvicinati. Abbassala per asset VR/game leggeri. |
| **Bake Materials** | Divide il bake in più gruppi di materiali. | Aumentalo per scansioni grandi che richiedono più dettaglio texture. Valori sopra `1` abilitano automaticamente Force CPU Baking. |
| **Texture Detail / Analyze Texture Detail** | Analisi avanzata per confronto dettaglio high-to-UV. | Usalo in Advanced prima del bake per capire se texture size e numero materiali sono bilanciati. |
| **Bake Samples** | Imposta il numero di sample Cycles per il bake. | Alzalo per bake più puliti, soprattutto AO. Abbassalo per test più rapidi. |
| **Bake Margin** | Aggiunge padding attorno alle isole UV bake. | Aumentalo per ridurre seam e texture bleeding. |
| **Bake Base Color** | Cuoce la texture colore principale. | Tienilo attivo quando vuoi preservare il colore originale della scansione. |
| **Bake Normal** | Cuoce o trasferisce una normal map. | Se il materiale high ha una normal texture collegata, ScanReady la trasferisce. Altrimenti esegue un bake normal geometrico high-to-low. |
| **Bake Roughness** | Trasferisce roughness dal materiale high quando è collegata una roughness texture. | Attivalo quando l'asset finale deve mantenere variazione roughness dal materiale originale. |
| **Bake Occlusion** | Cuoce una mappa Ambient Occlusion. | Attivalo per aggiungere profondità e ombre di contatto. |
| **Normal Strength** | Controllo avanzato della forza del nodo Normal Map. | Regolalo in Advanced > Bake Settings se il dettaglio normal appare troppo debole o troppo forte. |

---

## Ambient Occlusion

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **AO Source** | Sceglie come viene cotta AO. | Usa high-to-low per trasferire dettaglio dalla scansione, oppure low-only per AO più semplice. |
| **AO Auto Distance** | Calcola automaticamente la distanza AO dalla dimensione del modello. | Lascialo attivo per la maggior parte degli asset. |
| **AO Distance** | Distanza manuale dei raggi AO. | Regolalo quando la distanza automatica produce AO troppo forte o troppo debole. |
| **AO Samples** | Controlla il numero di sample per il bake AO. | Alzalo per AO più pulita. Abbassalo per bake più rapidi. |
| **AO Mix** | Controlla quanto la AO bake scurisce il materiale Base Color finale. | Il default e `1.0`. Abbassalo se il materiale finale sembra troppo scuro o contrastato. |

---

## Impostazioni output

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **Save Images** | Salva le texture bake su disco. | Attivalo quando esporti verso game engine, archivi o tool esterni. |
| **Open Folder After Bake** | Apre automaticamente la cartella del bake quando il salvataggio texture è completato. | Utile durante test e produzione, soprattutto quando vuoi controllare subito i file generati. |
| **Image Format** | Sceglie JPG, PNG o TIFF. | Usa JPG per color map compatte, PNG per output lossless, TIFF per alta precisione. |
| **JPG Quality** | Controlla la qualità di compressione JPG. | Alzalo per migliore qualità. Abbassalo per file più piccoli. |
| **TIFF 16-bit** | Salva texture TIFF con precisione più alta. | Usalo per asset ravvicinati, workflow archivio o mappe dettagliate. |
| **Output Folder** | Cartella dove vengono salvate le texture bake. | Impostala prima del bake se vuoi i file in una cartella specifica del progetto. |
| **Bake Folder** | Mostra la cartella usata dall'ultimo bake e fornisce un pulsante per aprirla. | Usalo dopo il bake per controllare o copiare rapidamente i file texture salvati. |

---

## Sicurezza memoria

| Impostazione | Descrizione | Quando regolarla |
|---|---|---|
| **Safe Memory Bake** | Usa un workflow bake più sicuro per scene pesanti. | Tienilo attivo per scansioni grandi o alte risoluzioni texture. |
| **Force CPU Baking** | Forza il bake su CPU invece che GPU. | Disattivo di default con un materiale. Abilitato automaticamente quando Bake Materials è `2` o superiore, e disattivabile manualmente. |

---

## Preset

| Controllo | Descrizione | Quando usarlo |
|---|---|---|
| **Preset Name** | Nome usato quando salvi le impostazioni correnti. | Usa un nome chiaro per un workflow o tipo di asset. |
| **Save Preset** | Salva le impostazioni correnti. | Usalo prima di processare scansioni simili. |
| **Preset Selector** | Menu con i preset salvati disponibili. | Usalo per scegliere quale preset ricaricare o eliminare. |
| **Reload Preset** | Ricarica il preset selezionato. | Usalo per ripetere un setup noto o tornare rapidamente a un preset salvato. |
| **Delete Preset** | Elimina il preset selezionato. | Usalo per rimuovere setup vecchi o inutilizzati. |

---

## Diagnostics

| Controllo | Descrizione | Quando usarlo |
|---|---|---|
| **Show Diagnostic Timing Report** | Mostra un report dettagliato dei tempi dopo One Click Bake, con sotto-report per Adaptive/Decimate e Bake/Finalize. | Tienilo disattivato per video e uso normale. Abilitalo quando vuoi analizzare performance o confrontare test. |

---

## Aggiornamenti

| Controllo | Descrizione | Quando usarlo |
|---|---|---|
| **Check for Updates** | Legge il manifest aggiornamenti configurato e controlla se è disponibile una nuova versione di ScanReady. | Usalo dalle preferenze Blender quando vuoi verificare la versione installata. |
| **Open Documentation** | Apre la documentazione online di ScanReady. | Usalo quando vuoi consultare guida rapida, workflow, FAQ o troubleshooting. |
| **Release Notes** | Apre il changelog e la pagina release notes di ScanReady. | Usalo per vedere cosa è cambiato prima di aggiornare. |
| **Update Manifest URL** | Memorizza l'URL JSON usato per i controlli aggiornamento. | Configuralo dopo la pubblicazione se cambia la sorgente aggiornamenti. |
| **Release Notes URL** | Memorizza l'indirizzo della pagina release notes. | Serve a collegare il pulsante Release Notes alla pagina corretta. |
| **Publishing Links** | Raccoglie i collegamenti pubblici utili per documentazione, release notes e distribuzione. | Utile quando prepari o controlli una release pubblicata. |

---

## Punti di partenza consigliati

### Asset VR leggero

| Impostazione | Direzione consigliata |
|---|---|
| **Final Faces** | Più basso |
| **Texture Size** | 1024 o 2048 |
| **Bake Normal** | Attivo se il dettaglio superficie è importante |
| **Bake Occlusion** | Opzionale |
| **Safe Memory Bake** | Attivo |
| **Bake Materials** | Mantienilo basso |

### Game prop

| Impostazione | Direzione consigliata |
|---|---|
| **Final Faces** | Medio |
| **Texture Size** | 2048 |
| **Bake Base Color** | Attivo |
| **Bake Normal** | Attivo |
| **Bake Occlusion** | Opzionale |
| **Image Format** | PNG o JPG in base alla pipeline |

### Asset da presentazione ravvicinata

| Impostazione | Direzione consigliata |
|---|---|
| **Final Faces** | Più alto |
| **Texture Size** | 4096 o superiore |
| **Bake Normal** | Attivo |
| **Bake Occlusion** | Attivo |
| **Bake Samples** | Più alto |
| **Image Format** | PNG o TIFF |

---

## Regola generale

Per il realtime, non conservare il dettaglio solo come geometria.

Usa la geometria per la forma principale e usa texture bake per il dettaglio visivo.

Questo equilibrio rende gli asset scansionati più facili da usare in VR, videogame, viewer realtime e scene interattive.
