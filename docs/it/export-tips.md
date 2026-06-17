# Consigli export

Dopo aver usato ScanReady, puoi esportare l'asset ottimizzato e baked per VR, AR, videogame, viewer realtime o altri workflow di produzione 3D.

L'obiettivo è mantenere il modello abbastanza leggero per l'uso realtime, preservando il dettaglio visivo della scansione originale tramite texture bake.

---

## Prima di esportare

Prima dell'export, controlla:

- la mesh finale è selezionata;
- la mesh ottimizzata ha UV;
- il materiale bake è assegnato;
- i file texture sono stati salvati se ti servono immagini esterne;
- la scala dell'oggetto è corretta;
- l'origine dell'oggetto è posizionata dove serve;
- la densità della mesh è adatta alla piattaforma target.

Per VR e videogame, le performance contano quanto la qualità visiva.

---

## Formati export consigliati

### glTF / GLB

Usa **glTF** o **GLB** per workflow realtime moderni.

Adatto per:

- viewer web;
- preview realtime;
- molti game engine;
- pipeline AR/VR;
- consegna asset leggeri.

`GLB` salva modello e texture in un unico file, utile per condivisione e preview.

### FBX

Usa **FBX** quando la pipeline target lo richiede.

Adatto per:

- workflow Unity;
- workflow Unreal Engine;
- trasferimento da DCC a engine;
- team che usano già FBX come standard.

FBX può funzionare bene, ma i collegamenti texture possono richiedere controllo dopo l'import.

### OBJ

Usa **OBJ** per scambio semplice di mesh statiche.

Adatto per:

- trasferimento geometria base;
- workflow archivio semplici;
- compatibilità con molti tool.

OBJ è semplice, ma è meno completo di glTF o FBX per workflow materiali moderni.

---

## Texture map

In base alle impostazioni, ScanReady può creare:

- texture Base Color;
- Normal map;
- Roughness map;
- Ambient Occlusion map.

Quando esporti verso un'altra applicazione, assicurati che il software esterno usi i file texture corretti.

### Base Color

Collega questa texture all'input colore principale o albedo.

### Normal Map

Collega questa texture all'input normal.

In alcuni software, potresti dover impostare il tipo immagine come **Non-Color** o **Normal Map**.

### Roughness Map

Collega questa texture all'input roughness quando il materiale target lo supporta.

Le roughness map devono essere trattate come dati **Non-Color**.

### Ambient Occlusion

Collega questa texture all'input AO se il motore target lo supporta.

Alcuni workflow combinano AO con altre mappe, in base all'engine o al setup materiale.

---

## Risoluzione texture

Scegli la dimensione texture in base all'uso finale.

### 1024

Buona per piccoli prop, oggetti di sfondo, mobile VR o preview leggere.

### 2048

Buona scelta generale per molti asset.

### 4096

Utile per oggetti ravvicinati o asset importanti.

### 8192

Usala solo quando serve dettaglio molto alto.

Texture grandi aumentano uso memoria, dimensione file, tempo di caricamento e costo realtime.

---

## Ottimizzazione VR

Per VR, mantieni gli asset particolarmente leggeri.

La VR richiede performance stabili perché la scena deve renderizzare fluidamente per entrambi gli occhi.

Prima di esportare per VR:

- riduci il numero di poligoni il più possibile;
- usa texture bake invece di geometria pesante;
- evita dimensioni texture inutilmente grandi;
- usa Normal map per preservare dettaglio superficie;
- testa l'asset nell'ambiente VR target;
- preferisci meno materiali quando possibile.

Un modello che sembra leggero su desktop può essere ancora troppo pesante per visori VR standalone.

---

## Ottimizzazione videogame

Per videogame, bilancia qualità e performance.

Prima di esportare per un game engine:

- mantieni un numero di poligoni adatto alla dimensione dell'asset;
- usa dettaglio texture invece di geometria eccessiva;
- usa Normal map per il dettaglio superficie;
- usa AO map se utile per il materiale;
- tieni sotto controllo il numero di materiali;
- usa dimensioni texture adatte alla distanza camera;
- testa l'asset nella scena reale di gioco, non solo isolato.

Un hero asset può usare più dettaglio di un prop di sfondo.

---

## Note Unity

Quando importi in Unity:

- controlla la scala;
- controlla le assegnazioni materiali;
- assegna Base Color ad Albedo/Base Map;
- assegna Normal map a Normal Map;
- marca la texture Normal map come normal map se Unity lo chiede;
- assegna Roughness/Smoothness in base allo shader che stai usando;
- collega AO se lo shader lo supporta;
- controlla le impostazioni di compressione texture.

Usa dimensioni texture più basse per progetti mobile o standalone VR.

---

## Note Unreal Engine

Quando importi in Unreal Engine:

- controlla scala e orientamento;
- controlla gli slot materiale;
- collega Base Color a Base Color;
- collega Normal map a Normal;
- collega Roughness a Roughness;
- collega AO ad Ambient Occlusion se usata;
- controlla le impostazioni di compressione texture;
- testa l'asset sotto illuminazione realtime.

Per workflow Nanite puoi usare più geometria, ma asset baked leggeri restano utili per VR, mobile, web e applicazioni interattive.

---

## Web e viewer realtime

Per viewer web o presentazioni realtime leggere:

- preferisci GLB quando possibile;
- mantieni dimensioni texture moderate;
- riduci il numero di materiali;
- mantieni bassa la densità mesh;
- testa il tempo di caricamento;
- testa le performance sul dispositivo target.

Un asset più piccolo è più facile da condividere, caricare e visualizzare in modo interattivo.

---

## Conserva la scansione originale

Non eliminare la scansione high-poly originale.

Conservala come asset sorgente per:

- bake futuri;
- export a qualità superiore;
- preservazione archivio;
- risoluzioni texture diverse;
- target di ottimizzazione diversi.

ScanReady crea una versione pratica da produzione, mentre la scansione originale resta la tua sorgente ad alto dettaglio.

---

## Checklist finale

Prima della consegna o dell'export, controlla:

- la mesh è ottimizzata;
- le UV sono presenti;
- il bake Base Color sembra corretto;
- la Normal map sembra corretta se usata;
- la Roughness map sembra corretta se usata;
- la AO map sembra corretta se usata;
- i file texture sono salvati;
- il pulsante **Bake Folder** dello Step 3 apre l'ultima cartella texture salvata;
- la dimensione file è accettabile;
- l'asset funziona bene nell'ambiente target.
