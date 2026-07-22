#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGER GROUP — générateur de pages statiques.

Ce script assemble l'en-tête, le pied de page et les métadonnées communes,
puis écrit les fichiers .html définitifs à la racine du site.

Utilisation :  python3 build.py
Il n'est PAS nécessaire pour héberger le site : les .html produits sont
autonomes. Il sert uniquement à modifier le menu ou le pied de page une
seule fois pour toutes les pages.
"""

import os
import datetime

RACINE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Paramètres du site — à modifier ici uniquement
# ---------------------------------------------------------------------------
SITE_URL = "https://agergroup.ci"
SOCIETE = "AGER GROUP"
SLOGAN = "Construire l'avenir, sécuriser le présent."
TEL_AFF = "+225 07 78 67 24 23"
TEL_URI = "+2250778672423"
EMAIL = "info@agergroup.ci"
VILLE = "Abidjan, Côte d'Ivoire"
ANNEE = datetime.date.today().year

# ---------------------------------------------------------------------------
# Pictogrammes
# ---------------------------------------------------------------------------
IC = {
    "immobilier": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14"/><path d="M9 21v-5h6v5"/><path d="M9 10h.01M15 10h.01"/></svg>',
    "juridique": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v5c0 4.5-3.2 8.6-8 10-4.8-1.4-8-5.5-8-10V6z"/><path d="M9 12l2 2 4-4"/></svg>',
    "recouvrement": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18"/><path d="M6 20V11M11 20V6M16 20v-6M21 20V9"/></svg>',
    "logistique": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 7h11v10H2z"/><path d="M13 10h4l4 4v3h-8z"/><circle cx="6.5" cy="18.5" r="1.8"/><circle cx="17" cy="18.5" r="1.8"/></svg>',
    "fleche": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
    "croix": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>',
    "chevron": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM10 9h3.8v1.7h.05c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.78 2.5 4.78 5.76V21h-4v-5.6c0-1.34-.03-3.07-1.9-3.07-1.9 0-2.2 1.46-2.2 2.97V21h-4z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 9h3V5.5h-2.6C11.6 5.5 10.5 7.2 10.5 9.3V11H8v3.5h2.5V22H14v-7.5h2.6L17 11h-3V9.6c0-.4.2-.6.7-.6z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 3h3l-6.6 7.5L21.8 21h-6l-4.7-6.1L5.6 21h-3l7-8-6.9-10h6.2l4.3 5.6zm-1 16h1.7L7.6 4.8H5.8z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12s0-3.3-.4-4.9a2.6 2.6 0 00-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4a2.6 2.6 0 00-1.8 1.8C2 8.7 2 12 2 12s0 3.3.4 4.9c.2.9.9 1.5 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.6 2.6 0 001.8-1.8C22 15.3 22 12 22 12zM10 15.2V8.8l5.3 3.2z"/></svg>',
}

MARQUE = (
    '<svg class="marque" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" '
    'role="img" aria-label="AGER GROUP">'
    '<rect width="100" height="100" fill="#173D56"/>'
    '<rect x="20.5" y="23.5" width="59" height="53" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
    '<text x="50" y="53" text-anchor="middle" font-family="Montserrat, Arial, sans-serif" '
    'font-size="27" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">AG</text>'
    '<rect x="34" y="61" width="32" height="3" fill="#D4A62A"/></svg>'
)

# ---------------------------------------------------------------------------
# Les quatre pôles — source unique de vérité
# ---------------------------------------------------------------------------
POLES = [
    {
        "id": "immobilier",
        "nom": "Immobilier",
        "fichier": "immobilier.html",
        "verbe": "Bâtir",
        "accroche": "Vente, location, gestion, promotion et expertise du patrimoine.",
        "resume": "Nous accompagnons la constitution, la valorisation et la gestion du patrimoine "
                  "immobilier, du terrain nu jusqu'à la mise en location.",
        "puces": ["Vente et location", "Gestion locative et syndic",
                  "Promotion et lotissement", "Expertise et construction"],
    },
    {
        "id": "juridique",
        "nom": "Juridique & Administratif",
        "fichier": "juridique.html",
        "verbe": "Sécuriser",
        "accroche": "Conseil, formalités, constitution de sociétés et conformité.",
        "resume": "Nous sécurisons les démarches, les dossiers et les engagements pour que "
                  "chaque décision repose sur une base juridique solide.",
        "puces": ["Constitution de sociétés", "Formalités et immatriculations",
                  "Conseil et rédaction d'actes", "Accompagnement réglementaire"],
    },
    {
        "id": "recouvrement",
        "nom": "Recouvrement",
        "fichier": "recouvrement.html",
        "verbe": "Recouvrer",
        "accroche": "Recouvrement amiable et contentieux, gestion du risque client.",
        "resume": "Nous transformons les créances en trésorerie par une démarche structurée, "
                  "traçable et respectueuse de la relation commerciale.",
        "puces": ["Recouvrement amiable", "Procédures contentieuses",
                  "Négociation et échéanciers", "Prévention du risque client"],
    },
    {
        "id": "logistique",
        "nom": "Transport & Logistique",
        "fichier": "logistique.html",
        "verbe": "Transporter",
        "accroche": "Transport, distribution, gestion de flotte et suivi opérationnel.",
        "resume": "Nous assurons la circulation fiable des marchandises et la coordination "
                  "des opérations, avec une visibilité complète sur chaque étape.",
        "puces": ["Transport de marchandises", "Distribution et livraison",
                  "Gestion de flotte", "Logistique intégrée"],
    },
]

POLE_PAR_ID = {p["id"]: p for p in POLES}

# ---------------------------------------------------------------------------
# Gabarits
# ---------------------------------------------------------------------------

def head(titre, description, fichier, page_classe="", jsonld=""):
    canonique = f"{SITE_URL}/{'' if fichier == 'index.html' else fichier}"
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
<meta name="author" content="{SOCIETE}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonique}">

<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{SOCIETE}">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonique}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titre}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta name="theme-color" content="#173D56">

<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="assets/img/favicon.ico">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{jsonld}
</head>
<body{f' class="{page_classe}"' if page_classe else ''}>
<a class="skip" href="#contenu">Aller au contenu</a>
"""


def entete():
    sous = "".join(
        f'<li><a href="{p["fichier"]}">{p["nom"]}<small>{p["accroche"]}</small></a></li>'
        for p in POLES
    )
    sous_mobile = "".join(
        f'<a href="{p["fichier"]}">{p["nom"]}</a>' for p in POLES
    )
    return f"""<header class="entete">
  <div class="wrap entete__inner">
    <a class="logo" href="index.html" aria-label="{SOCIETE} — accueil">
      <span class="logo__marque">{MARQUE}</span>
      <span class="logo__texte">
        <span class="logo__nom">{SOCIETE}</span>
        <span class="logo__slogan">Groupe multiservices</span>
      </span>
    </a>

    <nav class="nav" aria-label="Navigation principale">
      <a href="index.html">Accueil</a>
      <a href="groupe.html">Le Groupe</a>
      <div class="nav__item">
        <button class="nav__bouton" type="button" aria-expanded="false">Nos pôles {IC['chevron']}</button>
        <ul class="sous-menu" style="list-style:none;margin:0;padding:10px">{sous}</ul>
      </div>
      <a href="investisseurs.html">Investisseurs</a>
      <a href="contact.html">Contact</a>
    </nav>

    <div class="entete__actions">
      <a class="entete__tel" href="tel:{TEL_URI}">{TEL_AFF}</a>
      <a class="btn btn--or" href="contact.html">Nous contacter</a>
      <button class="burger" type="button" aria-expanded="false" aria-label="Ouvrir le menu"
              aria-controls="menu-mobile"><span></span></button>
    </div>
  </div>

  <div class="nav-mobile" id="menu-mobile">
    <div class="wrap">
      <a href="index.html">Accueil</a>
      <a href="groupe.html">Le Groupe</a>
      <p class="nav-mobile__titre">Nos pôles</p>
      <div class="sous-liste">{sous_mobile}</div>
      <a href="investisseurs.html">Investisseurs</a>
      <a href="contact.html">Contact</a>
      <a class="btn btn--or" href="contact.html">Demander un rendez-vous</a>
    </div>
  </div>
</header>

<main id="contenu">
"""


def cta_final(titre, texte, bouton1=("contact.html", "Demander un rendez-vous"),
              bouton2=("investisseurs.html", "Espace investisseurs")):
    return f"""<section class="cta-final">
  <div class="wrap cta-final__inner">
    <div>
      <h2>{titre}</h2>
      <p>{texte}</p>
    </div>
    <div class="btn-groupe">
      <a class="btn btn--bleu" href="{bouton1[0]}">{bouton1[1]}</a>
      <a class="btn btn--ligne-bleu" href="{bouton2[0]}">{bouton2[1]}</a>
    </div>
  </div>
</section>
"""


