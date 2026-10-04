# AI Unit Test Agent — rozwiązanie

## Decyzje techniczne

Wybrałem GitHub Copilot CLI uruchamiany przez GitHub Agentic Workflows (`gh-aw` v0.89.21). Workflow w Markdown definiuje zadanie dla modelu, a kompilator generuje wykonywalny plik Actions. Model decyduje, które zachowania wymagają testów; istniejące Vitest i pytest sprawdzają wynik. Nie zastępuję agenta skryptem generującym szablony.

Agent pracuje w sandboxie z ograniczonym dostępem do sieci i uprawnieniami odczytu. Oddzielny mechanizm safe outputs publikuje wyłącznie pliki testowe na gałęzi PR i komentarz z raportem. Kod aplikacji, konfiguracja i zależności pozostają poza zakresem zmian agenta. Testy korzystają ze wspólnych mocków design-systemu oraz mocków bazy, więc PostgreSQL i Docker nie są wymagane.

W gh-aw v0.89.21 walidator MCP `allowed-files` błędnie obejmuje również wcześniejsze commity autora PR. Krok `pre-agent-steps` poprawia wyłącznie zakres tej kontroli na zapisany przez framework SHA head PR → commit agenta, w kopii `gh-aw/safeoutputs/safe_outputs_handlers.cjs` uruchamianej przez kontener MCP (nie w oddzielnej kopii `actions`). Lista dozwolonych testów i kontrola patcha przy publikacji pozostają aktywne. Poprawka wymaga dokładnie jednego dopasowania w przypiętej wersji skryptu; zmiana implementacji przerywa uruchomienie i wymaga przeglądu. Po poprawieniu tego zachowania w gh-aw należy usunąć obejście.

## Pliki i przebieg

| Element | Definicja i zastosowanie |
| --- | --- |
| Custom agent | `.github/agents/unit-test-agent.agent.md` — zakres pracy, wybór skilli, weryfikacja i zasady publikacji. Workflow wybiera go przez `engine.agent`. |
| Analiza PR | `.github/skills/pr-test-analysis/SKILL.md` — diff względem merge base, decyzje dla plików, baseline, weryfikacja i raport. |
| Uzupełnienie coverage | `.github/skills/coverage-backfill/SKILL.md` — wybór maksymalnie trzech niepokrytych modułów na stos w jednej iteracji. |
| Frontend | `.github/skills/react-unit-tests/SKILL.md` — React Testing Library, Vitest, wspólne mocki i typecheck. |
| Backend | `.github/skills/fastapi-unit-tests/SKILL.md` — pytest, izolacja FastAPI i mockowanie SQLAlchemy. |
| Workflow agenta | `.github/workflows/unit-test-agent.md`; wykonywany przez Actions plik `.lock.yml` jest generowany i również trafia do repozytorium. |

Skille są jawnie instalowane przez `skills:` i odczytywane przez agenta odpowiednio do zadania. Dla PR agent ustala base/head SHA, analizuje trzydotowy diff, zapisuje decyzje `create/update/skip/blocked`, uruchamia baseline i tworzy testy. Następnie uruchamia testy celowane, cały zestaw zmienionego stosu i frontendowy typecheck. Dopiero poprawnie zweryfikowane testy może zatwierdzić i przekazać do safe output. Porażka baseline lub weryfikacji oznacza sam raport bez publikacji testów. Maksymalnie dwie próby poprawienia wygenerowanych testów ograniczają pętlę napraw.

Komentarz PR zawiera rewizje, decyzje i ich przyczyny, faktycznie użyte skille, pliki testowe, polecenia, wyniki oraz link do wykonania Actions. Zmiany wyłącznie w testach/dokumentacji nie powodują generowania kolejnych testów. Limit wykonania wynosi 20 minut, 35 tur i 300 AI credits.

## Przygotowanie i uruchomienie

