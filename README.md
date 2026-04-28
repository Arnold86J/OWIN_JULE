# 📊 World Data Insight : Plateforme de Visualisation Globale

> Inspirée par **Our World in Data** — Analyse, Exploration et Storytelling de données mondiales.

## 🎯 Vision du Projet
Concevoir une plateforme web de référence, interactive et professionnelle, dédiée à la compréhension des grands enjeux mondiaux par la donnée. L'objectif est de transformer des datasets complexes (santé, économie, climat, démographie) en récits visuels intelligibles grâce à des outils de data visualisation de pointe.

---

## 🚀 Fonctionnalités Clés

### 🎨 Expérience Visuelle & Dashboard
* **Interface Haute Performance** : Dashboard moderne, épuré et entièrement responsive.
* **Visualisations Avancées** : Graphiques dynamiques (lignes, barres, secteurs, nuages de points) et séries temporelles comparatives.
* **Cartographie Interactive** : Cartes choroplèthes mondiales permettant une exploration géographique granulaire.
* **Mode Sombre / Clair** : Optimisé pour le confort de lecture et l'analyse prolongée.

### 🔍 Exploration de Données (Smart Data)
* **Moteur de Recherche Intelligent** : Filtres croisés par pays, continents, périodes chronologiques et indicateurs spécifiques.
* **Outils de Comparaison** : Analyse simultanée de plusieurs pays pour identifier corrélations et divergences.
* **Exportation Complète** : Téléchargement des visualisations (PNG, SVG) et des données brutes (CSV, JSON).

### 🧠 Modules Avancés (Bonus)
* **Data Storytelling** : Articles interactifs où le texte et les graphiques s'articulent pour narrer les tendances mondiales.
* **Intelligence Artificielle** : Résumés automatiques des insights clés et détection de tendances par IA.
* **Analyses Prédictives** : Projections basées sur des modèles de séries temporelles.

---

## 🛠 Stack Technologique Cible

| Couche | Technologies Recommandées |
| :--- | :--- |
| **Frontend** | React / Next.js (SSR/SSG pour le SEO) |
| **Data Viz** | D3.js (sur-mesure), ECharts ou Chart.js |
| **Cartographie** | Mapbox GL / Leaflet |
| **Backend** | Python (FastAPI/Pandas) ou Node.js |
| **Base de données** | PostgreSQL (relationnel) + Redis (cache) |
| **UI / Design** | Tailwind CSS + shadcn/ui (Design System) |
| **Infrastructure** | Docker, Vercel (Front), AWS/Railway (Back) |

---

## 🗺 Roadmap de Développement (Tickets A → Z)

### PHASE 0 — STRATÉGIE & DESIGN
* **Ticket 0.1 | Vision & Cadrage** : Définition des Personas (Chercheurs, Journalistes, Décideurs) et rédaction du Product Vision Document.
* **Ticket 0.2 | Benchmark** : Analyse comparative (OWID, World Bank, Statista) pour identifier les leviers de différenciation.
* **Ticket 0.3 | Design System** : Création de la charte graphique scientifique (accessibilité WCAG, typographies premium, composants UI).

### PHASE 1 — ARCHITECTURE & DATA ENGINEERING
* **Ticket 1.1 | Architecture Système** : Schématisation des flux API, de la base de données et setup du Monorepo.
* **Ticket 1.2 | Pipeline ETL** : Développement des scripts d'ingestion (API World Bank, WHO, ONU) et nettoyage des données via Pandas.
* **Ticket 1.3 | DevOps** : Configuration CI/CD, environnements de staging et monitoring.

### PHASE 2 — DÉVELOPPEMENT CORE
* **Ticket 2.1 | API Restful** : Endpoints de recherche, filtrage et agrégation des indicateurs.
* **Ticket 2.2 | Moteur de Visualisation** : Création des librairies de composants graphiques réutilisables.
* **Ticket 2.3 | Dashboard Admin** : Interface de gestion des datasets, validation des imports et logs système.

### PHASE 3 — ANALYSE & OPTIMISATION
* **Ticket 3.1 | IA & Analytics** : Intégration de modèles pour le résumé automatique et la prévision.
* **Ticket 3.2 | SEO & Performance** : Optimisation du rendu côté serveur (SSR), lazy loading des graphiques et CDN.
* **Ticket 3.3 | QA & Sécurité** : Tests unitaires/E2E, audits de sécurité et tests de charge.

---

## 🏁 Résultat Attendu
Un portail de **Data Journalism** de classe mondiale, éducatif et évolutif. La plateforme doit offrir une fluidité de navigation exemplaire et une rigueur scientifique capable de rivaliser avec les leaders du secteur.
