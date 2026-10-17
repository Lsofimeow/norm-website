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
    const desktop = matchMedia('(min-width: 992px)');
    desktop.addEventListener('change', () => { if (desktop.matches) close(); });
  }
  const dialog = document.querySelector('.screen-dialog');
  if (dialog) {
    const image = dialog.querySelector('#screen-image');
    const caption = dialog.querySelector('#screen-caption');
    let opener;
    document.querySelectorAll('[data-screen]').forEach(button => {
      button.addEventListener('click', () => {
        opener = button;
        image.src = button.dataset.screen;
        image.alt = button.querySelector('img').alt;
        caption.textContent = button.dataset.caption;
        dialog.showModal();
        document.body.classList.add('screenshot-open');
      });
    });
    dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('screenshot-open');
      if (opener) opener.focus();
    });
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
