/**
 * AGER GROUP — traitement du formulaire de contact (fonction serverless Vercel)
 *
 * Remplace contact.php, qui ne peut pas s'exécuter sur Vercel.
 * Aucune dépendance npm : l'envoi passe par l'API HTTP de Resend via fetch.
 *
 * Cette version accepte les trois encodages possibles selon la façon dont le
 * formulaire est envoyé — urlencoded, multipart/form-data et JSON — afin de
 * fonctionner sans modifier assets/js/main.js.
 *
 * VARIABLES D'ENVIRONNEMENT À DÉFINIR DANS VERCEL
 *   RESEND_API_KEY      clé API Resend (obligatoire)
 *   MAIL_DESTINATAIRE   par défaut info@agergroup.ci
 *   MAIL_EXPEDITEUR     par défaut "AGER GROUP <site@agergroup.ci>"
 *                       le domaine doit être vérifié chez Resend
 *
 * Le formulaire y accède via la réécriture /contact.php -> /api/contact
 * définie dans vercel.json.
 */

const DESTINATAIRE = process.env.MAIL_DESTINATAIRE || 'info@agergroup.ci';
const EXPEDITEUR = process.env.MAIL_EXPEDITEUR || 'AGER GROUP <site@agergroup.ci>';

const LIBELLES_POLE = {
  immobilier: 'Immobilier',
  juridique: 'Juridique & Administratif',
  recouvrement: 'Recouvrement',
  logistique: 'Transport & Logistique',
  investisseur: "Demande d'investisseur",
  autre: 'Autre / non précisé',
};

function lireFlux(req) {
  return new Promise((resolve, reject) => {
    const morceaux = [];
    req.on('data', (c) => morceaux.push(c));
    req.on('end', () => resolve(Buffer.concat(morceaux)));
    req.on('error', reject);
  });
}

function analyserMultipart(brut, frontiere) {
  const champs = {};
  const separateur = `--${frontiere}`;
  const parties = brut.toString('utf8').split(separateur);

  for (const partie of parties) {
    if (!partie || partie === '--' || partie.trim() === '--') continue;

    const coupure = partie.indexOf('\r\n\r\n');
    if (coupure === -1) continue;

    const entetes = partie.slice(0, coupure);
    const nom = /name="([^"]*)"/.exec(entetes);
    if (!nom) continue;
    if (/filename="/.test(entetes)) continue;

    champs[nom[1]] = partie.slice(coupure + 4).replace(/\r\n$/, '');
  }
  return champs;
}

async function recupererDonnees(req) {
  if (req.body && typeof req.body === 'object' && Object.keys(req.body).length) {
    return req.body;
  }

  const typeContenu = req.headers['content-type'] || '';
  const brut = await lireFlux(req);
  if (!brut.length) return {};

  if (typeContenu.includes('multipart/form-data')) {
    const frontiere = /boundary=(?:"([^"]+)"|([^;]+))/.exec(typeContenu);
    if (!frontiere) return {};
    return analyserMultipart(brut, (frontiere[1] || frontiere[2]).trim());
  }

  if (typeContenu.includes('application/json')) {
    try {
      return JSON.parse(brut.toString('utf8'));
    } catch {
      return {};
    }
  }

  return Object.fromEntries(new URLSearchParams(brut.toString('utf8')));
}

function propre(valeur, max = 500) {
  if (typeof valeur !== 'string') return '';
  return valeur
    .replace(/[\r\n]+/g, ' ')
    .replace(/<[^>]*>/g, '')
    .trim()
    .slice(0, max);
}

function estAjax(req) {
  const h = req.headers || {};
  return (
    (h['x-requested-with'] || '').toLowerCase() === 'xmlhttprequest' ||
    (h.accept || '').includes('application/json')
  );
}

