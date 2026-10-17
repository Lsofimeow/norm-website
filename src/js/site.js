(() => {
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  document.documentElement.classList.add('js');
  if (menu && nav) {
    const close = () => { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { close(); menu.focus(); }
    });
    const desktop = matchMedia('(min-width: 801px)');
    desktop.addEventListener('change', () => { if (desktop.matches) close(); });
  }
  document.querySelectorAll('[data-workflow]').forEach(workflow => {
    const buttons = [...workflow.querySelectorAll('[data-step]')];
    const panels = [...workflow.querySelectorAll('[data-panel]')];
    const select = index => {
      buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
      panels.forEach((panel, i) => { panel.hidden = i !== index; });
    };
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => select(index));
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (index + 1) % buttons.length;
        if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (index - 1 + buttons.length) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next); buttons[next].focus(); }
      });
    });
    select(0);
  });
})();
