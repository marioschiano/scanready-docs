# Step 2 - UV / Cage

Step 2 genera le UV e prepara il cage per il bake.

<p align="center">
  <img src="../img/step2-uv-01.jpg" alt="Layout UV generato dalla mesh ottimizzata" style="max-width:760px;width:100%;">
</p>

## Obiettivo

Creare una mesh UV pronta per ricevere le texture dalla mesh high poly.

## Smart UV Preset

Il preset Smart UV cambia il comportamento di Smart UV Project.

Se la mesh UV non esiste ancora, dopo aver cambiato il preset ScanReady ti dira:

`Press Generate UVs.`

Se invece la mesh UV esiste gia, il Workflow Status puo consigliarti:

`Press Bake Textures.`

Questo succede perche il bake puo rigenerare automaticamente le UV quando serve.

<p align="center">
  <img src="../img/step2-uv-02.png" alt="Confronto checker texture con UV stirate e UV pulite" style="max-width:1000px;width:100%;">
</p>

## Cage

Il cage serve a catturare i dettagli della mesh high poly durante il bake.

<p align="center">
  <img src="../img/cage_01_red.png" alt="Avviso cage rosso con setup non valido per il bake" style="max-width:1000px;width:100%;">
</p>

### Cage Extrusion

Aumenta la distanza del cage.

Il valore parte da `0`, ma dopo che viene calcolato o regolato non deve essere azzerato solo perche cambi un preset UV.

### Auto Cage Extrusion

Calcola automaticamente una distanza iniziale per il cage.

### Show Cage

Mostra o nasconde il cage in viewport.

## Regola importante

Il cage deve diventare verde.

Se il cage e rosso o non copre bene la high poly, usa **Cage Extrusion** o **Auto Cage Extrusion**.

<p align="center">
  <img src="../img/step2-uv-03.png" alt="Confronto dimensione cage troppo piccolo, corretto e troppo grande" style="max-width:1100px;width:100%;">
</p>

<p align="center">
  <img src="../img/step2-uv-04.png" alt="Confronto effetto del cage sulla normal map baked" style="max-width:1100px;width:100%;">
</p>

## Immagini/GIF da aggiungere

- GIF cage rosso che diventa verde.
- Screenshot Smart UV Preset.
- Screenshot Auto Cage Extrusion.
- Screenshot Workflow Status dopo cambio UV.

