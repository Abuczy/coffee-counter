# ☕ Coffee Counter

Aplikacja do śledzenia wypitych kaw.

## Funkcjonalności

- Dodawanie kaw (typ, rozmiar)
- Podgląd wszystkich kaw
- Podgląd dzisiejszych kaw
- Statystyki (łącznie, dziś, ulubiony typ)
- Usuwanie wpisów

## Tech Stack

- **Backend:** Python + FastAPI
- **Baza danych:** PostgreSQL
- **Konteneryzacja:** Docker + Docker Compose
- **CI/CD:** GitHub Actions

## Uruchomienie

Wymagania: Docker

bash
docker compose up --build


Aplikacja: http://localhost:8000

Dokumentacja API: http://localhost:8000/docs

Zatrzymanie:

bash
docker compose down


## Endpointy

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/` | Strona główna |
| GET | `/health` | Health check |
| POST | `/coffee` | Dodaj kawę |
| GET | `/coffee` | Lista wszystkich kaw |
| GET | `/coffee/today` | Dzisiejsze kawy |
| GET | `/coffee/stats` | Statystyki |
| DELETE | `/coffee/{id}` | Usuń kawę |

## Struktura projektu

```
coffee-counter/
├── app/
│   ├── main.py          # Główna aplikacja FastAPI
│   ├── database.py      # Konfiguracja bazy danych
│   └── models.py        # Modele danych
├── tests/
│   └── test_main.py     # Testy jednostkowe
├── .github/
│   ├── actions/
│   │   └── coffee-summary/
│   │       └── action.yml    # Własna akcja GitHub
│   └── workflows/
│       ├── main.yml           # Pipeline dla main branch
│       ├── pr.yml             # Pipeline dla pull requestów
│       └── reusable-build.yml # Reusable workflow
├── Dockerfile           # Multi-stage build
├── docker-compose.yml   # Konfiguracja kontenerów
└── requirements.txt     # Zależności Python
```
## CI/CD

Projekt wykorzystuje GitHub Actions:

- **PR Check** — testy i linting przy PR
- **Main Pipeline** — budowanie i publikacja obrazu do GHCR
- **Reusable Workflow** — współdzielona logika buildowania
- **Własna akcja** — coffee-summary wyświetlająca podsumowanie projektu

Projekt zaliczeniowy – Nowatorski Projekt Indywidualny (DevOps)