def pied():
    liens_poles = "".join(f'<li><a href="{p["fichier"]}">{p["nom"]}</a></li>' for p in POLES)
    return f"""</main>

<footer class="pied">
  <div class="wrap">
    <div class="pied__grille">
      <div>
        <div class="pied__logo">
          <span class="marque" style="width:46px">{MARQUE}</span>
          <strong>{SOCIETE}</strong>
        </div>
        <p class="pied__slogan">{SLOGAN}</p>
        <p>Groupe multiservices basé à {VILLE}. Nous accompagnons entreprises,
           institutions et particuliers sur quatre métiers complémentaires.</p>
        <div class="reseaux">
          <a href="#" aria-label="LinkedIn" rel="noopener">{IC['linkedin']}</a>
          <a href="#" aria-label="Facebook" rel="noopener">{IC['facebook']}</a>
          <a href="#" aria-label="X" rel="noopener">{IC['x']}</a>
          <a href="#" aria-label="YouTube" rel="noopener">{IC['youtube']}</a>
        </div>
      </div>

      <div>
        <h4>Nos pôles</h4>
        <ul>{liens_poles}</ul>
      </div>

      <div>
        <h4>Le groupe</h4>
        <ul>
          <li><a href="groupe.html">Qui sommes-nous</a></li>
          <li><a href="groupe.html#valeurs">Nos valeurs</a></li>
          <li><a href="groupe.html#president">Mot du Président</a></li>
          <li><a href="investisseurs.html">Investisseurs</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div>
        <h4>Nous joindre</h4>
        <ul>
          <li><a href="tel:{TEL_URI}">{TEL_AFF}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{VILLE}</li>
          <li><a href="{SITE_URL}">agergroup.ci</a></li>
        </ul>
        <p style="margin-top:18px;font-size:.86rem">Du lundi au vendredi<br>8 h – 18 h (GMT)</p>
      </div>
    </div>

    <div class="pied__bas">
      <p style="margin:0">© {ANNEE} {SOCIETE}. Tous droits réservés.</p>
      <nav aria-label="Liens légaux">
        <a href="mentions-legales.html">Mentions légales</a>
        <a href="confidentialite.html">Politique de confidentialité</a>
        <a href="plan-du-site.html">Plan du site</a>
      </nav>
    </div>
  </div>
</footer>

<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def page_tete(fil, titre, chapo):
    fils = ' <span>›</span> '.join(fil)
    return f"""<section class="page-tete">
  <div class="wrap">
    <p class="fil">{fils}</p>
    <h1>{titre}</h1>
    <p>{chapo}</p>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
JSONLD_ORG = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{SOCIETE}",
  "url": "{SITE_URL}",
  "logo": "{SITE_URL}/assets/img/logo-ager.svg",
  "image": "{SITE_URL}/assets/img/og-image.jpg",
  "slogan": "{SLOGAN}",
  "description": "Groupe multiservices ivoirien : immobilier, juridique et administratif, recouvrement, transport et logistique.",
  "email": "{EMAIL}",
  "telephone": "{TEL_AFF}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "Abidjan",
    "addressCountry": "CI"
  }},
  "areaServed": [
    {{"@type": "Country", "name": "Côte d'Ivoire"}},
    {{"@type": "Place", "name": "Afrique de l'Ouest"}}
  ],
  "founder": {{"@type": "Person", "name": "Adouko Gérard", "jobTitle": "Président Directeur Général"}},
  "knowsAbout": ["Immobilier", "Droit des affaires", "Recouvrement de créances", "Transport et logistique"]
}}
</script>"""

JSONLD_FAQ = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Faut-il faire appel à plusieurs pôles à la fois ?","acceptedAnswer":{"@type":"Answer","text":"Non. Chaque pôle intervient de façon autonome. L'intérêt du groupe est de pouvoir mobiliser les autres compétences si votre dossier l'exige, sans que vous ayez à chercher un nouveau prestataire."}},
    {"@type":"Question","name":"Intervenez-vous en dehors d'Abidjan ?","acceptedAnswer":{"@type":"Answer","text":"Oui. Nos équipes interviennent sur l'ensemble du territoire ivoirien et, pour certains dossiers, dans la sous-région ouest-africaine."}},
    {"@type":"Question","name":"Travaillez-vous avec les particuliers ?","acceptedAnswer":{"@type":"Answer","text":"Oui. Particuliers, entreprises et institutions font partie de notre clientèle. Les modalités d'accompagnement sont adaptées à la nature et à la taille du dossier."}},
    {"@type":"Question","name":"Comment se passe un premier échange ?","acceptedAnswer":{"@type":"Answer","text":"Le premier échange est un diagnostic sans engagement. Nous qualifions votre besoin, identifions le pôle compétent et vous remettons une proposition écrite précisant le périmètre, les délais et les conditions."}},
    {"@type":"Question","name":"Sous quel délai obtient-on une réponse ?","acceptedAnswer":{"@type":"Answer","text":"Toute demande envoyée via le site reçoit une réponse sous 24 heures ouvrées."}}
  ]
}
</script>"""


# ---------------------------------------------------------------------------
# ACCUEIL
# ---------------------------------------------------------------------------
def cartes_poles():
    out = ""
    for i, p in enumerate(POLES):
        puces = "".join(f"<li>{x}</li>" for x in p["puces"])
        out += f"""      <article class="pole reveal" data-delai="{i * 90}">
        <span class="pole__icone">{IC[p['id']]}</span>
        <h3>{p['nom']}</h3>
        <p>{p['resume']}</p>
        <ul>{puces}</ul>
        <a class="lien-fleche" href="{p['fichier']}">Découvrir le pôle {IC['fleche']}</a>
      </article>
"""
    return out


ACCUEIL = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero__grille">
      <div>
        <p class="eyebrow">Groupe multiservices — {VILLE}</p>
        <h1>Construire l'avenir,<span class="or">sécuriser le présent.</span></h1>
        <p class="hero__intro">
          Quatre métiers réunis dans une seule structure : l'immobilier pour bâtir,
          le juridique pour sécuriser, le recouvrement pour préserver votre trésorerie,
          la logistique pour fluidifier vos opérations. Un seul interlocuteur, une
          responsabilité entière.
        </p>
        <div class="btn-groupe">
          <a class="btn btn--or" href="contact.html">Parler de votre projet</a>
          <a class="btn btn--ligne" href="#poles">Voir nos quatre pôles</a>
        </div>
        <div class="hero__poles">
          <span>Immobilier</span><span>Juridique</span>
          <span>Recouvrement</span><span>Logistique</span>
        </div>
      </div>

      <aside class="hero__cadre">
        <span class="marque" style="width:92px;display:block">{MARQUE}</span>
        <h2>Un groupe, quatre expertises</h2>
        <p>Nos clients ne juxtaposent plus des prestataires : ils traitent avec une
           structure unique qui répond de l'ensemble de la chaîne.</p>
        <dl>
          <div>
            <dt><span data-compteur="4">4</span></dt>
            <dd>pôles d'activité intégrés</dd>
          </div>
          <div>
            <dt><span data-compteur="24" data-suffixe=" h">24 h</span></dt>
            <dd>délai de réponse ouvré</dd>
          </div>
        </dl>
      </aside>
    </div>
  </div>
</section>

