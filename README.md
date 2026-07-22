# Site web AGER GROUP

Site vitrine institutionnel construit d'après le Brand Book officiel.
**Aucune étape de compilation n'est nécessaire** : les fichiers `.html` sont
autonomes et prêts à être déposés sur un hébergement.

---

## 1. Contenu de la livraison

```
/
├── index.html                  Accueil
├── groupe.html                 Le Groupe (histoire, vision, valeurs, ADN, président)
├── immobilier.html             Pôle Immobilier
├── juridique.html              Pôle Juridique & Administratif
├── recouvrement.html           Pôle Recouvrement
├── logistique.html             Pôle Transport & Logistique
├── investisseurs.html          Espace investisseurs
├── contact.html                Contact + formulaire
├── mentions-legales.html       Mentions légales
├── confidentialite.html        Politique de confidentialité
├── plan-du-site.html           Plan du site
├── 404.html                    Page d'erreur
│
├── contact.php                 Traitement du formulaire (envoi d'e-mail)
├── .htaccess                   HTTPS, URL propres, sécurité, cache (Apache)
├── robots.txt                  Indexation
├── sitemap.xml                 Plan XML pour les moteurs
├── build.py                    Générateur des pages (optionnel — voir §6)
│
└── assets/
    ├── css/style.css           Feuille de style unique
    ├── js/main.js              Scripts (aucune dépendance externe)
    └── img/
        ├── logo-ager.svg       Logo sur fond bleu
        ├── logo-ager-blanc.svg Logo sans fond
        ├── favicon.svg         Favicon vectoriel
        ├── favicon.ico         Favicon de repli
        ├── apple-touch-icon.png Icône iOS
        └── og-image.jpg        Image de partage (1200 × 630)
```

---

## 2. Mise en ligne

