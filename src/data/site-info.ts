/**
 * Informations légales et techniques de l'éditeur — source unique de vérité.
 *
 * Toute modification ici se répercute automatiquement sur :
 *   /mentions-legales/ , /politique-de-confidentialite/ , le bandeau cookies
 *   et le pied de page.
 *
 * ⚠️ Aucun identifiant personnel sensible (numéro de sécurité sociale, date de
 * naissance) ne doit être ajouté dans ce fichier ni dans un autre fichier du
 * dépôt : ces informations servent exclusivement aux vérifications KYC des
 * plateformes d'affiliation.
 *
 * Formulations neutres en genre (« Direction de la publication », « l'éditeur »,
 * « le responsable du traitement ») : le genre de la personne qui édite le site
 * n'étant pas connu, il n'apparaît nulle part dans les pages publiques.
 */
export const siteInfo = {
  siteName: "JourneyStorm",
  domain: "journeystorm.com",
  origin: "https://www.journeystorm.com",

  publisher: {
    name: "Thomas Nelson",
    role: "Direction de la publication",
    legalStatus:
      "Personne physique établie hors Union européenne (États-Unis), qui publie sous sa propre responsabilité.",
    address: {
      line1: "43871 Stronghold Ct",
      city: "Ashburn",
      region: "VA",
      postalCode: "20147",
      country: "États-Unis",
    },
    /**
     * true  → publie l'adresse complète (exigence LCEN art. 6 : nom et adresse
     *         professionnelle de l'éditeur).
     * false → ne publie que la ville (compromis vie privée / conformité).
     */
    publishFullAddress: true,
    email: "contact@journeystorm.com",
    /** Format international, lisible hors des États-Unis. */
    phone: "+1 703 492 1567",
    directorOfPublication: "Thomas Nelson",
  },

  /**
   * RGPD art. 27 — représentant de l'éditeur au sens de l'article 27 du RGPD.
   *
   * L'éditeur étant établi hors UE, il doit désigner un représentant établi sur
   * le territoire de l'Union européenne. Ce représentant est le point de
   * contact des visiteurs et de l'autorité de contrôle (CNIL).
   *
   * ⚠️ À COMPLÉTER — renseigner name / address / email ci-dessous.
   */
  euRepresentative: {
    enabled: false,
    name: "",
    addressLines: [] as string[],
    email: "",
  },

  hosting: {
    name: "Cloudflare, Inc.",
    address: "101 Townsend Street, San Francisco, CA 94107, États-Unis",
    phone: "+1 (650) 319-8930",
    url: "https://www.cloudflare.com",
  },

  /**
   * Régies / réseaux d'affiliation dont dépend le modèle économique du site.
   *
   * Le site diffuse des liens sponsorisés vers ces plateformes : le clic est
   * mesuré par un identifiant de campagne. Ajouter ou retirer une entrée ici
   * met à jour automatiquement les mentions légales, la politique de
   * confidentialité et le bandeau cookies.
   */
  adNetworks: [
    {
      name: "Metaffiliation (Voyage Privé)",
      purpose: "Mesure des clics vers les pages de ventes de voyages haut de gamme.",
      cookies: "Identifiant de campagne « mclic » (Metaffiliation), transmise au réseau d'affiliation lors du clic.",
      privacyPolicy: "https://www.metaffiliation.com/privacy-policy/",
    },
    {
      name: "Vacances Bleues (OXD)",
      purpose: "Mesure des clics vers les offres de villages de vacances.",
      cookies: "Identifiant de campagne « P513A7F5814031D3 », transmise au réseau d'affiliation lors du clic.",
      privacyPolicy: "https://www.vacancesbleues.fr/",
    },
    {
      name: "Maëva (Kwanko)",
      purpose: "Mesure des clics vers les offres de locations de vacances, campings et résidences de tourisme.",
      cookies: "Identifiant de campagne « P5138615814031D1 », transmise au réseau d'affiliation lors du clic.",
      privacyPolicy: "https://www.maeva.com/fr-fr/mentions-legales",
    },
  ] as const,

  /**
   * true  → les mentions légales nomment les réseaux d'affiliation utilisés.
   * false → elles n'en nomment aucun ; la liste complète reste dans la
   *         politique de confidentialité, où elle est legally requise
   *         (RGPD art. 13 : identification des tiers déposant des traceurs).
   */
  listAdNetworksInLegalNotices: true,

  analytics: {
    provider: "Google LLC — Google Analytics 4",
    id: "G-0T4J31F1E2",
  },

  /** Fournisseur d'images tiers référencé dans le pied de page. */
  imageProvider: {
    name: "Pexels",
    url: "https://www.pexels.com/",
  },

  consent: {
    /** Clé de stockage local du choix de l'utilisateur. */
    storageKey: "js_cookie_consent",
    /**
     * CNIL : le consentement est considéré comme expiré après 6 mois
     * (durée maximale recommandée pour les traceurs exemptés de consentement).
     */
    maxAgeDays: 180,
  },
} as const;

export const publisherAddress = siteInfo.publisher.publishFullAddress
  ? `${siteInfo.publisher.address.line1}, ${siteInfo.publisher.address.city} ${siteInfo.publisher.address.region} ${siteInfo.publisher.address.postalCode}, ${siteInfo.publisher.address.country}`
  : `${siteInfo.publisher.address.city} ${siteInfo.publisher.address.postalCode}, ${siteInfo.publisher.address.country}`;

export const publisherAddressHtml = siteInfo.publisher.publishFullAddress
  ? `${siteInfo.publisher.address.line1},<br />${siteInfo.publisher.address.city} ${siteInfo.publisher.address.region} ${siteInfo.publisher.address.postalCode}, ${siteInfo.publisher.address.country}`
  : `${siteInfo.publisher.address.city} ${siteInfo.publisher.address.postalCode}, ${siteInfo.publisher.address.country}`;
