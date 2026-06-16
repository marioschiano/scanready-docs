# ScanReady

ScanReady e un addon per Blender pensato per trasformare scansioni 3D pesanti in asset piu leggeri, con UV e texture bake pronti per VR, videogame e realtime.

Questa e la versione italiana della documentazione. La useremo come base di lavoro: prima completiamo testi, immagini e GIF in italiano, poi aggiorneremo la versione inglese.

<p align="center">
  <img src="../img/hero.png" alt="ScanReady workflow overview" style="max-width:620px;width:100%;">
</p>

## Cosa fa ScanReady

- crea una preview lowpoly dalla scansione originale;
- riduce la mesh mantenendo piu dettaglio nelle zone importanti;
- genera UV automatiche con Smart UV Project;
- crea e controlla il cage per il bake;
- cuoce Base Color, Normal, Roughness e Occlusion;
- salva un asset finale piu adatto a motori realtime.

<p align="center">
  <img src="../img/why-scanready-adaptive-optimization.png" alt="Confronto tra Blender Decimate e ScanReady Adaptive Reduce" style="max-width:1000px;width:100%;">
</p>

## Percorso consigliato

1. Installa l'addon.
2. Seleziona la mesh high poly o il parent della scansione.
3. Usa **One Click Bake** per un flusso automatico.
4. Oppure lavora a step: Preview / Reduce, UV / Cage, Bake / Output.

![Before After](../img/one_click_before_after.jpg)

<p align="center">
  <img src="../img/one-click-bake.gif" alt="ScanReady One Click Bake workflow" width="700">
</p>

## Pagine principali

- [Installazione](installation.md)
- [Guida rapida](quick-start.md)
- [One Click Bake](one-click.md)
- [Step 1 - Preview / Reduce](step1.md)
- [Step 2 - UV / Cage](step2.md)
- [Step 3 - Bake / Output](step3.md)
- [Impostazioni avanzate](advanced.md)
- [Risoluzione problemi](troubleshooting.md)

## Dove inserire immagini o GIF

| Punto | Tipo consigliato |
| --- | --- |
| Home | immagine hero con high poly e final affiancati |
| Guida rapida | GIF breve del flusso One Click |
| Step 1 | GIF riduzione e wireframe |
| Step 2 | GIF cage che diventa verde |
| Step 3 | screenshot materiali finali e texture salvate |

