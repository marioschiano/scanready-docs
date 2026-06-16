# Step 1 - Preview / Reduce

Step 1 crea una preview lowpoly della scansione.

<p align="center">
  <img src="../img/step1-reduce.gif" alt="Controllo Optimize Reduce che aggiorna la densita della preview lowpoly" style="max-width:820px;width:100%;">
</p>

## Obiettivo

Ridurre la mesh originale mantenendo una buona leggibilita delle forme.

## Controlli principali

### Final Faces

Numero indicativo di facce desiderate per la preview lowpoly.

Valori piu bassi rendono la mesh piu leggera. Valori piu alti conservano piu dettaglio.

### Optimize / Reduce

Controlla la percentuale di riduzione.

Esempio: `0.10` mantiene circa il 10% della geometria.

### Create Lowpoly Preview

Crea o aggiorna la mesh lowpoly preview.

Se non hai cambiato parametri importanti, ScanReady puo avvisarti che la preview e gia aggiornata.

<p align="center">
  <img src="../img/step1-preview-reduce.png" alt="Pannello Step 1 Preview Reduce con Create Lowpoly Preview" style="width:320px; max-width:100%;">
</p>

## Adaptive Reduce

Adaptive Reduce protegge le zone con piu dettaglio e riduce di piu le aree piatte.

Preset disponibili:

- **Balanced**
- **Preserve Details**
- **Flat Surfaces**

### Show Adaptive Weights

Mostra i pesi sulla preview:

- rosso: aree piatte ridotte di piu;
- blu/verde: dettaglio protetto.

<p align="center">
  <img src="../img/step1-slider_reduce.gif" alt="Slider Optimize Reduce che aggiorna il valore della preview lowpoly" style="width:360px; max-width:100%;">
</p>

<p align="center">
  <img src="../img/step1-wireframe.gif" alt="Show Wireframe sulla preview ottimizzata" style="max-width:820px;width:100%;">
</p>

<p align="center">
  <img src="../img/step1-checker.gif" alt="Show Checker sulla preview ottimizzata" style="max-width:820px;width:100%;">
</p>

<p align="center">
  <img src="../img/step1-checker-mix-scale.png" alt="Controlli Checker Mix e Checker Scale" style="width:320px; max-width:100%;">
</p>

<p align="center">
  <img src="../img/step1-checker-mix.gif" alt="Checker Mix cambia la forza dell'overlay checker" style="max-width:820px;width:100%;">
</p>

<p align="center">
  <img src="../img/step1-checker-scale.gif" alt="Checker Scale cambia la dimensione dei quadrati checker" style="max-width:820px;width:100%;">
</p>

<p align="center">
  <img src="../img/step1-cleaner.gif" alt="Pulizia mesh prima della preview lowpoly" style="max-width:820px;width:100%;">
</p>

## Quando rifare Step 1

Rifai **Create Lowpoly Preview** se cambi:

- Final Faces;
- Optimize / Reduce;
- Adaptive Preset;
- valori manuali di Adaptive Reduce;
- opzioni di pulizia mesh in Advanced.

## Immagini/GIF da aggiungere

- GIF riduzione mesh.
- Screenshot Show Adaptive Weights.
- GIF wireframe prima/dopo.
- Screenshot Workflow Status che consiglia Step 1.

