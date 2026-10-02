# Zadanie rekrutacyjne — AI Unit Test Agent

## Kontekst

Otrzymujesz repozytorium przykładowej aplikacji full-stack składającej się z:

- **Frontendu:** React + TypeScript
- **Backendu:** Python + FastAPI
- **Source control:** Git / GitHub

W projekcie znajdują się zarówno fragmenty posiadające testy jednostkowe, jak i kod, dla którego testy nie zostały jeszcze przygotowane.

## Zadanie

Twoim zadaniem jest przygotowanie **agentowego workflow**, którego celem jest wspieranie procesu tworzenia testów jednostkowych. Rozwiązanie powinno wykorzystywać **custom agenta oraz reużywalne skille**, uruchamiane w wybranym środowisku agentowym.

Agent powinien analizować zmiany wprowadzane w ramach Pull Requesta i, jeśli uzna to za zasadne, **tworzyć lub aktualizować testy jednostkowe dla zmienionego kodu**.

Rozwiązanie powinno:

- obsługiwać zarówno frontend, jak i backend,
- działać automatycznie dla Pull Requestów,
- weryfikować poprawność przygotowanych testów poprzez ich uruchomienie,
- udostępniać rezultat działania w kontekście Pull Requesta.

## Oczekiwany sposób realizacji

Rozwiązanie powinno obejmować **agentowy workflow, custom agenta oraz reużywalne skille** wykorzystywane w jego działaniu.

Wybór narzędzi, platformy, architektury i organizacji projektu pozostaje **do Twojej decyzji**.

## Dokumentacja

Do rozwiązania dołącz krótki plik `SOLUTION.md`, w którym opisz:

- najważniejsze decyzje techniczne i ich uzasadnienie,
- jak uruchomić workflow dla PR i jakie wymagania trzeba wcześniej spełnić,
- gdzie zdefiniowano custom agenta i skille oraz jak są wykorzystywane podczas wykonania,
- przykład działania z informacją o decyzjach agenta, użytych skillach i wynikach uruchomienia testów,
- przyjęte założenia,
- ograniczenia rozwiązania,
- elementy, które rozwinąłbyś lub zmienił w wersji produkcyjnej.
