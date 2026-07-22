(() => {
  'use strict';
  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => [...root.querySelectorAll(selector)];
  const navItem = qs('.nav__item');
  const navButton = qs('.nav__bouton');
  const closeDesktopMenu = () => {
    if (!navItem || !navButton) return;
    navItem.classList.remove('is-open');
    navButton.setAttribute('aria-expanded', 'false');
  };
  if (navItem && navButton) {
    navButton.addEventListener('click', (event) => {
      event.stopPropagation();
      const open = navItem.classList.toggle('is-open');
      navButton.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', (event) => {
      if (!navItem.contains(event.target)) closeDesktopMenu();
    });
  }
  const burger = qs('.burger');
  const mobileNav = qs('.nav-mobile');
  const closeMobileMenu = () => {
    if (!burger || !mobileNav) return;
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Ouvrir le menu');
    mobileNav.classList.remove('is-open');
  };
  if (burger && mobileNav) {
    burger.addEventListener('click', () => {
      const open = burger.getAttribute('aria-expanded') !== 'true';
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      mobileNav.classList.toggle('is-open', open);
    });
    qsa('a', mobileNav).forEach((link) => link.addEventListener('click', closeMobileMenu));
  }
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeDesktopMenu();
      closeMobileMenu();
    }
  });
  const reveals = qsa('.reveal');
  reveals.forEach((element) => {
    const delay = Number.parseInt(element.dataset.delai || '0', 10);
    element.style.setProperty('--delai', `${Number.isFinite(delay) ? delay : 0}ms`);
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px' });
    reveals.forEach((element) => observer.observe(element));
  } else {
    reveals.forEach((element) => element.classList.add('is-visible'));
  }
  const counters = qsa('[data-compteur]');
  const animateCounter = (element) => {
    if (element.dataset.anime === 'oui') return;
    element.dataset.anime = 'oui';
    const target = Number.parseInt(element.dataset.compteur || '0', 10);
    const suffix = element.dataset.suffixe || '';
    const start = performance.now();
    const duration = 1050;
    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = `${Math.round(target * eased)}${suffix}`;
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.45 });
    counters.forEach((element) => counterObserver.observe(element));
  } else {
    counters.forEach(animateCounter);
  }
  const poleSelect = qs('#pole');
  if (poleSelect) {
    const pole = new URLSearchParams(window.location.search).get('pole');
    if (pole && [...poleSelect.options].some((option) => option.value === pole)) {
      poleSelect.value = pole;
    }
  }
  const statusBox = qs('.form__retour');
  const envoi = new URLSearchParams(window.location.search).get('envoi');
  if (statusBox && envoi) {
    const ok = envoi === 'ok';
    statusBox.textContent = ok
      ? 'Merci, votre demande a bien été transmise.'
      : "Votre demande n'a pas pu être envoyée. Vous pouvez nous écrire directement à info@agergroup.ci.";
    statusBox.classList.add('is-visible', ok ? 'is-ok' : 'is-erreur');
  }
  const form = qs('form[data-ajax]');
  if (form && statusBox) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      statusBox.className = 'form__retour is-visible';
      if (!form.checkValidity()) {
        form.reportValidity();
        statusBox.textContent = 'Merci de renseigner tous les champs obligatoires.';
        statusBox.classList.add('is-erreur');
        return;
      }
      const action = form.getAttribute('action') || '';
      if (window.location.hostname.endsWith('.vercel.app') && action.endsWith('.php')) {
        statusBox.textContent = "Le formulaire est en cours d'activation. Pour le moment, écrivez-nous à info@agergroup.ci ou appelez le +225 07 78 67 24 23.";
        statusBox.classList.add('is-erreur');
        return;
      }
      const submit = qs('[type="submit"]', form);
      if (submit) submit.disabled = true;
      statusBox.textContent = 'Envoi en cours…';
      try {
        const response = await fetch(action, {
          method: form.method || 'POST',
          body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || data.ok === false) throw new Error(data.message || "L'envoi a échoué.");
        statusBox.textContent = data.message || 'Merci, votre demande a bien été transmise.';
        statusBox.classList.add('is-ok');
        form.reset();
      } catch (error) {
        statusBox.textContent = error.message || "Votre demande n'a pas pu être envoyée. Écrivez-nous à info@agergroup.ci.";
        statusBox.classList.add('is-erreur');
      } finally {
        if (submit) submit.disabled = false;
      }
    });
  }

  const presidentCard = qs('#president .president__carte');
  const presidentLogo = presidentCard ? qs('.marque', presidentCard) : null;
  if (presidentCard && presidentLogo) {
    const photo = document.createElement('img');
    photo.src = 'assets/img/president-adouko-gerard.svg';
    photo.alt = 'Adouko Gérard, Président Directeur Général d’AGER GROUP';
    photo.width = 480;
    photo.height = 600;
    photo.loading = 'lazy';
    photo.style.cssText = 'display:block;width:100%;max-width:320px;aspect-ratio:4/5;margin:0 auto 26px;object-fit:cover;object-position:center top;border-radius:8px;box-shadow:0 14px 34px rgba(23,61,86,.18)';
    const logoWrapper = presidentLogo.closest('span');
    (logoWrapper || presidentLogo).replaceWith(photo);
  }
})();