# Risoluzione problemi

Questa pagina copre problemi comuni del workflow ScanReady e offre soluzioni per bake, UV, ottimizzazione, uso memoria e preparazione realtime.

L'elaborazione delle scansioni puo essere impegnativa perche scansioni high-poly, texture baking, generazione UV e memoria dipendono dal modello sorgente e dall'hardware.

Per supporto, bug report o domande sul workflow, contatta:

<a href="mailto:support.marioschiano3d@gmail.com"><strong>support.marioschiano3d@gmail.com</strong></a>

---

## Il pannello ScanReady non appare

Controlla:

- l'addon e abilitato in **Edit > Preferences > Add-ons**;
- sei nel **3D Viewport**;
- hai premuto **N** per aprire la Sidebar;
- esiste la scheda **Scan Ready**;
- in alcuni casi serve riavviare Blender dopo aver abilitato l'addon.

---

## One Click Bake non parte

Assicurati che:

- sia selezionato un oggetto mesh;
- l'oggetto selezionato sia la scansione high-poly da processare;
- Blender sia in Object Mode;
- l'oggetto sia visibile e non nascosto;
- la scena non stia gia eseguendo un'altra operazione modal.

Se serve, salva il file, riavvia Blender e riprova.

---

## La preview mesh e troppo pesante

Se la preview ottimizzata e ancora troppo densa:

- abbassa **Optimize / Reduce**;
- abbassa **Final Faces**;
- aumenta la pulizia solo con cautela;
- crea di nuovo la preview lowpoly.

**Optimize / Reduce** e **Final Faces** sono collegati: entrambi controllano quanto sara leggera la preview lowpoly.

Per asset VR e videogame, la mesh deve restare abbastanza leggera da essere gestita bene nel viewport, esportata senza problemi e usata in realtime.

---

## La preview mesh ha perso troppo dettaglio

Se la preview ottimizzata sembra troppo semplificata:

- aumenta **Optimize / Reduce**;
- aumenta **Final Faces**;
- evita riduzioni troppo aggressive su oggetti molto sottili o delicati;
- crea di nuovo la preview.

**Optimize / Reduce** e **Final Faces** sono collegati: entrambi controllano quanto dettaglio geometrico viene mantenuto nella preview lowpoly.

Per silhouette importanti, mantieni abbastanza geometria per preservare la forma.

---

## Le UV sembrano allungate

Se il pattern checker mostra aree molto allungate:

- prova un metodo UV diverso;
- abbassa o alza **Smart UV Angle**;
- aumenta la separazione tra isole con **UV Padding**;
- usa un preset UV piu dettagliato;
- genera di nuovo le UV.

UV pulite sono importanti per texture bake buone.

---

## Il bake perde dettagli

Se parti del dettaglio della scansione mancano nella texture bake:

- abilita **Show Cage** e controlla il cage;
- aumenta leggermente **Cage Extrusion** oppure usa **Auto Cage Extrusion**;
- verifica che il cage copra completamente la sorgente high-poly;
- aumenta **Texture Size** se il bake ha risoluzione troppo bassa;
- assicurati che l'oggetto high-poly originale sia ancora disponibile.

Usa il valore di cage piu piccolo che cattura i dettagli in modo pulito.

---

## Perche la texture bake sembra di bassa qualita?

La qualita bake dipende da:

- risoluzione texture;
- densita poligoni;
- uso dello spazio UV;
- numero di materiali.

### Aumenta la risoluzione texture

Prova prima ad aumentare la risoluzione texture.

Esempio:

- 1024 -> dettaglio basso
- 2048 -> qualita standard
- 4096 -> alta qualita
- 8192 -> dettaglio molto alto

Risoluzioni piu alte aumentano l'uso memoria.

### Aumenta la densita dei poligoni

Se la mesh ottimizzata e troppo aggressiva, dettagli importanti possono essere persi prima del bake.

Prova:

- aumentare **Final Faces**;
- usare un valore **Optimize / Reduce** meno aggressivo.

### Usa piu materiali

