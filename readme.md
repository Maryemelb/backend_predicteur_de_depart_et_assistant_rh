# Documentation Projet – RetentionAI

**Plateforme Backend Intelligente de Prédiction du Turnover et Recommandations RH**

---

## 1. Introduction

### 1.1 Contexte général

Les départs volontaires représentent un enjeu stratégique majeur pour les directions des Ressources Humaines.
Ils entraînent des coûts importants (recrutement, formation, perte de savoir-faire) et fragilisent la performance globale de l'entreprise.

Actuellement, la majorité des décisions RH reposent sur :

- des analyses **a posteriori**,
- des indicateurs descriptifs,
- des appréciations humaines souvent subjectives.

**Point clé :** Il n'existe pas d'outil prédictif fiable ni de mécanisme automatisé de recommandations personnalisées.


---

## 2. Objectifs du Projet

### 2.1 Objectifs Business

- Identifier les employés à **haut risque de démission**
- Aider les RH à prendre des **décisions proactives**
- Proposer des **actions concrètes, personnalisées et opérationnelles**
- Réduire la subjectivité et les décisions manuelles

---

### 2.2 Objectifs Techniques

- Construire un **pipeline ML supervisé robuste**
- Comparer et optimiser plusieurs modèles
- Exposer le modèle via une **API FastAPI sécurisée**
- Intégrer une **IA générative externe**
- Garantir :
  - sécurité (JWT),
  - traçabilité (PostgreSQL),
  - reproductibilité (Docker),
  - qualité (tests unitaires).

---

## 3. Data Science & Machine Learning Supervisé

### 3.1 Objectif ML

Construire un modèle capable de prédire la probabilité de départ volontaire (`churn_probability`) d'un employé à partir de données RH internes.

---

### 3.2 Analyse & Préparation des Données

#### 3.2.1 Nettoyage des données

- Suppression des variables non pertinentes (ID techniques, colonnes constantes, redondantes)
- Gestion des valeurs manquantes
- Vérification de la cohérence des données

---

#### 3.2.2 Analyse Exploratoire (EDA)

- Visualisation des distributions (Seaborn)
- Analyse des déséquilibres de classes
- Étude des corrélations avec la variable cible (`Attrition`)
- Analyse des relations variables et churn

---

### 3.3 Préprocessing

- Transformation de la cible :
  - `Yes → 1`, `No → 0`
- Encodage catégoriel :
  - `OneHotEncoder`
- Mise à l'échelle :
  - **RobustScaler** (résistant aux outliers)
- Gestion du déséquilibre :
  - **SMOTE** (Synthetic Minority Over-sampling Technique)

---

### 3.4 Modèles entraînés

- Régression Logistique
- Random Forest Classifier

---

### 3.5 Évaluation des modèles

#### Métriques utilisées :

- Accuracy
- Recall (prioritaire pour capter les départs)
- F1-score
- Matrice de confusion
- Courbe ROC

---

### 3.6 Résultats Expérimentaux

#### Avant mise à l'échelle (sans RobustScaler)

| Modèle                | Accuracy | Recall | F1-score |
| --------------------- | -------- | ------ | -------- |
| Random Forest         | 0.8458   | 0.1818 | 0.2917   |
| Régression Logistique | 0.8413   | 0.1429 | 0.2391   |

---

#### Après application de RobustScaler

| Modèle                | Accuracy   | Recall     | F1-score   |
| --------------------- | ---------- | ---------- | ---------- |
| Random Forest         | 0.8685     | 0.1803     | 0.2750     |
| Régression Logistique | **0.8776** | **0.2131** | **0.3250** |

---

#### Après gestion du déséquilibre avec SMOTE

| Modèle                | Accuracy   | Recall     | F1-score   |
| --------------------- | ---------- | ---------- | ---------- |
| Random Forest         | 0.8662     | 0.25       | 0.3656     |
| Régression Logistique | **0.8730** | **0.3529** | **0.4615** |

**Modèle final retenu :** Régression Logistique + RobustScaler + SMOTE

**Justification :** Meilleur compromis entre recall et F1-score pour un usage RH.

---

### 3.7 Optimisation

- `GridSearchCV`
- Validation croisée (5 folds)
- Sélection automatique des meilleurs hyperparamètres


---

## 4. Backend & API FastAPI

### 4.1 Architecture Générale

- FastAPI
- PostgreSQL
- JWT Authentication
- Modèle ML sérialisé (`.pkl`)
- API IA générative externe