1. Włącz GitHub Actions i zapewnij aktywną licencję Copilot z dostępem do CLI. Wybrane akcje oraz kontenery gh-aw muszą być dozwolone przez politykę organizacji.
2. Dla obecnego repozytorium użytkownika dodaj w **Settings → Secrets and variables → Actions** sekret `COPILOT_GITHUB_TOKEN`: fine-grained PAT użytkownika z uprawnieniem konta **Copilot Requests: Read**. Nie używaj tokena OAuth z `gh auth login` jako tego sekretu. Token służy do inferencji; publikacja w tym repo korzysta z `GITHUB_TOKEN`.
3. Zapisz definicje agenta, skilli i oba pliki workflow na gałęzi bazowej. Po zmianie workflow wygeneruj lock i dołącz go do commita wraz z generowanym `.github/aw/actions-lock.json` (przypięcie akcji do SHA):

```sh
gh extension install github/gh-aw --pin v0.89.21
gh aw compile unit-test-agent --no-check-update
```

Po otwarciu, ponownym otwarciu, aktualizacji lub oznaczeniu PR jako gotowego do review workflow uruchamia się automatycznie. Wspierane są PR-y z gałęzi tego samego repozytorium.

Ręczne uruchomienie dla PR nr 123 (workflow musi już istnieć na `main`):

```sh
gh aw run unit-test-agent --ref main \
  --raw-field mode=pr \
  --raw-field 'aw_context={"item_type":"pull_request","item_number":123}'
```

Uzupełnienie istniejącego coverage na gałęzi tego PR:

```sh
gh aw run unit-test-agent --ref main \
  --raw-field mode=coverage \
  --raw-field 'aw_context={"item_type":"pull_request","item_number":123}'
```

Bez kontekstu otwartego PR workflow nie publikuje zmian. Lokalnie, z zainstalowanym i zalogowanym Copilot CLI, można wybrać ten sam profil:

```sh
copilot --agent unit-test-agent
```

Przykładowe polecenie w sesji: „Użyj coverage-backfill i skilli obu stosów. Uzupełnij testy maksymalnie trzech niepokrytych modułów na stos, uruchom testy i typecheck, pozostaw lokalny diff oraz raport. Nie publikuj zmian”. Instalacja zależności i aktywacja `.venv` są opisane w README.

