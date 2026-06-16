# Step 3 - Bake / Output

Step 3 cuoce le texture dalla mesh high poly alla mesh finale.

<p align="center">
  <img src="../img/high-to-low-workflow.png" alt="Risultato baked con poligoni ridotti e dettaglio visivo preservato" style="max-width:900px;width:100%;">
</p>

## Mappe supportate

ScanReady supporta:

- Base Color;
- Normal;
- Roughness;
- Occlusion.

## Texture Preset

Scegli la risoluzione delle texture.

Valori piu alti aumentano qualita e tempo di bake.

## Bake Materials

Divide il bake in piu materiali.

Se aumenti il numero di materiali, ScanReady sa che deve aggiornare il layout UV. Quando premi **Bake Textures**, l'addon rigenera automaticamente le UV se necessario e poi fa il bake.

Per questo il Workflow Status puo dire:

`Press Bake Textures.`

## Bake Textures

Esegue il bake delle mappe selezionate.

Se una mappa e gia aggiornata e non hai cambiato parametri, ScanReady dovrebbe evitare di rifarla.

Esempio:

- hai gia fatto Base Color;
- attivi Normal;
- ScanReady dovrebbe cuocere solo Normal.

## Immagini/GIF da aggiungere

- Screenshot mappe bake selezionate.
- Screenshot cartella output.
- Screenshot materiali finali.
- GIF bake con progress aggiornato.