### Par FTP / gestionnaire de fichiers
1. Connectez-vous à votre hébergement.
2. Déposez **tout le contenu de ce dossier** dans la racine web
   (`public_html`, `www` ou `htdocs` selon l'hébergeur).
3. Vérifiez que le fichier caché `.htaccess` a bien été transféré — beaucoup de
   clients FTP masquent les fichiers commençant par un point.
4. Ouvrez votre domaine : `index.html` s'affiche automatiquement.

### Prérequis serveur
| Élément | Nécessaire |
|---|---|
| PHP 7.4 ou supérieur | uniquement pour le formulaire (`contact.php`) |
| Apache avec `mod_rewrite` | pour les URL propres et la redirection HTTPS |
| Certificat SSL | oui — le site force HTTPS |

Le site fonctionne **sans PHP** : seul le formulaire de contact serait alors
inopérant (voir §4 pour les solutions de remplacement).

---

## 3. À personnaliser avant la mise en ligne

Cinq points seulement, tous signalés ici :

1. **Le domaine.** Ouvrez `build.py` et modifiez `SITE_URL` en haut du fichier,
   puis relancez `python3 build.py`. Sans Python, faites un
   rechercher-remplacer de `https://agergroup.ci` dans tous les `.html`, ainsi
   que dans `robots.txt` et `sitemap.xml`.

2. **Les chiffres du bandeau.** Sur `index.html`, les repères
   « 120+ dossiers », « 95 % clients reconduits » sont des valeurs à confirmer.
   Ils se modifient dans l'attribut `data-compteur` **et** dans le texte :
   ```html
   <strong data-compteur="120" data-suffixe="+">120+</strong>
   ```
   Si vous préférez ne pas afficher de chiffres, supprimez le bloc
   `<section class="reperes">`.

3. **Les réseaux sociaux.** Dans `build.py`, fonction `pied()`, remplacez les
   `href="#"` par vos URL LinkedIn, Facebook, X et YouTube. Supprimez les lignes
   des réseaux que vous n'utilisez pas.

4. **Les mentions légales.** La page `mentions-legales.html` contient un encadré
   signalant les informations à compléter : forme juridique, capital social,
   numéro RCCM, compte contribuable, adresse postale et coordonnées de
   l'hébergeur. **Ce complément est une obligation légale.**

5. **L'adresse postale.** Le site indique « Abidjan, Côte d'Ivoire ». Ajoutez la
   commune et le quartier dans `build.py` (constante `VILLE`) pour améliorer le
   référencement local.

---

## 4. Le formulaire de contact

`contact.php` valide les données, envoie un e-mail à l'adresse du groupe et
adresse un accusé de réception au visiteur. Il intègre :

- un champ piège anti-robot (invisible pour les humains) ;
- une limitation à un envoi toutes les 20 secondes ;
- un nettoyage des données contre l'injection d'en-têtes e-mail ;
- un journal local `demandes.log` en secours si l'envoi échoue.

### Configuration
Ouvrez `contact.php` et ajustez le bloc en haut du fichier :

```php
const DESTINATAIRE  = 'info@agergroup.ci';
const EXPEDITEUR    = 'site@agergroup.ci';   // doit appartenir à votre domaine
```

> **Important :** l'adresse `EXPEDITEUR` doit être une adresse réelle de votre
> domaine. Un expéditeur d'un autre domaine fait basculer les messages en
> indésirables.

### Si votre hébergement n'autorise pas `mail()`
Beaucoup d'hébergeurs mutualisés bloquent la fonction `mail()` de PHP. Deux
options :

- **SMTP authentifié** — installez PHPMailer et remplacez les appels `mail()`
  par un envoi SMTP via votre boîte professionnelle ;
- **Service externe** — remplacez `action="contact.php"` dans `contact.html` par
  l'URL d'un service de formulaire (Formspree, FormSubmit…). Le JavaScript
  fonctionne déjà avec ces services.

Dans tous les cas, testez un envoi réel avant l'annonce publique du site.

---

## 5. Hébergement sous Nginx

Le fichier `.htaccess` n'est lu que par Apache. Sous Nginx, demandez à votre
hébergeur l'équivalent :

```nginx
server {
    index index.html;
    error_page 404 /404.html;

    # URL sans extension
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

---

## 6. Modifier le menu ou le pied de page

L'en-tête et le pied sont identiques sur les douze pages. Pour éviter douze
modifications manuelles, `build.py` regénère l'ensemble :

```bash
python3 build.py
```

Le script contient, en haut de fichier, toutes les données du site :
coordonnées, description des quatre pôles, textes des pages. Modifiez-y le
contenu puis relancez la commande.

**Vous pouvez aussi ignorer complètement ce script** et éditer directement les
fichiers `.html` — ils ne dépendent de rien.

Si vous conservez `build.py` sur le serveur, il reste protégé par `.htaccess`.
Le plus simple est de ne pas le téléverser du tout.

---

## 7. Référencement

Déjà en place :

- balises `title` et `description` propres à chaque page ;
- URL canoniques ;
- balises Open Graph et Twitter Card avec image de partage ;
- données structurées JSON-LD : `Organization` sur l'accueil, `Service` sur
  chaque pôle, `FAQPage` sur les questions fréquentes ;
- `sitemap.xml` et `robots.txt` ;
- structure de titres cohérente (un seul `h1` par page).

Après la mise en ligne :

1. déclarez le site dans Google Search Console ;
2. soumettez `https://votre-domaine/sitemap.xml` ;
3. créez la fiche Google Business Profile du groupe pour le référencement local
   sur Abidjan.

---

## 8. Accessibilité et performances

- Navigation complète au clavier, focus visible, lien d'évitement.
- Contrastes conformes aux recommandations WCAG AA sur les couleurs de la charte.
- Animations désactivées si le système demande une réduction des mouvements.
- Aucune bibliothèque externe : le poids total du site est inférieur à 400 Ko.
- Feuille de style d'impression incluse.

---

## 9. Conformité à la charte

| Élément | Valeur du Brand Book |
|---|---|
| Bleu institutionnel | `#2E5F87` |
| Or prestige | `#D4A62A` |
| Bleu profond | `#173D56` |
| Gris anthracite | `#3A3A3A` |
| Blanc pur | `#FFFFFF` |
| Titres | Montserrat Bold |
| Textes | Inter |

Le motif de cadre repris sur l'ensemble du site provient directement du logo :
le Brand Book décrit le cadre blanc comme le symbole de la protection, de la
structure et de l'accompagnement. Il devient ici la signature graphique du site.

L'or est réservé aux accents et aux boutons d'action ; il n'est jamais utilisé
en aplat large, conformément à l'esprit sobre et institutionnel de la charte.
