/* Progressive enhancement: step through a reflection or learning model. */
(() => {
  document.querySelectorAll('[data-stepper]').forEach(group => {
    const scope = group.closest('[data-stepper-root]') || group.parentElement || group;
    const buttons = [...group.querySelectorAll('[data-stage]')];
    const items = [...scope.querySelectorAll('[data-panel]')];

    function activate(stage) {
      buttons.forEach(button => {
        button.setAttribute('aria-pressed', String(button.dataset.stage === stage));
      });
      items.forEach(panel => {
        panel.hidden = panel.dataset.panel !== stage;
      });
    }

    buttons.forEach(button => {
      button.addEventListener('click', () => activate(button.dataset.stage));
    });
    if (buttons.length) activate(buttons[0].dataset.stage);
  });
})();