<section class="reperes">
  <div class="wrap">
    <div class="reperes__grille">
      <div class="repere">
        <strong data-compteur="120" data-suffixe="+">120+</strong>
        <span>Dossiers accompagnés</span>
      </div>
      <div class="repere">
        <strong data-compteur="4">4</strong>
        <span>Pôles d'expertise</span>
      </div>
      <div class="repere">
        <strong data-compteur="95" data-suffixe=" %">95 %</strong>
        <span>Clients reconduits</span>
      </div>
      <div class="repere">
        <strong data-compteur="24" data-suffixe=" h">24 h</strong>
        <span>Délai de réponse</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="duo">
      <div class="reveal">
        <p class="eyebrow">Le groupe</p>
        <h2>Un partenaire de confiance pour bâtir, sécuriser et développer</h2>
        <hr class="filet">
        <p>Dans un environnement économique exigeant, {SOCIETE} se positionne comme un
           partenaire de confiance pour les entreprises, les institutions et les
           particuliers. Le groupe apporte une réponse globale à des besoins essentiels :
           bâtir, sécuriser, recouvrer, transporter et organiser.</p>
        <p>Cette réunion d'expertises complémentaires au sein d'une même structure n'est pas
           une commodité administrative. C'est ce qui nous permet de voir un dossier dans son
           entier — le terrain, le titre, la créance, la livraison — là où des prestataires
           séparés ne voient chacun qu'un fragment.</p>
        <div class="btn-groupe" style="margin-top:30px">
          <a class="btn btn--bleu" href="groupe.html">Découvrir le groupe</a>
        </div>
      </div>
      <div class="reveal" data-delai="120">
        <div class="encart">
          <h4>Notre promesse</h4>
          <p>Des services intégrés, fiables et performants pour accompagner durablement
             la croissance de nos clients.</p>
        </div>
        <div class="encart">
          <h4>Notre territoire</h4>
          <p>Immobilier, affaires juridiques et administratives, recouvrement, transport
             et logistique — en Côte d'Ivoire et dans la sous-région ouest-africaine.</p>
        </div>
        <div class="encart">
          <h4>Nos interlocuteurs</h4>
          <p>Particuliers, entreprises, investisseurs, institutions, promoteurs,
             propriétaires et créanciers.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--gris" id="poles">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Architecture des activités</p>
      <h2>Quatre pôles, une seule responsabilité</h2>
      <hr class="filet">
      <p>Chaque pôle est autonome et peut intervenir seul. Ensemble, ils couvrent
         l'essentiel de ce qui fait avancer ou bloquer un projet.</p>
    </div>
    <div class="grille grille--4">
{cartes_poles()}    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Pourquoi {SOCIETE}</p>
      <h2>La différence d'un groupe intégré</h2>
      <hr class="filet">
      <p>Le même dossier, traité de deux façons.</p>
    </div>
    <div class="compare reveal">
      <div class="compare__col compare__col--avant">
        <h3>Avec des prestataires séparés</h3>
        <ul>
          <li>{IC['croix']}<span>Chaque intervenant découvre le dossier depuis le début.</span></li>
          <li>{IC['croix']}<span>Les délais s'additionnent au lieu de se recouvrir.</span></li>
          <li>{IC['croix']}<span>Personne ne répond du résultat d'ensemble.</span></li>
          <li>{IC['croix']}<span>Les informations transitent par vous, à vos risques.</span></li>
          <li>{IC['croix']}<span>Un blocage juridique arrête tout le projet immobilier.</span></li>
        </ul>
      </div>
      <div class="compare__col compare__col--apres">
        <h3>Avec {SOCIETE}</h3>
        <ul>
          <li>{IC['check']}<span>Un dossier unique, partagé entre les pôles concernés.</span></li>
          <li>{IC['check']}<span>Les travaux avancent en parallèle dès que possible.</span></li>
          <li>{IC['check']}<span>Un interlocuteur unique, responsable du résultat.</span></li>
          <li>{IC['check']}<span>La circulation de l'information est notre charge, pas la vôtre.</span></li>
          <li>{IC['check']}<span>Le blocage est anticipé par le pôle compétent, en amont.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--gris">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Notre méthode</p>
      <h2>Quatre étapes, dans cet ordre</h2>
      <hr class="filet">
      <p>La séquence compte : nous ne proposons rien avant d'avoir compris, et nous
         n'engageons rien avant d'avoir écrit.</p>
    </div>
    <div class="etapes">
      <div class="etape reveal">
        <span class="etape__num">01</span>
        <h3>Écoute</h3>
        <p>Un premier échange, sans engagement, pour comprendre votre situation réelle
           et pas seulement la demande formulée.</p>
      </div>
      <div class="etape reveal" data-delai="90">
        <span class="etape__num">02</span>
        <h3>Diagnostic</h3>
        <p>Nous qualifions le dossier, identifions les risques et le ou les pôles
           compétents, puis remettons une proposition écrite.</p>
      </div>
      <div class="etape reveal" data-delai="180">
        <span class="etape__num">03</span>
        <h3>Exécution</h3>
        <p>Un chef de dossier unique pilote l'intervention et coordonne les pôles
           mobilisés jusqu'à l'aboutissement.</p>
      </div>
      <div class="etape reveal" data-delai="270">
        <span class="etape__num">04</span>
        <h3>Suivi</h3>
        <p>Un point d'avancement régulier, un dossier archivé et traçable, et un
           accompagnement au-delà de la livraison.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Valeurs fondamentales</p>
      <h2>Ce sur quoi nous ne transigeons pas</h2>
      <hr class="filet">
    </div>
    <div class="grille grille--3">
      <div class="valeur reveal"><h4>Excellence</h4><p>La recherche constante d'un service de qualité, mesurée sur le résultat livré et non sur l'effort fourni.</p></div>
      <div class="valeur reveal" data-delai="70"><h4>Intégrité</h4><p>La transparence et le respect des engagements, y compris quand ils nous coûtent.</p></div>
      <div class="valeur reveal" data-delai="140"><h4>Professionnalisme</h4><p>Une méthode rigoureuse et orientée résultats, documentée à chaque étape.</p></div>
      <div class="valeur reveal" data-delai="210"><h4>Innovation</h4><p>Des solutions adaptées aux nouveaux usages et aux réalités du marché local.</p></div>
      <div class="valeur reveal" data-delai="280"><h4>Engagement</h4><p>Une implication durable auprès des clients, au-delà de la mission ponctuelle.</p></div>
      <div class="valeur reveal" data-delai="350"><h4>Proximité</h4><p>Une connaissance du terrain ivoirien qui change les délais et les décisions.</p></div>
    </div>
  </div>
</section>

<section class="section invest">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Espace investisseurs</p>
      <h2>Un modèle diversifié sur un marché en croissance</h2>
      <hr class="filet">
      <p>Quatre sources de revenus décorrélées, un ancrage à Abidjan et une trajectoire
         d'expansion vers la sous-région ouest-africaine.</p>
    </div>
    <div class="invest__chiffres">
      <div class="invest__chiffre reveal">
        <strong>4</strong>
        <span>lignes d'activité indépendantes, qui amortissent les cycles propres à chaque secteur.</span>
      </div>
      <div class="invest__chiffre reveal" data-delai="90">
        <strong>UEMOA</strong>
        <span>un cadre réglementaire commun à huit pays, qui rend la réplication du modèle possible.</span>
      </div>
      <div class="invest__chiffre reveal" data-delai="180">
        <strong>B2B + B2C</strong>
        <span>une base de clients mixte : entreprises, institutions et particuliers.</span>
      </div>
    </div>
    <div class="btn-groupe">
      <a class="btn btn--or" href="investisseurs.html">Consulter le dossier investisseurs</a>
      <a class="btn btn--ligne" href="contact.html?pole=investisseur">Prendre contact</a>
    </div>
  </div>
</section>

<section class="section section--gris" id="president">
  <div class="wrap">
    <div class="president">
      <div class="president__carte reveal">
        <span class="marque" style="width:96px;margin:0 auto 26px;display:block">{MARQUE}</span>
        <strong>ADOUKO GÉRARD</strong>
        <span>Président Directeur Général</span>
      </div>
      <div class="president__texte reveal" data-delai="120">
        <p class="eyebrow">Mot du Président</p>
        <p>Dans un environnement économique en constante évolution, les entreprises et les
           particuliers ont besoin de partenaires fiables, capables de les accompagner avec
           professionnalisme, rigueur et efficacité. C'est dans cette vision qu'{SOCIETE}
           a été créé.</p>
        <p>Notre ambition est de proposer des solutions intégrées et performantes dans les
           domaines de l'immobilier, des affaires juridiques et administratives, du
           recouvrement ainsi que du transport et de la logistique. Chez {SOCIETE}, nous
           croyons que la confiance se construit par la qualité du travail accompli, la
           transparence dans nos engagements et la satisfaction de nos partenaires.</p>
        <p class="president__signature">
          Adouko Gérard
          <small>Président Directeur Général, {SOCIETE}</small>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Questions fréquentes</p>
      <h2>Ce qu'on nous demande avant de nous confier un dossier</h2>
      <hr class="filet">
    </div>
    <div class="faq reveal">
      <details>
        <summary>Faut-il faire appel à plusieurs pôles à la fois ?</summary>
        <p>Non. Chaque pôle intervient de façon autonome et se suffit à lui-même.
           L'intérêt du groupe est de pouvoir mobiliser les autres compétences si votre
           dossier l'exige, sans que vous ayez à chercher un nouveau prestataire ni à
           réexpliquer votre situation.</p>
      </details>
      <details>
        <summary>Intervenez-vous en dehors d'Abidjan ?</summary>
        <p>Oui. Nos équipes interviennent sur l'ensemble du territoire ivoirien et, pour
           certains dossiers, dans la sous-région ouest-africaine. Les modalités et délais
           sont précisés dans la proposition écrite.</p>
      </details>
      <details>
        <summary>Travaillez-vous avec les particuliers ?</summary>
        <p>Oui. Particuliers, entreprises et institutions font partie de notre clientèle.
           Les modalités d'accompagnement sont adaptées à la nature et à la taille du
           dossier, pas au statut du demandeur.</p>
      </details>
      <details>
        <summary>Comment se passe un premier échange ?</summary>
        <p>Le premier échange est un diagnostic sans engagement. Nous qualifions votre
           besoin, identifions le pôle compétent et vous remettons une proposition écrite
           précisant le périmètre, les délais et les conditions.</p>
      </details>
      <details>
        <summary>Sous quel délai obtient-on une réponse ?</summary>
        <p>Toute demande envoyée via ce site reçoit une réponse sous 24 heures ouvrées.
           Pour les situations urgentes, le téléphone reste le canal le plus rapide.</p>
      </details>
    </div>
  </div>