---

### 4.2 Authentification & Sécurité (JWT)

#### POST `/register`

Création d'un utilisateur RH.

**Request :**
```json
{
  "username": "hr_manager",
  "password": "securepassword"
}
```

**Sécurité :**
- Hash du mot de passe : **bcrypt**
- Stockage sécurisé dans PostgreSQL

---

#### POST `/login`

Authentification utilisateur.

**Request :**
```json
{
  "username": "hr_manager",
  "password": "securepassword"
}
```

**Response :**
```json
{
  "access_token": "<JWT_SIGNÉ>",
  "token_type": "bearer"
}
```

---

### 4.3 Sécurisation des routes

- Middleware JWT
- Accès autorisé uniquement aux utilisateurs authentifiés

---

### 4.4 Endpoint Machine Learning

#### POST `/predict`

**Fonctionnement :**
- Charge le modèle `.pkl`
- Applique le pipeline de preprocessing
- Retourne une probabilité de départ

**Response :**
```json
{
  "churn_probability": 0.78
}
```

---

### 4.5 Base de Données PostgreSQL

#### Table `users`

| Champ         | Type      |
| ------------- | --------- |
| id            | SERIAL    |
| username      | VARCHAR   |
| password_hash | TEXT      |
| created_at    | TIMESTAMP |

---

#### Table `predictions_history`

| Champ       | Type      |
| ----------- | --------- |
| id          | SERIAL    |
| timestamp   | TIMESTAMP |
| user_id     | INT       |
| employee_id | INT       |
| probability | FLOAT     |

---

## 5. IA Générative & Prompt Engineering

### 5.1 Objectif

Transformer une simple prédiction ML en **valeur RH concrète**.

---

### 5.2 Logique Métier

- Si `churn_probability > 50%`
  - Génération automatique d'un plan de rétention personnalisé.

---

### 5.3 Exemple de Prompt Dynamique
```
Agis comme un expert RH.

Voici les informations sur l'employé :
- Age : [Age]
- Département : [Department]
- Rôle : [JobRole]

Contexte : ce salarié a un risque élevé de départ selon le modèle ML.

Tâche : propose 3 actions concrètes et personnalisées pour le retenir, 
en tenant compte de sa satisfaction, performance et équilibre vie pro/perso.
```

---

### 5.4 Endpoint IA

#### POST `/generate-retention-plan`

**Response :**
```json
{
  "retention_plan": [
    "Proposer 2 jours de télétravail",
    "Réévaluer la charge de déplacement",
    "Mettre en place un plan de formation personnalisé"
  ]
}
```

---

## 6. Frontend (Vue d'ensemble)

### Objectifs

- Authentification RH
- Saisie du profil employé
- Visualisation du risque de départ
- Affichage automatique du plan de rétention

### Technologie utilisée

- **Next.js (React)**

---

## 7. Docker & Déploiement

### Objectifs

- Même environnement partout
- Déploiement reproductible
- Lancement en une seule commande

### Fichiers requis

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`

### Commande de lancement
```bash
docker-compose up --build
```

---

## 8. Tests Unitaires (Pytest)

**Cas de test couverts :**

- Vérifier le chargement du modèle
- Vérifier la cohérence des prédictions
- Mock de l'API LLM externe
- Tests des endpoints sécurisés

**Exécution :**
```bash
pytest 
```


---

## 9. Conclusion

RetentionAI est une solution **complète, industrialisée et orientée métier**, combinant :

- Machine Learning prédictif,
- IA générative,
- API sécurisée,
- Bonnes pratiques MLOps et Backend.

**Impact :** Cette solution permet aux RH de passer d'une **approche réactive** à une **approche proactive et intelligente**.

---

## Annexes

### Livrables

- Code source complet (backend + frontend)
- Modèle ML entraîné (`.pkl`)
- Documentation technique
- Tests unitaires
- Configuration Docker
- Collection Postman

### Technologies utilisées

- **Backend :** FastAPI, PostgreSQL, SQLAlchemy
- **ML :** scikit-learn, pandas, numpy, SMOTE
- **IA Générative :** OpenAI API / Hugging Face
- **DevOps :** Docker, Docker Compose, pytest
- **Tracking :** MLflow (bonus)
- **CI/CD :** GitHub Actions (bonus)

---

## Contact

Pour toute question ou support technique :
- GitHub : https://github.com/Maryemelbhttps://github.com/Maryemelb
- Email : maryemelbergui@gmail.com