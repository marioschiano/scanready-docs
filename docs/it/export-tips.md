# Consigli export

Dopo il bake, controlla sempre mesh finale, materiali e texture prima di esportare.

<p align="center">
  <img src="../img/high-to-low-workflow.png" alt="Asset baked e ottimizzato pronto per export realtime" style="max-width:900px;width:100%;">
</p>

## Prima di esportare

- seleziona la mesh final;
- controlla Base Color e Normal;
- verifica che le texture siano salvate nella cartella output;
- controlla che non siano rimasti cage o preview visibili se non servono.

## Formati consigliati

### GLB / glTF

Buono per realtime, web e motori moderni.

### FBX

Utile per pipeline generiche, Unity o Unreal.

### OBJ

Semplice, ma meno completo per materiali moderni.

## Texture

Per asset realtime:

- Base Color in JPG o PNG;
- Normal in PNG o TIFF;
- AO in PNG;
- Roughness in PNG o JPG in base al progetto.

## Immagini da aggiungere

- screenshot export glTF;
- screenshot cartella texture;
- screenshot asset importato in un motore realtime.

