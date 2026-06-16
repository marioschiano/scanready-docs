# One Click Bake

**One Click Bake** esegue automaticamente il flusso completo: preview lowpoly, UV, cage e bake.

<p align="center">
  <img src="../img/quick-start-one-click.png" alt="Pulsante One Click Bake in Blender" style="width:240px; max-width:100%;">
</p>

<p align="center">
  <img src="../img/one-click-bake.gif" alt="Workflow animato One Click Bake in Blender" style="max-width:820px;width:100%;">
</p>

## Quando usarlo

Usalo quando vuoi un risultato rapido senza regolare ogni step manualmente.

E utile per:

- test veloci;
- prototipi;
- asset da controllare subito in realtime;
- scansioni dove i preset di default funzionano bene.

## Cosa succede quando premi One Click Bake

1. ScanReady prepara la sorgente.
2. Crea o aggiorna la preview lowpoly.
3. Genera le UV.
4. Stima il cage se serve.
5. Esegue il bake delle mappe selezionate.
6. Mostra la mesh finale.

## Comportamento della cache

Se ripremi One Click Bake senza cambiare parametri, ScanReady non dovrebbe rifare lavoro inutile.

Se cambi solo la risoluzione texture, rifara il bake.

Se cambi un parametro di Step 1, rifara la preview e poi gli step necessari.

Se cambi un parametro UV quando la mesh UV esiste gia, il bake rigenera le UV automaticamente prima di cuocere.

<p align="center">
  <img src="../img/one_click_before_after.jpg" alt="Confronto prima e dopo One Click Bake" style="max-width:820px;width:100%;">
</p>

## Immagini da aggiungere

- GIF del pulsante One Click Bake.
- Screenshot del Global Progress durante le fasi.
- Screenshot finale con mesh final visibile.

