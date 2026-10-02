# Wewnętrzna macierz oceny

| Poziom | Tytuł | Uzasadnienie | Oczekiwanie | Czego nie chcemy |
|---|---|---|---|---|
| 🔴 **Kluczowe** | **Agentowy workflow** | Podstawa zadania | Uruchamiany dla PR agent analizuje zmiany, podejmuje decyzje, korzysta z narzędzi i ich wyników oraz tworzy lub aktualizuje testy | Jednorazowe wywołanie LLM w skrypcie, zapisujące odpowiedź jako test, bez agentowego procesu |
| 🔴 **Kluczowe** | **Custom agent** | Zachowanie agenta musi być świadomie zdefiniowane | Własna definicja zadania, instrukcji, odpowiedzialności, narzędzi i ograniczeń, faktycznie używana przez środowisko agentowe | Domyślny agent bez konfiguracji albo nieużywana definicja dodana jedynie do repo |
| 🔴 **Kluczowe** | **Reużywalne skille** | Wiedza o testowaniu ma być dostępna agentowi jako reużywalne procedury | Skille obejmują React/TypeScript i Python/FastAPI; agent dobiera je do zmian i rzeczywiście stosuje podczas pracy | Cała wiedza zaszyta w jednym monolitycznym prompcie lub pliki skilli, których workflow nie wykorzystuje |
| 🔴 **Kluczowe** | **React + FastAPI** | Rozwiązanie ma obsługiwać cały projekt | Obsługa testów React/TypeScript oraz Python/FastAPI | Obsługa tylko jednej części aplikacji |
| 🔴 **Kluczowe** | **Integracja z PR** | Agent ma być częścią procesu developerskiego | Automatyczne uruchamianie dla PR oraz dostępny rezultat działania | Konieczność ręcznego uruchamiania |
| 🔴 **Kluczowe** | **Weryfikacja testów** | Wygenerowanie kodu nie oznacza jego poprawności | Wygenerowane lub zmodyfikowane testy są faktycznie uruchamiane | Generowanie testów bez ich sprawdzenia |
| 🔴 **Kluczowe** | **Pętla weryfikacji i poprawy** | Wynik narzędzia powinien wpływać na dalsze działanie agenta | Agent analizuje wynik testów i w razie błędów wygenerowanych testów poprawia je oraz ponawia weryfikację z limitem prób; raportuje nierozwiązane problemy | Zakończenie po generowaniu niezależnie od wyniku testów, nieskończone retry lub zmiana kodu aplikacji wyłącznie po to, aby test przeszedł |
| 🔴 **Kluczowe** | **Podstawowe bezpieczeństwo** | Agent otrzymuje dostęp do repozytorium i infrastruktury | Bezpieczne przechowywanie secrets i rozsądne permissions | Hardcoded secrets, nieuzasadnione szerokie uprawnienia |
| 🟡 **Standardowe** | **Analiza zmian** | Nie cały projekt jest istotny dla każdego PR | Agent identyfikuje zmieniony kod i skupia analizę na odpowiednim zakresie | Bezmyślne analizowanie całego repo przy każdym PR |
| 🟡 **Standardowe** | **Jakość testów** | Test powinien rzeczywiście sprawdzać zachowanie kodu | Sensowne przypadki testowe, edge cases, mocking i zgodność z istniejącymi konwencjami | Trywialne testy tworzone wyłącznie dla coverage |
| 🟡 **Standardowe** | **Context management** | Kontekst LLM jest ograniczonym zasobem | Świadome dobieranie kodu i informacji przekazywanych agentowi | Wrzucanie całego repo do contextu bez uzasadnienia |
| 🟡 **Standardowe** | **Optymalizacja kosztów** | Agent powinien efektywnie korzystać z LLM | Kontrola tokenów i liczby wywołań, świadomy dobór modeli/reasoning effort | Najmocniejszy model do każdej operacji, zbędny kontekst i niekontrolowane wywołania |
| 🟡 **Standardowe** | **Agent security** | Kod PR jest potencjalnie niezaufanym inputem | Świadomość prompt injection, least privilege, ochrona secrets, izolacja/sandboxing tam, gdzie potrzebne, ograniczenie blast radius | Ufanie instrukcjom w kodzie, nadmierne permissions, niekontrolowany dostęp do narzędzi/secrets |
| 🟡 **Standardowe** | **Obsługa błędów** | LLM, tools oraz testy mogą zawodzić | Kontrolowana obsługa failed testów, błędów API i innych problemów | Ukrywanie błędów, chaotyczne zakończenie workflow lub niekontrolowane retry |
| 🟡 **Standardowe** | **Architektura** | Rozwiązanie powinno mieć czytelny podział odpowiedzialności | Czytelna współpraca workflow, custom agenta, skilli i narzędzi; możliwość dalszego rozwoju bez zbędnej złożoności | Jeden ogromny prompt/skrypt odpowiedzialny za wszystko lub rozbudowana infrastruktura bez uzasadnienia |
| 🟡 **Standardowe** | **Decyzje techniczne** | Istotny jest sposób myślenia kandydata | Potrafi uzasadnić architekturę, wybór modeli/narzędzi oraz wskazać trade-offy | Brak uzasadnienia decyzji lub brak zrozumienia zastosowanych rozwiązań |
| 🟢 **Nice to have** | **Observability** | Agent powinien być możliwy do diagnozowania | Logowanie działań, czasu, błędów, wykorzystania modeli/tokenów itp. | Black box, w którym trudno ustalić, co zrobił agent |
| 🟢 **Nice to have** | **Rozszerzalność** | Rozwiązanie może w przyszłości obsługiwać więcej technologii | Architektura pozwalająca stosunkowo łatwo dodać np. Java/Spring lub kolejny typ testów | Silne powiązanie całego rozwiązania z konkretnym repo i dwoma frameworkami |

### Jak traktować poziomy

Oceniamy działanie i uzasadnienie rozwiązania, bez narzucania struktury katalogów, konkretnej platformy, frameworka, dostawcy LLM ani liczby agentów. Jeden custom agent korzystający ze skilli może w pełni spełnić wymagania. Python i inne języki są dopuszczalne do implementacji narzędzi i integracji; o spełnieniu zadania decyduje rzeczywiste wykonanie agentowego workflow.

Podczas oceny poproś o pokazanie przebiegu dla PR: użytej definicji agenta, dobranych skilli, decyzji o zakresie testów, wywołań narzędzi i wyników weryfikacji. Jeśli testy nie wymagają korekty w tym przykładzie, sprawdź również, jak workflow obsługuje niepowodzenie i limit prób. Sam opis w dokumentacji nie zastępuje działającej integracji.

**🔴 Kluczowe** — brak któregoś z tych elementów oznacza poważny problem z realizacją zadania.

**🟡 Standardowe** — tego oczekujemy od osoby pasującej do opisanej roli. Nie wszystko musi być w pełni zaimplementowane w ciągu 4 godzin, ale kandydat powinien pokazać świadomość problemu i umieć uzasadnić swoje podejście.

**🟢 Nice to have** — nie wymagamy. To elementy pozwalające wyróżnić kandydatów z większym doświadczeniem w budowaniu systemów agentowych.