</section>

{cta_final(
    "Parlons de votre projet.",
    "Un premier échange suffit souvent à savoir si nous sommes le bon partenaire. "
    "Il est sans engagement et vous repartez avec un avis clair."
)}
"""


# ---------------------------------------------------------------------------
# LE GROUPE
# ---------------------------------------------------------------------------
GROUPE = f"""
{page_tete(['<a href="index.html">Accueil</a>', 'Le Groupe'],
           'Un groupe d\'expertise intégré, né d\'une ambition simple',
           'Réunir, au sein d\'une même structure, des expertises complémentaires capables '
           'de répondre aux défis concrets des organisations.')}

<section class="section">
  <div class="wrap">
    <div class="duo duo--haut">
      <div class="reveal">
        <p class="eyebrow">Histoire de la marque</p>
        <h2>Une vision multiservices, structurée en quatre pôles</h2>
        <hr class="filet">
        <p>{SOCIETE} est né du constat qu'un projet échoue rarement pour une seule raison.
           Un terrain se bloque sur un titre. Une entreprise saine se fragilise sur une
           créance impayée. Une livraison manquée coûte un client. Ces problèmes relèvent
           de métiers différents, mais ils appartiennent au même dossier.</p>
        <p>Le groupe s'inscrit dans une logique de service, de proximité et de performance.
           Son histoire exprime la solidité d'une structure qui accompagne la réalisation
           des projets immobiliers, la sécurisation administrative et juridique, la maîtrise
           des créances et la fluidité des opérations logistiques.</p>
      </div>
      <div class="reveal" data-delai="120">
        <div class="encart">
          <h4>Origine</h4>
          <p>Une vision multiservices : rassembler ce que le marché traitait en silos.</p>
        </div>
        <div class="encart">
          <h4>Structuration</h4>
          <p>Quatre pôles complémentaires, chacun autonome, tous coordonnés.</p>
        </div>
        <div class="encart">
          <h4>Expansion</h4>
          <p>Devenir un partenaire de référence en Côte d'Ivoire, puis en Afrique de l'Ouest.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sombre">
  <div class="wrap">
    <div class="grille grille--2">
      <div class="reveal">
        <p class="eyebrow">Vision</p>
        <h2 style="font-size:1.7rem">Devenir un groupe multiservices de référence</h2>
        <p>En Côte d'Ivoire et en Afrique de l'Ouest, reconnu pour la qualité de son
           accompagnement, la fiabilité de ses services et sa capacité à créer de la
           valeur durable.</p>
      </div>
      <div class="reveal" data-delai="120">
        <p class="eyebrow">Mission</p>
        <h2 style="font-size:1.7rem">Accompagner à chaque étape du projet</h2>
        <p>Particuliers, entreprises et institutions, grâce à des services intégrés,
           sécurisés, performants et adaptés aux réalités du marché.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="valeurs">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Valeurs fondamentales</p>
      <h2>Cinq valeurs, appliquées au quotidien</h2>
      <hr class="filet">
    </div>
    <div class="grille grille--3">
      <div class="valeur reveal"><h4>Excellence</h4><p>La recherche constante d'un service de qualité.</p></div>
      <div class="valeur reveal" data-delai="70"><h4>Intégrité</h4><p>La transparence et le respect des engagements.</p></div>
      <div class="valeur reveal" data-delai="140"><h4>Professionnalisme</h4><p>Une méthode rigoureuse et orientée résultats.</p></div>
      <div class="valeur reveal" data-delai="210"><h4>Innovation</h4><p>Des solutions adaptées aux nouveaux usages.</p></div>
      <div class="valeur reveal" data-delai="280"><h4>Engagement</h4><p>Une implication durable auprès des clients.</p></div>
    </div>
  </div>
</section>

<section class="section section--gris">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">ADN de marque</p>
      <h2>Cinq piliers qui guident chaque décision</h2>
      <hr class="filet">
      <p>Ils orientent l'expérience client, le ton de nos échanges et l'exécution
         opérationnelle.</p>
    </div>
    <div class="grille grille--3">
      <div class="valeur reveal"><h4>Confiance</h4><p>Rassurer par la clarté : pas d'engagement oral, pas de zone d'ombre.</p></div>
      <div class="valeur reveal" data-delai="70"><h4>Sécurité</h4><p>Protéger les intérêts de nos clients, en amont plutôt qu'en réparation.</p></div>
      <div class="valeur reveal" data-delai="140"><h4>Croissance</h4><p>Accompagner la réussite, pas seulement exécuter une prestation.</p></div>
      <div class="valeur reveal" data-delai="210"><h4>Efficacité</h4><p>Réduire les contraintes : moins d'interlocuteurs, moins de délais morts.</p></div>
      <div class="valeur reveal" data-delai="280"><h4>Proximité</h4><p>Comprendre le terrain, ses usages et ses circuits réels.</p></div>
    </div>
  </div>
</section>

<section class="section" id="president">
  <div class="wrap">
    <div class="president">
      <div class="president__carte reveal">
        <span class="marque" style="width:96px;margin:0 auto 26px;display:block">{MARQUE}</span>
        <strong>ADOUKO GÉRARD</strong>
        <span>Président Directeur Général</span>
      </div>
      <div class="president__texte reveal" data-delai="120">
        <p class="eyebrow">Mot du Président</p>
        <p>Bienvenue chez {SOCIETE}.</p>
        <p>Dans un environnement économique en constante évolution, les entreprises et les
           particuliers ont besoin de partenaires fiables, capables de les accompagner avec
           professionnalisme, rigueur et efficacité. C'est dans cette vision qu'{SOCIETE}
           a été créé.</p>
        <p>Notre ambition est de proposer des solutions intégrées et performantes dans les
           domaines de l'immobilier, des affaires juridiques et administratives, du
           recouvrement ainsi que du transport et de la logistique. Chez {SOCIETE}, nous
           croyons que la confiance se construit par la qualité du travail accompli, la
           transparence dans nos engagements et la satisfaction de nos partenaires.</p>
        <p class="president__signature">
          Adouko Gérard
          <small>Président Directeur Général, {SOCIETE}</small>
        </p>
      </div>
    </div>
  </div>
</section>

{cta_final("Une question sur le groupe ?",
           "Nos équipes répondent sous 24 heures ouvrées, en français, depuis Abidjan.",
           ("contact.html", "Nous écrire"), ("index.html#poles", "Voir les pôles"))}
