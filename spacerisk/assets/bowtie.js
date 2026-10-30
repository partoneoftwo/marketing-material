// Bowtie demo: toggling barriers lets risk particles through (the page works without this script).
document.querySelectorAll("[data-bowtie]").forEach(function (demo) {
  var svg = demo.querySelector("svg.bt"), caption = demo.querySelector("[data-caption]");
  function update() {
    var prev = demo.querySelector('[data-toggle="prev"]').checked, mit = demo.querySelector('[data-toggle="mit"]').checked;
    svg.classList.toggle("prev-off", !prev);
    svg.classList.toggle("mit-off", !mit);
    caption.textContent = prev && mit ? caption.dataset.on : caption.dataset.off;
  }
  demo.querySelectorAll("[data-toggle]").forEach(function (t) { t.addEventListener("change", update); });
});
