(function () {
  const deck = document.querySelector(".deck");
  const slides = Array.from(document.querySelectorAll(".slide"));
  const controls = document.querySelector(".controls");
  const progress = document.querySelector(".progress");
  const pageCount = document.querySelector(".page-count");
  const cornerPage = document.querySelector(".corner-page");
  const jumpMenu = document.querySelector(".jump-menu");
  const soundUrl = deck?.dataset.sound || "../assets/sounds/typewriter-keyboard-a6.mp3";
  const editKey = `dark-ai-ppt-edits:${location.pathname}:${deck?.dataset.version || "v1"}`;
  const logoKey = `dark-ai-ppt-logo:${location.pathname}`;
  let index = Math.max(0, Number(location.hash.replace("#", "")) - 1 || 0);
  let audio;
  let editMode = false;
  let annotateMode = false;

  const zoomItems = Array.from(document.querySelectorAll("[data-zoom-src]"));
  const zoomOverlay = document.querySelector(".zoom-overlay");
  const zoomImage = zoomOverlay?.querySelector("img");
  let zoomIndex = -1;

  const annotationCanvas = document.querySelector(".annotation-canvas");
  const annotationToolbar = document.querySelector(".annotation-toolbar");
  const annotationCtx = annotationCanvas?.getContext("2d");
  let inkColor = "#ff5f5f";
  let drawing = false;
  let lastPoint = null;

  function playTypewriter() {
    try {
      audio = audio || new Audio(soundUrl);
      audio.pause();
      audio.currentTime = 0;
      audio.volume = 0.85;
      audio.play().catch(() => {});
      window.setTimeout(() => audio.pause(), 1900);
    } catch (_) {}
  }

  function update() {
    slides.forEach((slide, i) => slide.classList.toggle("active", i === index));
    const pageText = `${index + 1}/${slides.length}`;
    pageCount.textContent = pageText;
    if (cornerPage) cornerPage.textContent = pageText;
    if (progress) {
      const progressMax = Math.max(0, window.innerWidth - progress.offsetWidth);
      const ratio = slides.length <= 1 ? 0 : index / (slides.length - 1);
      progress.style.left = `${Math.round(progressMax * ratio)}px`;
    }
    updateJumpMenuState();
    history.replaceState(null, "", `#${index + 1}`);
  }

  function slideTitle(slide, i) {
    const title = slide.dataset.title
      || slide.querySelector("[data-editable], .slide-title, .report-title, h1, h2")?.textContent
      || `第 ${i + 1} 页`;
    return title.replace(/\s+/g, " ").trim().slice(0, 34);
  }

  function buildJumpMenu() {
    if (!jumpMenu) return;
    jumpMenu.innerHTML = slides.map((slide, i) => (
      `<button type="button" data-jump="${i}"><b>${i + 1}</b><span>${slideTitle(slide, i)}</span></button>`
    )).join("");
    jumpMenu.querySelectorAll("[data-jump]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        index = Number(button.dataset.jump) || 0;
        jumpMenu.hidden = true;
        update();
      });
    });
  }

  function updateJumpMenuState() {
    jumpMenu?.querySelectorAll("[data-jump]").forEach((button) => {
      button.classList.toggle("active", Number(button.dataset.jump) === index);
    });
  }

  function editableItems() {
    return Array.from(document.querySelectorAll("[data-editable]"));
  }

  function loadEdits() {
    try {
      const edits = JSON.parse(localStorage.getItem(editKey) || "{}");
      editableItems().forEach((item, i) => {
        const key = item.dataset.editable || `editable-${i}`;
        if (edits[key]) item.innerHTML = edits[key];
      });
    } catch (_) {}
  }

  function saveEdits() {
    const edits = {};
    editableItems().forEach((item, i) => {
      const key = item.dataset.editable || `editable-${i}`;
      edits[key] = item.innerHTML;
    });
    localStorage.setItem(editKey, JSON.stringify(edits));
  }

  function setEditMode(enabled) {
    editMode = enabled;
    if (editMode) setAnnotateMode(false);
    document.body.classList.toggle("editing", editMode);
    editableItems().forEach((item) => {
      item.contentEditable = editMode ? "true" : "false";
      item.spellcheck = false;
    });
    document.querySelector(".edit-btn").textContent = editMode ? "完成" : "编辑";
    if (!editMode) saveEdits();
  }

  function resizeAnnotationCanvas() {
    if (!annotationCanvas || !annotationCtx) return;
    const ratio = window.devicePixelRatio || 1;
    annotationCanvas.width = Math.round(window.innerWidth * ratio);
    annotationCanvas.height = Math.round(window.innerHeight * ratio);
    annotationCanvas.style.width = `${window.innerWidth}px`;
    annotationCanvas.style.height = `${window.innerHeight}px`;
    annotationCtx.setTransform(ratio, 0, 0, ratio, 0, 0);
    annotationCtx.lineCap = "round";
    annotationCtx.lineJoin = "round";
    annotationCtx.lineWidth = 5;
  }

  function clearInk() {
    if (!annotationCanvas || !annotationCtx) return;
    annotationCtx.clearRect(0, 0, annotationCanvas.width, annotationCanvas.height);
  }

  function setAnnotateMode(enabled) {
    annotateMode = enabled;
    if (annotateMode && editMode) setEditMode(false);
    document.body.classList.toggle("annotating", annotateMode);
    if (annotationToolbar) annotationToolbar.hidden = !annotateMode;
    const annotateButton = document.querySelector(".annotate-btn");
    if (annotateButton) annotateButton.textContent = annotateMode ? "完成" : "标注";
    if (annotateMode) resizeAnnotationCanvas();
  }

  function applyLogo(src) {
    document.querySelectorAll("[data-logo], .brand-logo img, .top-logo img, .report-logo img").forEach((img) => {
      img.src = src;
    });
  }

  function loadLogo() {
    const src = localStorage.getItem(logoKey);
    if (src) applyLogo(src);
  }

  function revealBottomLine() {
    const line = slides[index]?.querySelector(".bottom-line");
    if (!line || line.classList.contains("revealed")) return false;
    line.classList.add("revealed");
    playTypewriter();
    return true;
  }

  function next(force) {
    if (!force && revealBottomLine()) return;
    index = Math.min(slides.length - 1, index + 1);
    update();
  }

  function prev() {
    index = Math.max(0, index - 1);
    update();
  }

  function openZoom(target) {
    zoomIndex = zoomItems.indexOf(target);
    if (zoomIndex < 0 || !zoomOverlay || !zoomImage) return;
    zoomImage.src = target.dataset.zoomSrc || target.querySelector("img")?.src || "";
    zoomOverlay.classList.add("active");
  }

  function closeZoom() {
    zoomOverlay?.classList.remove("active");
    zoomIndex = -1;
  }

  function switchZoom(delta) {
    if (zoomIndex < 0) return;
    zoomIndex = (zoomIndex + delta + zoomItems.length) % zoomItems.length;
    zoomImage.src = zoomItems[zoomIndex].dataset.zoomSrc || zoomItems[zoomIndex].querySelector("img")?.src || "";
  }

  document.querySelector(".prev-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    prev();
  });

  document.querySelector(".next-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    next(true);
  });

  document.querySelector(".fullscreen-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  });

  document.querySelector(".edit-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    setEditMode(!editMode);
  });

  document.querySelector(".annotate-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    setAnnotateMode(!annotateMode);
  });

  annotationToolbar?.querySelectorAll(".ink-color").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      inkColor = button.dataset.ink || inkColor;
      annotationToolbar.querySelectorAll(".ink-color").forEach((item) => {
        item.classList.toggle("active", item === button);
      });
    });
  });

  annotationToolbar?.querySelector(".ink-clear")?.addEventListener("click", (event) => {
    event.stopPropagation();
    clearInk();
  });

  annotationToolbar?.querySelector(".ink-done")?.addEventListener("click", (event) => {
    event.stopPropagation();
    setAnnotateMode(false);
  });

  document.querySelector(".logo-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    document.querySelector(".logo-input")?.click();
  });

  document.querySelector(".logo-input")?.addEventListener("change", (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const src = String(reader.result);
      localStorage.setItem(logoKey, src);
      applyLogo(src);
    };
    reader.readAsDataURL(file);
  });

  pageCount?.addEventListener("click", (event) => {
    event.stopPropagation();
    if (!jumpMenu) return;
    jumpMenu.hidden = !jumpMenu.hidden;
  });

  editableItems().forEach((item) => {
    item.addEventListener("click", (event) => {
      if (editMode) event.stopPropagation();
    });
    item.addEventListener("input", saveEdits);
  });

  document.querySelector(".more-btn")?.addEventListener("click", (event) => {
    event.stopPropagation();
    controls?.classList.toggle("collapsed");
    if (controls?.classList.contains("collapsed") && jumpMenu) jumpMenu.hidden = true;
  });

  zoomItems.forEach((item) => {
    item.addEventListener("click", (event) => {
      if (annotateMode) return;
      event.stopPropagation();
      openZoom(item);
    });
  });

  annotationCanvas?.addEventListener("pointerdown", (event) => {
    if (!annotateMode || !annotationCtx) return;
    drawing = true;
    lastPoint = { x: event.clientX, y: event.clientY };
    annotationCanvas.setPointerCapture?.(event.pointerId);
  });

  annotationCanvas?.addEventListener("pointermove", (event) => {
    if (!drawing || !lastPoint || !annotationCtx) return;
    annotationCtx.strokeStyle = inkColor;
    annotationCtx.beginPath();
    annotationCtx.moveTo(lastPoint.x, lastPoint.y);
    annotationCtx.lineTo(event.clientX, event.clientY);
    annotationCtx.stroke();
    lastPoint = { x: event.clientX, y: event.clientY };
  });

  ["pointerup", "pointercancel", "pointerleave"].forEach((type) => {
    annotationCanvas?.addEventListener(type, () => {
      drawing = false;
      lastPoint = null;
    });
  });

  zoomOverlay?.addEventListener("click", (event) => {
    if (event.target === zoomOverlay || event.target === zoomImage) closeZoom();
  });
  document.querySelector(".zoom-prev")?.addEventListener("click", (event) => {
    event.stopPropagation();
    switchZoom(-1);
  });
  document.querySelector(".zoom-next")?.addEventListener("click", (event) => {
    event.stopPropagation();
    switchZoom(1);
  });

  document.addEventListener("click", (event) => {
    if (zoomOverlay?.classList.contains("active")) return;
    if (editMode) return;
    if (annotateMode) return;
    if (jumpMenu && !jumpMenu.hidden && !event.target.closest(".jump-menu, .page-count")) {
      jumpMenu.hidden = true;
      return;
    }
    if (event.target.closest("button, a, input, [data-zoom-src], .controls")) return;
    next(false);
  });

  document.addEventListener("keydown", (event) => {
    if (annotateMode) {
      if (event.key === "Escape") setAnnotateMode(false);
      return;
    }
    if (editMode && event.target.closest("[data-editable], input, textarea")) return;
    if (zoomOverlay?.classList.contains("active")) {
      if (event.key === "Escape") closeZoom();
      if (event.key === "ArrowLeft") switchZoom(-1);
      if (event.key === "ArrowRight") switchZoom(1);
      return;
    }
    if (["ArrowRight", "ArrowDown", " ", "Enter", "PageDown"].includes(event.key)) next(false);
    if (["ArrowLeft", "ArrowUp", "Backspace", "PageUp"].includes(event.key)) prev();
  });

  let wheelLock = false;
  document.addEventListener("wheel", (event) => {
    if (wheelLock || annotateMode || zoomOverlay?.classList.contains("active")) return;
    if (Math.abs(event.deltaY) < 24 && Math.abs(event.deltaX) < 24) return;
    wheelLock = true;
    if (event.deltaY > 0 || event.deltaX > 0) next(false);
    else prev();
    setTimeout(() => { wheelLock = false; }, 520);
  }, { passive: true });

  loadEdits();
  loadLogo();
  buildJumpMenu();
  resizeAnnotationCanvas();
  window.addEventListener("resize", () => {
    resizeAnnotationCanvas();
    update();
  });
  update();
})();