"""


# ---------------------------------------------------------------------------
# PAGES DE PÔLES
# ---------------------------------------------------------------------------
CONTENU_POLES = {
    "immobilier": {
        "titre": "Pôle Immobilier — bâtir et valoriser votre patrimoine",
        "chapo": "Vente, location, gestion, promotion, lotissement, expertise et construction. "
                 "Le pôle qui porte la dimension de bâtisseur et de créateur de valeur durable.",
        "intro": [
            "Le pôle Immobilier accompagne ses clients sur toute la durée de vie d'un bien : "
            "l'acquisition, la sécurisation du titre, la valorisation, la mise en exploitation "
            "et la transmission. Il s'adresse autant au particulier qui achète son premier "
            "terrain qu'au promoteur qui structure une opération de lotissement.",
            "En Côte d'Ivoire, la valeur d'un bien tient autant à son emplacement qu'à la "
            "solidité de son dossier. C'est précisément là que l'appartenance au groupe change "
            "la donne : le pôle Juridique intervient sur les titres et les formalités avant "
            "que le problème ne se transforme en contentieux.",
        ],
        "prestations": [
            ("Vente et acquisition", "Recherche, négociation, accompagnement jusqu'à la signature."),
            ("Location et gestion locative", "Sélection des locataires, quittancement, suivi des impayés."),
            ("Promotion immobilière", "Montage d'opérations, coordination des intervenants, commercialisation."),
            ("Lotissement", "Découpage, viabilisation, constitution des dossiers administratifs."),
            ("Expertise immobilière", "Évaluation de la valeur vénale et locative, audit de conformité."),
            ("Construction et suivi de chantier", "Pilotage des travaux, contrôle des délais et de la qualité."),
            ("Gestion de patrimoine", "Arbitrage, valorisation et structuration d'un portefeuille de biens."),
            ("Syndic et administration de biens", "Gestion des parties communes, charges et assemblées."),
        ],
        "pour_qui": [
            "Particuliers cherchant à acquérir, louer ou valoriser un bien",
            "Propriétaires souhaitant déléguer la gestion de leur patrimoine",
            "Promoteurs et investisseurs structurant une opération",
            "Entreprises et institutions gérant un parc immobilier",
        ],
        "croise": ("juridique", "Titres fonciers, baux et formalités sont sécurisés en amont "
                                "par le pôle Juridique & Administratif."),
    },
    "juridique": {
        "titre": "Pôle Juridique & Administratif — sécuriser vos démarches",
        "chapo": "Conseil, formalités, constitution d'entreprises et accompagnement "
                 "réglementaire, dans le respect des cadres en vigueur.",
        "intro": [
            "Le pôle Affaires juridiques et administratives sécurise les démarches, les "
            "dossiers, les formalités et les engagements. Il apporte une assistance "
            "professionnelle aux entreprises, aux institutions et aux particuliers, avec un "
            "principe constant : ce qui n'est pas écrit n'existe pas.",
            "Son intervention est le plus souvent préventive. Constituer correctement une "
            "société, rédiger un bail sans ambiguïté ou vérifier un titre avant la signature "
            "coûte une fraction de ce que coûte le contentieux qui aurait suivi.",
        ],
        "prestations": [
            ("Constitution de sociétés", "Choix de la forme, statuts, immatriculation et publications."),
            ("Formalités administratives", "Déclarations, agréments, licences et mises à jour au registre."),
            ("Rédaction et revue d'actes", "Contrats, baux, protocoles, conditions générales."),
            ("Conseil juridique aux entreprises", "Accompagnement sur les décisions à effet juridique."),
            ("Accompagnement réglementaire", "Mise en conformité et veille sur les obligations applicables."),
            ("Secrétariat juridique", "Tenue des registres, assemblées, procès-verbaux."),
            ("Sécurisation foncière", "Vérification des titres, régularisations et transferts."),
            ("Assistance dans les relations avec l'administration", "Suivi des dossiers auprès des services compétents."),
        ],
        "pour_qui": [
            "Entrepreneurs créant ou restructurant leur société",
            "PME sans direction juridique interne",
            "Institutions et associations soumises à des obligations déclaratives",
            "Particuliers engagés dans une démarche foncière ou successorale",
        ],
        "croise": ("recouvrement", "Lorsqu'une créance devient contentieuse, le passage au pôle "
                                   "Recouvrement se fait sans perte d'information."),
    },
    "recouvrement": {
        "titre": "Pôle Recouvrement — préserver votre trésorerie",
        "chapo": "Recouvrement amiable et contentieux, négociation responsable, traçabilité "
                 "et protection des intérêts économiques.",
        "intro": [
            "Le pôle Recouvrement aide les organisations à préserver leur trésorerie par des "
            "démarches amiables ou contentieuses structurées. Une créance impayée n'est pas "
            "seulement une perte comptable : c'est un besoin en fonds de roulement financé "
            "par l'entreprise elle-même.",
            "Notre approche privilégie l'issue amiable. Dans la majorité des dossiers, le "
            "débiteur n'est pas de mauvaise foi mais en difficulté de trésorerie : un "
            "échéancier réaliste et suivi recouvre plus, et plus vite, qu'une procédure "
            "engagée trop tôt. Le contentieux reste disponible, comme une étape, pas comme "
            "un réflexe.",
        ],
        "prestations": [
            ("Recouvrement amiable", "Relances graduées, mise en demeure, négociation directe."),
            ("Recouvrement contentieux", "Constitution du dossier et suivi de la procédure."),
            ("Négociation et échéanciers", "Accords écrits, suivis et sécurisés juridiquement."),
            ("Analyse du portefeuille de créances", "Segmentation par ancienneté et probabilité de recouvrement."),
            ("Prévention du risque client", "Vérification en amont et conditions de paiement adaptées."),
            ("Reporting et traçabilité", "Historique complet des diligences sur chaque dossier."),
            ("Recouvrement de loyers", "Traitement des impayés locatifs, en lien avec le pôle Immobilier."),
            ("Assistance au précontentieux", "Préparation des pièces avant toute action judiciaire."),
        ],
        "pour_qui": [
            "PME dont les délais de paiement pèsent sur la trésorerie",
            "Bailleurs confrontés à des loyers impayés",
            "Prestataires de services à facturation récurrente",
            "Institutions gérant des créances de nature diverse",
        ],
        "croise": ("juridique", "Les procédures et les actes sont pris en charge par le pôle "
                                "Juridique & Administratif, sans prestataire supplémentaire."),
    },
    "logistique": {
        "titre": "Pôle Transport & Logistique — fluidifier vos opérations",
        "chapo": "Transport, distribution, gestion de flotte, logistique intégrée et suivi "
                 "opérationnel. La maîtrise du terrain et la fiabilité du service.",
        "intro": [
            "Le pôle Transport et Logistique accompagne la circulation des biens, la "
            "distribution, la gestion de flotte et la coordination opérationnelle. Il reflète "
            "la maîtrise du terrain, la rapidité d'exécution et la fiabilité du service.",
            "À Abidjan comme à l'intérieur du pays, la performance logistique se joue moins "
            "sur la distance que sur la connaissance des circuits réels : l'état des axes, "
            "les créneaux portuaires, les points de rupture. C'est cette connaissance qui "
            "sépare une livraison annoncée d'une livraison tenue.",
        ],
        "prestations": [
            ("Transport de marchandises", "Enlèvement, acheminement et livraison sur le territoire."),
            ("Distribution", "Livraison multi-points et tournées organisées."),
            ("Gestion de flotte", "Affectation, entretien, suivi de l'utilisation des véhicules."),
            ("Logistique intégrée", "Coordination de bout en bout, du fournisseur au client final."),
            ("Suivi opérationnel", "Points d'étape et information en cas d'aléa, pas après."),
            ("Transport pour compte de tiers", "Mise à disposition de moyens pour vos opérations."),
            ("Coordination des enlèvements", "Organisation des retraits et gestion des créneaux."),
            ("Reporting d'exploitation", "Indicateurs de ponctualité et de conformité des livraisons."),
        ],
        "pour_qui": [
            "Distributeurs et commerçants approvisionnant plusieurs points de vente",
            "Industriels et importateurs organisant leurs flux",
            "Entreprises souhaitant externaliser leur flotte",
            "Institutions et ONG avec des besoins d'acheminement ponctuels",
        ],
        "croise": ("juridique", "Contrats de transport, assurances et responsabilités sont "
                                "cadrés par le pôle Juridique & Administratif."),
    },
}


def page_pole(pid):
    p = POLE_PAR_ID[pid]
    c = CONTENU_POLES[pid]
    autres = [x for x in POLES if x["id"] != pid]

    intro = "".join(f"<p>{t}</p>" for t in c["intro"])
    prest = "".join(
        f'<li>{IC["check"]}<span><strong>{t}</strong>{d}</span></li>'
        for t, d in c["prestations"]
    )
    qui = "".join(f"<li>{x}</li>" for x in c["pour_qui"])
    croise_pole = POLE_PAR_ID[c["croise"][0]]
    autres_cartes = "".join(
        f"""      <article class="pole reveal">
        <span class="pole__icone">{IC[a['id']]}</span>
        <h3>{a['nom']}</h3>
        <p>{a['accroche']}</p>
        <a class="lien-fleche" href="{a['fichier']}">Découvrir {IC['fleche']}</a>
      </article>