Se aumentare la risoluzione texture non basta, l'asset puo richiedere piu materiali.

Ogni materiale riceve il proprio spazio texture, permettendo una conservazione del dettaglio molto piu alta sul modello.

Aumentare solo la densita dei poligoni non e sempre la soluzione migliore.

Mesh molto dense possono diventare piu pesanti da elaborare, piu lente da cuocere e piu difficili da usare in applicazioni realtime.

Per questo ScanReady puo consigliare un numero appropriato di materiali bake in base a complessita e dimensione della scansione.

Esempio:

- 1 materiale -> dettaglio texture piu basso
- 2 materiali -> qualita texture migliorata
- 4 materiali -> dettaglio texture molto piu alto

Usare piu materiali e spesso una soluzione migliore rispetto ad aumentare semplicemente la densita dei poligoni.

Questo e particolarmente utile per:

- scansioni grandi;
- asset ambiente;
- oggetti museali;
- asset fotogrammetrici complessi;
- dettagli fini della superficie.

---

## Il bake cattura aree sbagliate

Se il bake include dettagli dalla parte sbagliata del modello:

- riduci **Cage Extrusion**;
- controlla la preview cage;
- assicurati che gli oggetti non si sovrappongano;
- nascondi o sposta oggetti non correlati se serve;
- esegui di nuovo il bake.

Un cage troppo grande puo proiettare superfici vicine indesiderate.

---

## Le texture non vengono salvate

Controlla:

- **Save Images** e attivo;
- **Output Folder** e valida;
- il file Blender e stato salvato se usi un percorso relativo come `//bake/`;
- hai permessi di scrittura nella cartella selezionata;
- il bake e stato completato con successo.

I percorsi relativi vengono salvati accanto al file `.blend` corrente.

Dopo un bake riuscito, usa **Bake Folder** nello Step 3 per aprire l'ultima cartella texture. Se il pulsante non e ancora visibile, esegui prima un bake con **Save Images** attivo.

---

## Perche il bake e molto lento?

Il bake puo essere lento con scansioni grandi o texture ad alta risoluzione.

Per velocizzarlo:

- abbassa **Texture Size**;
- abbassa **Bake Samples**;
- riduci il numero di materiali bake se possibile;
- disattiva le mappe che non ti servono;
- usa una mesh finale piu piccola quando appropriato.

Normal map e AO ad alta risoluzione possono aumentare il tempo di bake.

---

## Blender finisce la memoria

Le scansioni grandi possono usare molta memoria durante il bake.

Prova:

- abilita **Safe Memory Bake**;
- abilita **Force CPU Baking** se la memoria GPU e limitata;
- abbassa **Texture Size**;
- abbassa il numero di materiali bake;
- chiudi altre applicazioni pesanti;
- salva e riavvia Blender prima del bake.

Force CPU Baking di solito e piu lento, ma puo essere piu sicuro su sistemi con poca VRAM.

ScanReady abilita automaticamente **Force CPU Baking** quando il numero di materiali bake e impostato a `2` o piu.

Per bake a singolo materiale, il bake GPU puo comunque essere usato quando disponibile.

---

## La Normal Map sembra troppo forte o troppo debole

Regola **Normal Strength**.

Cambia la forza del nodo Normal Map nel materiale finale.

Influenza l'aspetto del materiale, non l'immagine normal bake.

Se il materiale high-poly originale ha una normal texture collegata, ScanReady trasferisce quella normal map sul nuovo layout UV.

Se non e collegata nessuna normal texture, ScanReady genera una normal map nuova proiettando il dettaglio della geometria high-poly sulla mesh lowpoly.

---

## Mancano le informazioni Roughness

ScanReady puo trasferire roughness solo quando il materiale high-poly originale contiene gia una roughness texture o un input roughness utilizzabile.

Se nel materiale originale non esistono informazioni roughness, non puo essere generato automaticamente un trasferimento roughness.

Controlla il node tree del materiale originale e verifica che le informazioni roughness siano disponibili prima del bake.

---

## Ambient Occlusion e troppo scura