W organizacji z centralnym rozliczaniem Copilota można zamiast PAT zmienić `copilot-requests: none` na `write` i ponownie skompilować workflow. Nie wymaga to sekretu inferencji. [Wymagania uwierzytelnienia](https://github.github.com/gh-aw/reference/auth/).

## Przykład wykonany w tym repozytorium

Podczas implementacji wykonałem lokalnie procedurę backfill zgodnie ze skillami `coverage-backfill`, `react-unit-tests` i `fastapi-unit-tests`. Jest to rzeczywista weryfikacja dodanych testów, a nie zapis wykonania zdalnego Copilot CLI ani przykładowy komentarz udający wynik Actions.

| Decyzja | Zachowania objęte nowymi testami |
| --- | --- |
| `create`: `frontend/src/lib/http.ts` | JSON i nagłówki, brak body przy 204, błędy sieci, anulowanie, 422, komunikat serwera i niepoprawne body błędu. |
| `create`: `useTodoFilters.ts` | Domyślna kolejność, połączenie statusu i wyszukiwania, zachowanie filtrów po zmianie danych. |
| `create`: `TodoEmptyState.tsx` | Tworzenie pierwszego zadania, zablokowana akcja, brak wyników filtrowania; wspólne mocki design-systemu. |
| `create`: `backend/app/api/health.py` | Sprawdzenie dostępności bazy i propagacja błędu, bez rzeczywistego połączenia. |
| `create`: `backend/app/core/config.py` | Priorytet argumentu/zmiennych, budowanie URL, znaki specjalne w danych i brak konfiguracji; mock ładowania `.env`. |
| `create`: `backend/app/core/lifespan.py` | Inicjalizacja sesji oraz zwolnienie silnika po sukcesie i błędach startu/obsługi aplikacji. |
| `skip` | Design-system, deklaracje typów i stałe; pozostałe moduły poza limitem tej iteracji. |

Baseline: frontend **18 testów**, backend **21 testów**, oba zestawy poprawne. Dodano **14 testów frontendu** i **9 backendu** w sześciu plikach.

| Weryfikacja z katalogu repozytorium | Wynik |
| --- | --- |
| `npm --prefix frontend test -- src/lib/http.test.ts src/features/todos/hooks/useTodoFilters.test.ts src/features/todos/components/TodoEmptyState.test.tsx` | 14/14 testów. |
| `python -m pytest -c backend/pyproject.toml backend/tests/api/test_health.py backend/tests/core/test_config.py backend/tests/core/test_lifespan.py` | 9/9 testów. |
| `npm --prefix frontend run test:coverage` | 32/32 testów, 17 plików testowych; statements 46,42% → 57,73%, branches 43,79% → 58,39%. |
| `npm --prefix frontend run typecheck` i `npm --prefix frontend run build` | Poprawne. |
| `python -m pytest -c backend/pyproject.toml backend/tests --cov=backend/app --cov-config=backend/pyproject.toml --cov-report=term-missing --cov-report=json:backend/coverage/coverage.json --cov-report=html:backend/coverage/html` | 30/30 testów; łączne pokrycie instrukcji i gałęzi 42,42% → 61,82%. |
| `gh aw compile unit-test-agent --no-check-update --actionlint` | Poprawna kompilacja i lint workflow; powtórna kompilacja daje identyczny lock. |

Sześć wybranych modułów osiągnęło 100% pokrycia mierzonych instrukcji/gałęzi. Pozostałe luki nie są ukrywane ani blokowane sztucznym progiem. Backend zgłasza istniejące ostrzeżenie Starlette dotyczące `httpx`; testy przechodzą. Lokalna weryfikacja: Node 24, Python 3.11; Workflow agenta używa Node 22 i Python 3.12.

## Założenia i ograniczenia

- Celem są sensowne testy jednostkowe, a nie 100% coverage całej aplikacji. Tryb PR obejmuje zmiany; backfill uzupełnia ograniczone partie istniejących luk.
- Repozytorium musi mieć dostęp do Copilota. Podczas tej implementacji Actions były włączone, ale nie było sekretu inferencji ani otwartego PR. Nie wykonano inferencji Copilota, zdalnego push testów ani komentarza PR; wymaga to konfiguracji opisanej powyżej i opublikowania zmian.
- Forki są wyłączone przez wygenerowany workflow i nie otrzymują dostępu do sekretów. Chroniona gałąź PR lub zmiana head w trakcie wykonania może uniemożliwić publikację; wynik wymaga wtedy przeglądu.
- Model może źle ocenić potrzebę testu lub napisać słaby test. Zielone testy nie dowodzą poprawności; wymagany jest review człowieka. Zakaz publikacji po porażce jest częścią instrukcji agenta; safe outputs niezależnie egzekwują zakres plików, ale nie oceniają jakości asercji.
- Commit przez domyślny `GITHUB_TOKEN` nie uruchamia kolejnego CI. Agent sprawdza testy przed publikacją; repozytorium nie zawiera osobnego workflow CI do testów aplikacji. [Zachowanie i opcje uruchamiania CI](https://github.github.com/gh-aw/reference/triggering-ci/).

## Wersja produkcyjna

Dodałbym niezależną weryfikację wygenerowanego patcha w osobnym izolowanym jobie przed publikacją, testy mutacyjne oceniające jakość asercji, pomiar diff coverage i monitoring kosztów/skuteczności. Do ponownego uruchamiania CI po commitach agenta użyłbym krótkotrwałego tokena GitHub App z minimalnymi uprawnieniami. Obsługę forków rozszerzyłbym przez artefakty patcha do review, bez uruchamiania ich kodu z uprawnieniami zapisu.