"""
        for a in autres
    )

    jsonld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{p['nom']}",
  "provider": {{"@type": "Organization", "name": "{SOCIETE}", "url": "{SITE_URL}"}},
  "areaServed": {{"@type": "Country", "name": "Côte d'Ivoire"}},
  "description": "{c['chapo']}"
}}
</script>"""

    corps = f"""
{page_tete(['<a href="index.html">Accueil</a>', '<a href="index.html#poles">Nos pôles</a>', p['nom']],
           c['titre'], c['chapo'])}

<section class="section">
  <div class="wrap">
    <div class="duo duo--haut">
      <div class="prose reveal">
        <p class="eyebrow">{p['verbe']}</p>
        <h2>Ce que fait ce pôle</h2>
        <hr class="filet">
        {intro}
      </div>
      <div class="reveal" data-delai="120">
        <div class="encart">
          <h4>Pour qui</h4>
          <ul style="margin:0;padding-left:1.1em;font-size:.95rem;color:var(--gris-texte)">{qui}</ul>
        </div>
        <div class="encart">
          <h4>L'avantage du groupe</h4>
          <p>{c['croise'][1]} <a href="{croise_pole['fichier']}">Voir le pôle {croise_pole['nom']}</a>.</p>
        </div>
        <div class="btn-groupe" style="margin-top:24px">
          <a class="btn btn--or" href="contact.html?pole={pid}">Demander une étude</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--gris">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Prestations</p>
      <h2>Le détail de nos interventions</h2>
      <hr class="filet">
    </div>
    <ul class="prestations reveal">{prest}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Notre méthode</p>
      <h2>Comment nous traitons un dossier</h2>
      <hr class="filet">
    </div>
    <div class="etapes">
      <div class="etape reveal"><span class="etape__num">01</span><h3>Écoute</h3><p>Un échange sans engagement pour cerner la situation réelle.</p></div>
      <div class="etape reveal" data-delai="90"><span class="etape__num">02</span><h3>Diagnostic</h3><p>Qualification du dossier et proposition écrite chiffrée.</p></div>
      <div class="etape reveal" data-delai="180"><span class="etape__num">03</span><h3>Exécution</h3><p>Un chef de dossier unique pilote l'intervention.</p></div>
      <div class="etape reveal" data-delai="270"><span class="etape__num">04</span><h3>Suivi</h3><p>Points d'avancement réguliers et dossier traçable.</p></div>
    </div>
  </div>
</section>

<section class="section section--gris">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Les autres pôles</p>
      <h2>Une expertise n'arrive jamais seule</h2>
      <hr class="filet">
    </div>
    <div class="grille grille--3">
{autres_cartes}    </div>
  </div>
</section>

{cta_final(f"Un dossier {p['nom'].lower()} à traiter ?",
           "Décrivez-nous votre situation. Nous vous rappelons sous 24 heures ouvrées "
           "avec un premier avis.",
           ("contact.html?pole=" + pid, "Demander une étude"),
           ("index.html#poles", "Voir tous les pôles"))}
"""
    return head(f"{p['nom']} — {SOCIETE}", c["chapo"][:157], p["fichier"], jsonld=jsonld) \
        + entete() + corps + pied()


# ---------------------------------------------------------------------------
# INVESTISSEURS
# ---------------------------------------------------------------------------
INVESTISSEURS = f"""
{page_tete(['<a href="index.html">Accueil</a>', 'Investisseurs'],
           'Un modèle multiservices, un marché en construction',
           'Quatre lignes d\'activité décorrélées, un ancrage abidjanais et une trajectoire '
           'd\'expansion vers l\'espace UEMOA.')}

<section class="section">
  <div class="wrap wrap--etroit prose reveal">
    <p class="eyebrow">Thèse d'investissement</p>
    <h2>Pourquoi ce modèle</h2>
    <hr class="filet">
    <p>{SOCIETE} repose sur une conviction simple : en Afrique de l'Ouest, les entreprises
       et les particuliers ne manquent pas de prestataires, ils manquent d'interlocuteurs
       capables de traiter un dossier de bout en bout. La fragmentation du marché des
       services professionnels crée un coût de coordination que le client paie sans le
       mesurer — en délais, en allers-retours et en risques non couverts.</p>
    <p>Le groupe capte cette valeur en internalisant la coordination. Chaque pôle est
       viable seul ; ensemble, ils produisent un effet de rétention que peu d'acteurs
       locaux peuvent reproduire à court terme.</p>
  </div>
</section>

<section class="section section--sombre">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Structure du modèle</p>
      <h2>Quatre moteurs, des cycles différents</h2>
      <hr class="filet">
      <p>La diversification n'est pas cosmétique : les cycles de l'immobilier, du droit
         des affaires, du recouvrement et de la logistique ne se retournent pas en même
         temps.</p>
    </div>
    <div class="grille grille--2">
      <div class="encart reveal">
        <h4>Immobilier — capital et récurrence</h4>
        <p>Revenus de transaction (ponctuels, à forte valeur) complétés par la gestion
           locative, qui génère des honoraires récurrents et prévisibles.</p>
      </div>
      <div class="encart reveal" data-delai="80">
        <h4>Juridique — récurrence et amorçage</h4>
        <p>La constitution de sociétés est une porte d'entrée à faible coût d'acquisition ;
           le secrétariat juridique et la conformité fidélisent ensuite dans la durée.</p>
      </div>
      <div class="encart reveal" data-delai="160">
        <h4>Recouvrement — contracyclique</h4>
        <p>L'activité progresse quand la conjoncture se tend et que les délais de paiement
           s'allongent. Elle amortit mécaniquement les cycles bas des autres pôles.</p>
      </div>
      <div class="encart reveal" data-delai="240">
        <h4>Logistique — volume et actifs</h4>
        <p>Marges unitaires plus faibles mais volumes réguliers, et constitution
           progressive d'une flotte qui devient un actif au bilan.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Marché</p>
      <h2>Le contexte ivoirien et sous-régional</h2>
      <hr class="filet">
    </div>
    <div class="grille grille--3">
      <div class="valeur reveal">
        <h4>Formalisation</h4>
        <p>La structuration progressive du tissu économique ivoirien élargit
           mécaniquement la demande de services juridiques et administratifs formalisés.</p>
      </div>
      <div class="valeur reveal" data-delai="80">
        <h4>Urbanisation</h4>
        <p>La pression foncière sur le Grand Abidjan soutient durablement la demande en
           transaction, gestion et sécurisation immobilière.</p>
      </div>
      <div class="valeur reveal" data-delai="160">
        <h4>Espace UEMOA</h4>
        <p>Un cadre juridique et monétaire partagé par huit pays, qui rend la réplication
           du modèle possible sans reconstruction complète.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--gris">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Trajectoire</p>
      <h2>Nos axes de développement</h2>
      <hr class="filet">
      <p>L'ordre importe : nous consolidons avant d'étendre.</p>
    </div>
    <div class="etapes">
      <div class="etape reveal">
        <span class="etape__num">01</span>
        <h3>Consolider Abidjan</h3>
        <p>Densifier la base de clients sur le district autonome et industrialiser les
           processus de chaque pôle.</p>
      </div>
      <div class="etape reveal" data-delai="90">
        <span class="etape__num">02</span>
        <h3>Outiller</h3>
        <p>Digitaliser le suivi des dossiers pour rendre la coordination inter-pôles
           mesurable et reproductible.</p>
      </div>
      <div class="etape reveal" data-delai="180">
        <span class="etape__num">03</span>
        <h3>Couvrir le territoire</h3>
        <p>Étendre la couverture aux principaux pôles économiques du pays, en priorité
           sur les métiers les moins capitalistiques.</p>
      </div>
      <div class="etape reveal" data-delai="270">
        <span class="etape__num">04</span>
        <h3>Franchir la frontière</h3>
        <p>Répliquer le modèle dans l'espace UEMOA, en commençant par les marchés au
           cadre réglementaire le plus proche.</p>
      </div>
    </div>
  </div>
</section>

<section class="section invest">
  <div class="wrap">
    <div class="titre-bloc reveal">
      <p class="eyebrow">Gouvernance</p>
      <h2>Ce sur quoi un investisseur peut s'appuyer</h2>
      <hr class="filet">
    </div>
    <div class="grille grille--2">
      <div class="encart reveal">
        <h4>Direction identifiée</h4>
        <p>Le groupe est dirigé par son Président Directeur Général, Adouko Gérard, qui
           porte la vision multiservices depuis l'origine.</p>
      </div>
      <div class="encart reveal" data-delai="80">
        <h4>Traçabilité des dossiers</h4>
        <p>Chaque intervention est documentée de l'écoute au suivi, ce qui rend l'activité
           auditable et la performance mesurable.</p>
      </div>
      <div class="encart reveal" data-delai="160">
        <h4>Cadre réglementaire respecté</h4>
        <p>Les activités sont exercées dans le respect des cadres ivoiriens applicables à
           chaque métier.</p>
      </div>
      <div class="encart reveal" data-delai="240">
        <h4>Documentation sur demande</h4>
        <p>États financiers, structure du capital et projections sont communiqués aux
           investisseurs qualifiés, après prise de contact.</p>
      </div>
    </div>
    <div class="btn-groupe" style="margin-top:44px">
      <a class="btn btn--or" href="contact.html?pole=investisseur">Demander le dossier complet</a>
      <a class="btn btn--ligne" href="tel:{TEL_URI}">Appeler la direction</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--etroit reveal">
    <p style="font-size:.86rem;color:var(--gris-texte);border-left:3px solid var(--gris-bord);padding-left:20px">
      Les informations présentées sur cette page ont une vocation générale d'information
      sur l'activité et la stratégie du groupe. Elles ne constituent ni une offre au public,
      ni une sollicitation d'investissement, ni un conseil en investissement. Toute
      documentation financière est transmise sur demande, dans un cadre contractuel défini.
    </p>
  </div>
</section>

{cta_final("Entrons en relation.",
           "Nous répondons aux investisseurs sous 24 heures ouvrées et organisons un "
           "premier entretien à Abidjan ou en visioconférence.",
           ("contact.html?pole=investisseur", "Prendre contact"),
           ("groupe.html", "Découvrir le groupe"))}
"""


# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------
options_pole = "".join(
    f'<option value="{p["id"]}">{p["nom"]}</option>' for p in POLES
)

CONTACT = f"""
{page_tete(['<a href="index.html">Accueil</a>', 'Contact'],
           'Parlons de votre projet',
           'Décrivez votre situation en quelques lignes. Nous identifions le pôle compétent '
           'et revenons vers vous sous 24 heures ouvrées.')}

<section class="section">
  <div class="wrap">
    <div class="form-bloc">
      <div class="reveal">
        <p class="eyebrow">Formulaire</p>
        <h2>Votre demande</h2>
        <hr class="filet">
        <p style="color:var(--gris-texte);margin-bottom:34px">
          Les champs marqués d'un astérisque sont nécessaires pour vous répondre.
        </p>

        <form class="form" action="contact.php" method="post" data-ajax novalidate>
          <div class="form__retour" role="status" aria-live="polite"></div>

          <div class="champ champ--duo">
            <div class="champ">
              <label for="nom">Nom et prénoms <span class="req">*</span></label>
              <input type="text" id="nom" name="nom" required autocomplete="name" maxlength="120">
            </div>
            <div class="champ">
              <label for="societe">Société ou organisation</label>
              <input type="text" id="societe" name="societe" autocomplete="organization" maxlength="120">
            </div>
          </div>

          <div class="champ champ--duo">
            <div class="champ">
              <label for="email">Adresse e-mail <span class="req">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email" maxlength="160">
            </div>
            <div class="champ">
              <label for="telephone">Téléphone <span class="req">*</span></label>
              <input type="tel" id="telephone" name="telephone" required autocomplete="tel" maxlength="40">
            </div>
          </div>

          <div class="champ">
            <label for="pole">Votre demande concerne <span class="req">*</span></label>
            <select id="pole" name="pole" required>
              <option value="">— Sélectionnez —</option>
              {options_pole}
              <option value="investisseur">Une demande d'investisseur</option>
              <option value="autre">Autre / je ne sais pas encore</option>
            </select>
          </div>

          <div class="champ">
            <label for="message">Votre message <span class="req">*</span></label>
            <textarea id="message" name="message" required maxlength="4000"
              placeholder="Décrivez votre situation, l'échéance souhaitée et tout élément utile."></textarea>
          </div>

          <!-- Champ anti-robot : laissé vide par les humains -->
          <div style="position:absolute;left:-9999px" aria-hidden="true">
            <label for="societe_web">Ne pas remplir</label>
            <input type="text" id="societe_web" name="societe_web" tabindex="-1" autocomplete="off">
          </div>

          <label class="form__rgpd">
            <input type="checkbox" name="consentement" required>
            <span>J'accepte que mes informations soient utilisées pour traiter ma demande,
              conformément à la <a href="confidentialite.html">politique de confidentialité</a>.</span>
          </label>

          <div>
            <button class="btn btn--or" type="submit">Envoyer ma demande</button>
          </div>
        </form>
      </div>

      <aside class="coord reveal" data-delai="120">
        <h3>Nous joindre directement</h3>
        <dl>
          <div>
            <dt>Téléphone</dt>
            <dd><a href="tel:{TEL_URI}">{TEL_AFF}</a>
              <small>Du lundi au vendredi, 8 h – 18 h (GMT)</small></dd>
          </div>
          <div>
            <dt>E-mail</dt>
            <dd><a href="mailto:{EMAIL}">{EMAIL}</a>
              <small>Réponse sous 24 heures ouvrées</small></dd>
          </div>
          <div>
            <dt>Adresse</dt>
            <dd>{VILLE}
              <small>Rendez-vous sur convocation préalable</small></dd>
          </div>
          <div>
            <dt>Site</dt>
            <dd><a href="{SITE_URL}">agergroup.ci</a></dd>
          </div>
        </dl>
      </aside>
    </div>
  </div>
</section>

<section class="section section--gris">
  <div class="wrap">
    <div class="titre-bloc titre-bloc--centre reveal">
      <p class="eyebrow">Orientation</p>
      <h2>Vous savez déjà quel pôle vous concerne ?</h2>
      <hr class="filet">
    </div>
    <div class="grille grille--4">
""" + "".join(
    f"""      <article class="pole reveal">
        <span class="pole__icone">{IC[p['id']]}</span>
        <h3>{p['nom']}</h3>
        <p>{p['accroche']}</p>
        <a class="lien-fleche" href="{p['fichier']}">Voir le pôle {IC['fleche']}</a>
      </article>
"""
    for p in POLES
) + """    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# PAGES LÉGALES
# ---------------------------------------------------------------------------
MENTIONS = f"""
{page_tete(['<a href="index.html">Accueil</a>', 'Mentions légales'],
           'Mentions légales',
           'Informations relatives à l\'éditeur, à l\'hébergement et à l\'utilisation du site.')}

<section class="section">
  <div class="wrap wrap--etroit prose">
    <h2>Éditeur du site</h2>
    <p>Le présent site est édité par <strong>{SOCIETE}</strong>, société de droit ivoirien
       dont le siège est situé à {VILLE}.</p>
    <ul>
      <li>Directeur de la publication : Adouko Gérard, Président Directeur Général</li>
      <li>Téléphone : <a href="tel:{TEL_URI}">{TEL_AFF}</a></li>
      <li>E-mail : <a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>Site : <a href="{SITE_URL}">agergroup.ci</a></li>
    </ul>
    <p style="background:var(--gris-fond);padding:18px 22px;border-left:3px solid var(--or);font-size:.94rem">
      <strong>À compléter avant mise en ligne :</strong> forme juridique, montant du capital
      social, numéro RCCM, numéro de compte contribuable et adresse postale complète.
    </p>

    <h2>Hébergement</h2>
    <p>Le site est hébergé par le prestataire d'hébergement retenu par {SOCIETE}.
       Les coordonnées complètes de l'hébergeur sont à renseigner ici avant la mise en ligne.</p>

    <h2>Propriété intellectuelle</h2>
    <p>L'ensemble des éléments composant ce site — structure, textes, identité visuelle,
       logo, charte graphique, illustrations et code — est la propriété exclusive de
       {SOCIETE} ou de ses partenaires, et est protégé par les dispositions relatives au
       droit d'auteur et au droit des marques.</p>
    <p>Toute reproduction, représentation, adaptation ou exploitation, totale ou partielle,
       de ces éléments, par quelque procédé que ce soit, sans autorisation écrite préalable
       de {SOCIETE}, est interdite.</p>

    <h2>Responsabilité</h2>
    <p>{SOCIETE} s'efforce d'assurer l'exactitude et la mise à jour des informations
       diffusées sur ce site. Les contenus sont fournis à titre d'information générale et
       ne constituent pas un conseil juridique, immobilier, financier ou fiscal
       personnalisé. Seule une consultation formalisée engage la responsabilité du groupe.</p>
    <p>{SOCIETE} ne saurait être tenu responsable des dommages résultant de l'utilisation
       du site, d'une interruption de service, ou du contenu des sites tiers accessibles
       depuis des liens hypertextes.</p>

    <h2>Liens hypertextes</h2>
    <p>La mise en place d'un lien vers ce site est libre, sous réserve qu'elle ne porte pas
       atteinte à l'image du groupe et ne laisse pas supposer un partenariat inexistant.
       {SOCIETE} n'exerce aucun contrôle sur les sites vers lesquels des liens peuvent
       renvoyer.</p>

    <h2>Droit applicable</h2>
    <p>Les présentes mentions sont régies par le droit ivoirien. Tout litige relatif à
       l'utilisation du site relève de la compétence des juridictions d'Abidjan, à défaut
       de règlement amiable.</p>

    <h2>Contact</h2>
    <p>Pour toute question relative aux présentes mentions :
       <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>
"""

CONFIDENTIALITE = f"""
{page_tete(['<a href="index.html">Accueil</a>', 'Politique de confidentialité'],
           'Politique de confidentialité',
           'Quelles données nous collectons, pourquoi, combien de temps, et comment exercer '
           'vos droits.')}

