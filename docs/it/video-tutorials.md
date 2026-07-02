# <span class="sr-addon-icon sr-icon-render" title="Video Tutorials"></span>Video Tutorials

Questa pagina raccoglie i video tutorial di ScanReady nell'ordine consigliato per imparare il workflow.

I video possono essere guardati direttamente dentro la documentazione. Quando pubblichi nuovi tutorial su YouTube, possiamo sostituire ogni slot con l'embed del video corrispondente.

!!! tip "Ordine consigliato"
    L'ordine segue il percorso di un nuovo utente: installazione, One Click Bake, workflow manuale, Advanced e troubleshooting.

---

## 1. Installazione

Come installare ScanReady come Blender Extension e verificare che il pannello sia disponibile in Blender.

<div class="sr-video">
  <div class="sr-video-placeholder">
    <div>
      <strong>Video Installazione</strong>
      <span>Sostituire questo slot con l'embed YouTube quando il video è pronto.</span>
    </div>
  </div>
</div>

---

## 2. One Click Bake

Workflow completo per convertire una scansione high-poly in un asset ottimizzato con UV, cage, bake e materiali finali.

<div class="sr-video">
  <div class="sr-video-placeholder">
    <div>
      <strong>Video One Click Bake</strong>
      <span>Sostituire questo slot con l'embed YouTube quando il video è pronto.</span>
    </div>
  </div>
</div>

---

## 3. Workflow manuale

Guida passo passo per controllare separatamente Step 1, Step 2 e Step 3.

<div class="sr-video">
  <div class="sr-video-placeholder">
    <div>
      <strong>Video Workflow manuale</strong>
      <span>Sostituire questo slot con l'embed YouTube quando il video è pronto.</span>
    </div>
  </div>
</div>

---

## 4. Adaptive Reduce e Advanced

Come leggere i pesi Adaptive Reduce, scegliere i preset, proteggere i bordi importanti e regolare le impostazioni avanzate.

<div class="sr-video">
  <div class="sr-video-placeholder">
    <div>
      <strong>Video Adaptive Reduce / Advanced</strong>
      <span>Sostituire questo slot con l'embed YouTube quando il video è pronto.</span>
    </div>
  </div>
</div>

---

## 5. Troubleshooting bake

Come correggere cage, UV, texture nere, normal map piatte, problemi di memoria e bake non riusciti.

<div class="sr-video">
  <div class="sr-video-placeholder">
    <div>
      <strong>Video Troubleshooting bake</strong>
      <span>Sostituire questo slot con l'embed YouTube quando il video è pronto.</span>
    </div>
  </div>
</div>

---

## Come inserire un video YouTube

Quando hai l'ID del video, sostituisci lo slot placeholder con questo blocco:

```html
<div class="sr-video">
  <iframe
    src="https://www.youtube.com/embed/VIDEO_ID"
    title="ScanReady tutorial"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>
```

L'ID è la parte finale dell'URL YouTube. Per esempio, in `https://www.youtube.com/watch?v=ABC123`, l'ID è `ABC123`.
