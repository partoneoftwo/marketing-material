// Bowtie demo: toggling barriers lets risk particles through (the page works without this script).
// The hazard event (button or the knot in the drawing) starts off; pressing it switches both barrier sides on.
document.querySelectorAll("[data-bowtie]").forEach(function (demo) {
  var svg = demo.querySelector("svg.bt"), caption = demo.querySelector("[data-caption]");
  var prevBox = demo.querySelector('[data-toggle="prev"]'), mitBox = demo.querySelector('[data-toggle="mit"]');
  var eventBtn = demo.querySelector("[data-event]"), knot = demo.querySelector("[data-event-knot]");
  function update() {
    var prev = prevBox.checked, mit = mitBox.checked;
    svg.classList.toggle("prev-off", !prev);
    svg.classList.toggle("mit-off", !mit);
    caption.textContent = prev && mit ? caption.dataset.on : caption.dataset.off;
    if (eventBtn) eventBtn.setAttribute("aria-pressed", String(prev && mit));
  }
  function pressEvent() {
    var on = eventBtn.getAttribute("aria-pressed") !== "true";
    prevBox.checked = on;
    mitBox.checked = on;
    update();
  }
  demo.querySelectorAll("[data-toggle]").forEach(function (t) { t.addEventListener("change", update); });
  if (eventBtn) {
    demo.querySelector("[data-event-row]").hidden = false;
    eventBtn.addEventListener("click", pressEvent);
    if (knot) {
      knot.setAttribute("role", "button");
      knot.setAttribute("tabindex", "0");
      knot.setAttribute("aria-label", eventBtn.textContent);
      knot.addEventListener("click", pressEvent);
      knot.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pressEvent(); } });
    }
    prevBox.checked = false;  // default: hazard event not activated, no barriers
    mitBox.checked = false;
  }
  update();
});