<section class="section">
  <div class="wrap wrap--etroit prose">
    <h2>Notre principe</h2>
    <p>{SOCIETE} ne collecte que les données nécessaires au traitement de votre demande.
       Aucune donnée n'est vendue, louée ou cédée à des tiers à des fins commerciales.</p>

    <h2>Données collectées</h2>
    <p>Via le formulaire de contact, nous collectons : vos nom et prénoms, votre société le
       cas échéant, votre adresse e-mail, votre numéro de téléphone, le pôle concerné et le
       contenu de votre message.</p>
    <p>Les serveurs d'hébergement enregistrent par ailleurs des données techniques
       (adresse IP, date et heure d'accès) à des fins de sécurité et de bon fonctionnement.</p>

    <h2>Finalités</h2>
    <ul>
      <li>Répondre à votre demande et vous recontacter ;</li>
      <li>Qualifier votre besoin et l'orienter vers le pôle compétent ;</li>
      <li>Assurer le suivi de la relation commerciale si elle s'engage ;</li>
      <li>Garantir la sécurité et la disponibilité du site.</li>
    </ul>

    <h2>Base et consentement</h2>
    <p>Le traitement repose sur votre consentement explicite, recueilli par la case à cocher
       du formulaire, ainsi que sur l'intérêt légitime du groupe à répondre aux sollicitations
       qui lui sont adressées.</p>

    <h2>Durée de conservation</h2>
    <p>Les demandes n'ayant pas donné lieu à une relation contractuelle sont conservées
       trois ans à compter du dernier contact. Les données liées à un dossier client sont
       conservées pendant la durée de la relation, puis selon les durées légales applicables
       en matière comptable et juridique.</p>

    <h2>Destinataires</h2>
    <p>Vos données sont accessibles aux seules équipes internes d'{SOCIETE} en charge du
       traitement de votre demande, ainsi qu'à nos prestataires techniques (hébergement,
       messagerie) tenus à une obligation de confidentialité.</p>

    <h2>Sécurité</h2>
    <p>Le site est servi en HTTPS. Les accès aux données sont limités aux personnes
       habilitées. Nous appliquons des mesures raisonnables de protection contre la perte,
       l'altération et l'accès non autorisé.</p>

    <h2>Cookies</h2>
    <p>Ce site ne dépose aucun cookie publicitaire ni traceur tiers. Seuls des cookies
       strictement nécessaires au fonctionnement peuvent être utilisés. Si une solution de
       mesure d'audience est ajoutée ultérieurement, cette page sera mise à jour et votre
       consentement sera recueilli au préalable.</p>

    <h2>Vos droits</h2>
    <p>Vous disposez d'un droit d'accès, de rectification, d'effacement, d'opposition et de
       limitation du traitement de vos données. Vous pouvez également retirer votre
       consentement à tout moment.</p>
    <p>Pour exercer ces droits, écrivez à <a href="mailto:{EMAIL}">{EMAIL}</a> en précisant
       votre demande. Une réponse vous sera apportée dans un délai raisonnable.</p>
    <p>En Côte d'Ivoire, l'Autorité de Régulation des Télécommunications (ARTCI) est
       l'autorité compétente en matière de protection des données à caractère personnel.
       Vous pouvez la saisir en cas de difficulté persistante.</p>

    <h2>Modifications</h2>
    <p>Cette politique peut être mise à jour. La version en vigueur est celle publiée sur
       cette page.</p>
  </div>
</section>
"""

PLAN = f"""
{page_tete(['<a href="index.html">Accueil</a>', 'Plan du site'],
           'Plan du site',
           'Toutes les pages du site en un coup d\'œil.')}

<section class="section">
  <div class="wrap">
    <div class="grille grille--3">
      <div>
        <h3>Le groupe</h3>
        <ul style="padding-left:1.1em">
          <li><a href="index.html">Accueil</a></li>
          <li><a href="groupe.html">Le Groupe</a></li>
          <li><a href="groupe.html#valeurs">Nos valeurs</a></li>
          <li><a href="groupe.html#president">Mot du Président</a></li>
        </ul>
      </div>
      <div>
        <h3>Nos pôles</h3>
        <ul style="padding-left:1.1em">
""" + "".join(f'          <li><a href="{p["fichier"]}">{p["nom"]}</a></li>\n' for p in POLES) + f"""        </ul>
      </div>
      <div>
        <h3>Informations</h3>
        <ul style="padding-left:1.1em">
          <li><a href="investisseurs.html">Espace investisseurs</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="confidentialite.html">Politique de confidentialité</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""

ERREUR404 = f"""
<section class="erreur">
  <div class="wrap">
    <p class="erreur__code">404</p>
    <h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">Cette page n'existe pas ou plus</h1>
    <p style="max-width:520px;margin:0 auto 34px;color:var(--gris-texte)">
      Le lien est peut-être erroné, ou la page a été déplacée. Vous pouvez revenir à
      l'accueil ou nous écrire directement.
    </p>
    <div class="btn-groupe" style="justify-content:center">
      <a class="btn btn--or" href="index.html">Retour à l'accueil</a>
      <a class="btn btn--ligne-bleu" href="contact.html">Nous contacter</a>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Assemblage
# ---------------------------------------------------------------------------
PAGES = [
    ("index.html",
     f"{SOCIETE} — Immobilier, Juridique, Recouvrement, Logistique à Abidjan",
     "Groupe multiservices ivoirien : immobilier, affaires juridiques et administratives, "
     "recouvrement de créances, transport et logistique. Un interlocuteur unique à Abidjan.",
     ACCUEIL, JSONLD_ORG + "\n" + JSONLD_FAQ),

    ("groupe.html",
     f"Le Groupe — {SOCIETE}",
     "Histoire, vision, mission, valeurs et ADN d'AGER GROUP, groupe multiservices basé à "
     "Abidjan et actif sur quatre pôles complémentaires.",
     GROUPE, ""),

    ("investisseurs.html",
     f"Espace investisseurs — {SOCIETE}",
     "Thèse d'investissement, structure du modèle, marché ivoirien et sous-régional, "
     "trajectoire de développement et gouvernance d'AGER GROUP.",
     INVESTISSEURS, ""),

    ("contact.html",
     f"Contact — {SOCIETE}",
     "Contactez AGER GROUP à Abidjan. Réponse sous 24 heures ouvrées sur l'immobilier, "
     "le juridique, le recouvrement ou la logistique.",
     CONTACT, ""),

    ("mentions-legales.html", f"Mentions légales — {SOCIETE}",
     "Mentions légales du site agergroup.ci : éditeur, hébergement, propriété "
     "intellectuelle et responsabilité.", MENTIONS, ""),

    ("confidentialite.html", f"Politique de confidentialité — {SOCIETE}",
     "Données collectées, finalités, durées de conservation et exercice de vos droits sur "
     "le site d'AGER GROUP.", CONFIDENTIALITE, ""),

    ("plan-du-site.html", f"Plan du site — {SOCIETE}",
     "Toutes les pages du site AGER GROUP.", PLAN, ""),

    ("404.html", f"Page introuvable — {SOCIETE}",
     "La page demandée est introuvable sur le site d'AGER GROUP.", ERREUR404, ""),
]


def construire():
    ecrits = []

    for fichier, titre, desc, corps, jsonld in PAGES:
        html = head(titre, desc, fichier, jsonld=jsonld) + entete() + corps + pied()
        with open(os.path.join(RACINE, fichier), "w", encoding="utf-8") as f:
            f.write(html)
        ecrits.append(fichier)

    for p in POLES:
        with open(os.path.join(RACINE, p["fichier"]), "w", encoding="utf-8") as f:
            f.write(page_pole(p["id"]))
        ecrits.append(p["fichier"])

    # sitemap.xml
    aujourd = datetime.date.today().isoformat()
    urls = ["index.html", "groupe.html"] + [p["fichier"] for p in POLES] + \
           ["investisseurs.html", "contact.html", "mentions-legales.html",
            "confidentialite.html", "plan-du-site.html"]
    prio = {"index.html": "1.0", "contact.html": "0.9", "investisseurs.html": "0.9"}
    lignes = "\n".join(
        f"  <url>\n    <loc>{SITE_URL}/{'' if u == 'index.html' else u}</loc>\n"
        f"    <lastmod>{aujourd}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n"
        f"    <priority>{prio.get(u, '0.8')}</priority>\n  </url>"
        for u in urls
    )
    with open(os.path.join(RACINE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + lignes + "\n</urlset>\n")
    ecrits.append("sitemap.xml")

    print("Pages générées :")
    for e in ecrits:
        print("  ·", e)


if __name__ == "__main__":
    construire()