function repondre(req, res, ok, message, code = 200) {
  if (estAjax(req)) {
    return res.status(code).json({ ok, message, success: ok });
  }
  res.setHeader('Location', `/contact.html?envoi=${ok ? 'ok' : 'erreur'}#contenu`);
  return res.status(303).end();
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return repondre(req, res, false, 'Méthode non autorisée.', 405);
  }

  let donnees;
  try {
    donnees = await recupererDonnees(req);
  } catch (e) {
    console.error('Lecture du corps impossible :', e);
    return repondre(req, res, false, 'Requête illisible.', 400);
  }

  if (donnees.societe_web) {
    return repondre(req, res, true, 'Merci, votre demande a bien été transmise.');
  }

  const nom = propre(donnees.nom, 120);
  const societe = propre(donnees.societe, 120);
  const email = propre(donnees.email, 160);
  const telephone = propre(donnees.telephone, 40);
  const pole = propre(donnees.pole, 40);
  const message = typeof donnees.message === 'string'
    ? donnees.message.replace(/<[^>]*>/g, '').trim().slice(0, 4000)
    : '';

  const manques = [];
  if (nom.length < 2) manques.push('le nom');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) manques.push('une adresse e-mail valide');
  if (telephone.length < 6) manques.push('un numéro de téléphone');
  if (message.length < 10) manques.push('un message');
  if (!donnees.consentement) manques.push("votre accord sur l'utilisation des données");

  if (manques.length) {
    return repondre(req, res, false, `Merci d'indiquer ${manques.join(', ')}.`, 422);
  }

  const libellePole = LIBELLES_POLE[pole] || 'Non précisé';
  const horodatage = new Date().toLocaleString('fr-FR', { timeZone: 'Africa/Abidjan' });

  const corps = [
    'Nouvelle demande reçue depuis le site agergroup.ci',
    '',
    `Pôle concerné : ${libellePole}`,
    `Reçue le      : ${horodatage}`,
    '',
    '--- Coordonnées -------------------------------------------',
    `Nom        : ${nom}`,
    `Société    : ${societe || '—'}`,
    `E-mail     : ${email}`,
    `Téléphone  : ${telephone}`,
    '',
    '--- Message -----------------------------------------------',
    message,
  ].join('\n');

  if (!process.env.RESEND_API_KEY) {
    console.error("RESEND_API_KEY absente : impossible d'envoyer le message.");
    console.log(corps);
    return repondre(
      req, res, false,
      `Le service d'envoi n'est pas configuré. Écrivez-nous à ${DESTINATAIRE}.`,
      500
    );
  }

  const enteteResend = {
    Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
    'Content-Type': 'application/json',
  };

  try {
    const envoi = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: enteteResend,
      body: JSON.stringify({
        from: EXPEDITEUR,
        to: [DESTINATAIRE],
        reply_to: email,
        subject: `[Site AGER GROUP] ${libellePole} — ${nom}`,
        text: corps,
      }),
    });

    if (!envoi.ok) {
      console.error('Échec Resend :', envoi.status, await envoi.text());
      throw new Error('envoi refusé');
    }

    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: enteteResend,
      body: JSON.stringify({
        from: EXPEDITEUR,
        to: [email],
        subject: 'Votre demande a bien été reçue — AGER GROUP',
        text: [
          `Bonjour ${nom},`,
          '',
          `Nous avons bien reçu votre demande concernant : ${libellePole}.`,
          '',
          "Nos équipes l'examinent et reviennent vers vous sous 24 heures ouvrées.",
          'Pour toute urgence, vous pouvez nous joindre au +225 07 78 67 24 23.',
          '',
          'Rappel de votre message :',
          '--------------------------------------------',
          message,
          '--------------------------------------------',
          '',
          'Cordialement,',
          '',
          'AGER GROUP',
          "Construire l'avenir, sécuriser le présent.",
          "Abidjan, Côte d'Ivoire — agergroup.ci",
        ].join('\n'),
      }),
    }).catch(() => {});

    return repondre(req, res, true, 'Merci, votre demande a bien été transmise.');
  } catch (erreur) {
    console.error('Erreur de traitement du formulaire :', erreur);
    return repondre(
      req, res, false,
      `L'envoi a échoué. Merci de nous écrire à ${DESTINATAIRE}.`,
      500
    );
  }
}