Prova:

- abbassare la forza AO nel materiale finale;
- ridurre **AO Distance** se la distanza automatica e disattivata;
- usare impostazioni AO piu controllate;
- verificare se la sorgente AO e adatta all'asset.

AO deve aggiungere profondita, non nascondere i dettagli della scansione.

---

## Perche il bake contiene aree nere o mancanti?

Se la texture bake contiene aree nere, dettagli mancanti o proiezioni errate, di solito la cage extrusion e troppo piccola.

In questo caso alcune parti della scansione high-poly non vengono raggiunte correttamente durante il bake.

Aree nere possono comparire anche quando parti della mesh lowpoly ottimizzata si trovano davanti o dietro la sorgente high-poly, quindi i raggi di bake non colpiscono la superficie prevista.

Per correggere:

- abilita **Show Cage**;
- aumenta leggermente **Cage Extrusion** oppure usa **Auto Cage Extrusion**;
- controlla il cage attorno al modello prima del bake;
- verifica che il cage copra completamente la sorgente high-poly.

Il cage deve circondare completamente la superficie high-poly.

In ScanReady, la preview del cage diventa verde quando il cage e abbastanza grande da coprire correttamente la superficie della scansione.

Se alcune aree mancano ancora, aumenta leggermente l'extrusion e controlla di nuovo il cage.

Quando il cage sembra corretto, esegui di nuovo il bake per verificare se le aree mancanti o nere sono state corrette.

Usa il valore piu piccolo che copre completamente la scansione senza catturare superfici vicine indesiderate.

---

## Quale preset Adaptive Reduce devo usare?

Adaptive Reduce cambia come ScanReady distribuisce la riduzione mesh sulla scansione prima di UV e bake.

| Preset | Ideale per | Risultato |
|---|---|---|
| **Balanced** | La maggior parte delle scansioni | Buon comportamento generale. Usalo per primo. |
| **Preserve Details** | Scansioni complesse con forme scultoree, pieghe, incisioni, danni o piccoli dettagli | Protegge piu fortemente le aree di dettaglio importanti. |
| **Flat Surfaces** | Oggetti con ampie superfici semplici, pannelli, muri, pavimenti o aree architettoniche piatte | Riduce in modo piu aggressivo le aree semplici per risparmiare poligoni. |
| **Hard Surface** | Veicoli, props, macchinari e scansioni hard-surface | Usa un passaggio approssimato piu veloce e protegge solo rotture di normale piu forti. |

Se la preview ottimizzata perde dettagli importanti, prova **Preserve Details** e crea di nuovo la preview.

Se la preview mantiene troppa geometria su aree semplici, prova **Flat Surfaces** e crea di nuovo la preview.

Per veicoli o scansioni hard-surface, prova **Hard Surface** e controlla silhouette e principali interruzioni dei pannelli.

---

## Ho cambiato troppi valori e non so come tornare indietro

Se hai modificato molte impostazioni e il risultato e diventato difficile da controllare, usa **Reset Defaults**.

Questo e utile quando hai cambiato diversi valori in Advanced, come impostazioni di Occlusion, Bake, UV, Adaptive Reduce o memoria, e non sai piu quale parametro sta causando il problema.

**Reset Defaults** riporta ScanReady a una base pulita.

Dopo il reset:

1. Riparti da **Balanced** come preset Adaptive Reduce.
2. Crea di nuovo la preview lowpoly.
3. Genera di nuovo le UV.
4. Controlla il cage.
5. Esegui prima un bake semplice, ad esempio solo Base Color.

Quando il workflow base funziona, riattiva gli altri controlli uno alla volta.

---

## Primo intervento consigliato

Se il risultato non e buono, usa questo ordine:

1. Controlla la preview lowpoly
2. Controlla le UV con la vista checker
3. Controlla la preview cage
4. Cuoci prima solo Base Color
5. Aggiungi Normal, Roughness e AO dopo che Base Color funziona
6. Aumenta la risoluzione texture solo quando il workflow e corretto

Questo rende piu facile isolare i problemi.
