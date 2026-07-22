<?php
/**
 * AGER GROUP — traitement du formulaire de contact
 *
 * Reçoit les données du formulaire de contact.html, les valide, puis envoie
 * un e-mail au groupe. Répond en JSON lorsque l'appel vient du JavaScript,
 * et redirige vers une page de confirmation sinon.
 *
 * CONFIGURATION : ajustez les constantes du bloc ci-dessous.
 */

declare(strict_types=1);

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const DESTINATAIRE   = 'info@agergroup.ci';
const EXPEDITEUR     = 'site@agergroup.ci';   // doit appartenir à votre domaine
const SUJET_PREFIXE  = '[Site AGER GROUP]';
const COPIE_CLIENT   = true;                  // accusé de réception au visiteur
const JOURNAL        = __DIR__ . '/demandes.log'; // mettre '' pour désactiver

// ---------------------------------------------------------------------------
// Utilitaires
// ---------------------------------------------------------------------------
function estAjax(): bool
{
    return isset($_SERVER['HTTP_X_REQUESTED_WITH'])
        && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';
}

function repondre(bool $ok, string $message, int $code = 200): void
{
    http_response_code($code);

    if (estAjax()) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message], JSON_UNESCAPED_UNICODE);
        exit;
    }

    $etat = $ok ? 'ok' : 'erreur';
    header('Location: contact.html?envoi=' . $etat . '#contenu');
    exit;
}

/** Nettoie une valeur et neutralise toute tentative d'injection d'en-tête. */
function propre(string $cle, int $max = 500): string
{
    $valeur = $_POST[$cle] ?? '';
    if (!is_string($valeur)) {
        return '';
    }
    $valeur = trim($valeur);
    $valeur = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $valeur);
    $valeur = strip_tags($valeur);
    return mb_substr($valeur, 0, $max);
}

// ---------------------------------------------------------------------------
// Contrôles préalables
// ---------------------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    repondre(false, 'Méthode non autorisée.', 405);
}

// Piège à robots : ce champ est invisible pour un humain.
if (!empty($_POST['societe_web'])) {
    repondre(true, 'Merci, votre demande a bien été transmise.');
}

// Limitation simple : une soumission toutes les 20 secondes par session.
session_start();
$maintenant = time();
if (isset($_SESSION['dernier_envoi']) && ($maintenant - $_SESSION['dernier_envoi']) < 20) {
    repondre(false, 'Merci de patienter quelques instants avant un nouvel envoi.', 429);
}

// ---------------------------------------------------------------------------
// Récupération et validation
// ---------------------------------------------------------------------------
$nom       = propre('nom', 120);
$societe   = propre('societe', 120);
$email     = propre('email', 160);
$telephone = propre('telephone', 40);
$pole      = propre('pole', 40);
$message   = trim(strip_tags($_POST['message'] ?? ''));
$message   = mb_substr($message, 0, 4000);

$erreurs = [];

if ($nom === '' || mb_strlen($nom) < 2) {
    $erreurs[] = 'le nom';
}
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $erreurs[] = 'une adresse e-mail valide';
}
if ($telephone === '' || mb_strlen($telephone) < 6) {
    $erreurs[] = 'un numéro de téléphone';
}
if ($message === '' || mb_strlen($message) < 10) {
    $erreurs[] = 'un message';
}
if (empty($_POST['consentement'])) {
    $erreurs[] = 'votre accord sur l\'utilisation des données';
}

if ($erreurs) {
    repondre(false, 'Merci d\'indiquer ' . implode(', ', $erreurs) . '.', 422);
}

// ---------------------------------------------------------------------------
// Libellé du pôle
// ---------------------------------------------------------------------------
$libelles = [
    'immobilier'    => 'Immobilier',
    'juridique'     => 'Juridique & Administratif',
    'recouvrement'  => 'Recouvrement',
    'logistique'    => 'Transport & Logistique',
    'investisseur'  => 'Demande d\'investisseur',
    'autre'         => 'Autre / non précisé',
];
$libellePole = $libelles[$pole] ?? 'Non précisé';

// ---------------------------------------------------------------------------
// Composition du message
// ---------------------------------------------------------------------------
$horodatage = date('d/m/Y à H:i');
$ip = $_SERVER['REMOTE_ADDR'] ?? 'inconnue';

$corps = <<<TEXTE
Nouvelle demande reçue depuis le site agergroup.ci

Pôle concerné : {$libellePole}
Reçue le      : {$horodatage}

--- Coordonnées -------------------------------------------
Nom        : {$nom}
Société    : {$societe}
E-mail     : {$email}
Téléphone  : {$telephone}

--- Message -----------------------------------------------
{$message}

-----------------------------------------------------------
Adresse IP de l'expéditeur : {$ip}
TEXTE;

$entetes = [
    'From: AGER GROUP <' . EXPEDITEUR . '>',
    'Reply-To: ' . $nom . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: PHP/' . phpversion(),
];

$sujet = SUJET_PREFIXE . ' ' . $libellePole . ' — ' . $nom;

$envoye = @mail(DESTINATAIRE, $sujet, $corps, implode("\r\n", $entetes));

// ---------------------------------------------------------------------------
// Accusé de réception au visiteur
// ---------------------------------------------------------------------------
if ($envoye && COPIE_CLIENT) {
    $accuse = <<<TEXTE
Bonjour {$nom},

Nous avons bien reçu votre demande concernant : {$libellePole}.

Nos équipes l'examinent et reviennent vers vous sous 24 heures ouvrées.
Pour toute urgence, vous pouvez nous joindre au +225 07 78 67 24 23.

Rappel de votre message :
--------------------------------------------
{$message}
--------------------------------------------

Cordialement,

AGER GROUP
Construire l'avenir, sécuriser le présent.
Abidjan, Côte d'Ivoire — agergroup.ci
TEXTE;

    @mail(
        $email,
        'Votre demande a bien été reçue — AGER GROUP',
        $accuse,
        implode("\r\n", [
            'From: AGER GROUP <' . EXPEDITEUR . '>',
            'Content-Type: text/plain; charset=UTF-8',
        ])
    );
}

// ---------------------------------------------------------------------------
// Journal local (utile si l'envoi de mail est indisponible)
// ---------------------------------------------------------------------------
if (JOURNAL !== '') {
    $ligne = sprintf(
        "[%s] %s | %s | %s | %s | %s | mail=%s%s",
        date('c'), $libellePole, $nom, $societe, $email, $telephone,
        $envoye ? 'ok' : 'echec', PHP_EOL
    );
    @file_put_contents(JOURNAL, $ligne, FILE_APPEND | LOCK_EX);
}

$_SESSION['dernier_envoi'] = $maintenant;

if ($envoye) {
    repondre(true, 'Merci, votre demande a bien été transmise.');
}

repondre(false, 'L\'envoi a échoué. Merci de nous écrire à ' . DESTINATAIRE . '.', 500);
