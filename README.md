# PGE Dystrybucja Wyłączenia | PGE Dystrybucja Outages

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://hacs.xyz/)
![Version](https://img.shields.io/badge/version-0.1.1-green.svg)
[![Downloads](https://img.shields.io/github/downloads/gregopl/PGE-Dystrybucja-Outages/total)](https://github.com/gregopl/PGE-Dystrybucja-Outages/releases)
[![Issues](https://img.shields.io/github/issues/gregopl/PGE-Dystrybucja-Outages)](https://github.com/gregopl/PGE-Dystrybucja-Outages/issues)
[![Stars](https://img.shields.io/github/stars/gregopl/PGE-Dystrybucja-Outages?style=social)](https://github.com/gregopl/PGE-Dystrybucja-Outages/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/gregopl/PGE-Dystrybucja-Outages)](https://github.com/gregopl/PGE-Dystrybucja-Outages/commits/main)

## 🇵🇱 PL (Polski)

Niestandardowa integracja dla Home Assistant pobierająca planowane/aktywne przerwy w dostawie prądu dla wybranego **miasta + ulicy** z **PGE Dystrybucja**.

### Funkcje
- Sensor pokazujący **liczbę godzin do najbliższego wyłączenia** (wartość zaokrąglona w dół).
- Wszystkie znalezione zdarzenia dodawane są do wskazanego **kalendarza** (tytuły: _PGE Wyłączenie: Planowane_ / _PGE Wyłączenie: Awaria_).
- **Wielostopniowa konfiguracja** z weryfikacją miejscowości i ulicy przez API.
- Możliwość monitorowania wielu miast i ulic.
- Blokada duplikatów.

### Instalacja (ręczna)
1. Skopiuj katalog `custom_components/pge_dystrybucja_outages` do `/config/custom_components/pge_dystrybucja_outages`.
2. Zrestartuj Home Assistant.
3. Dodaj integrację w **Ustawienia → Urządzenia i Usługi**.

### Instalacja przez HACS (repozytorium niestandardowe)
1. HACS → **Niestandardowe repozytoria**.
2. Repozytorium: `https://github.com/gregopl/PGE-Dystrybucja-Outages`; **Typ:** Integracja.
3. Zainstaluj, zrestartuj HA, dodaj integrację.

### Konfiguracja
- Krok 1: Stwórz lokalny kalendarz w HA
- Krok 2: Podaj nazwę miejscowości  
- Krok 3: Podaj nazwę ulicy  
- Krok 4: Wybierz encję lokalnego kalendarza, do którego zostaną dodane zdarzenia. (**WYMAGANE**)
- Każda kombinacja `miasto + ulica` może być dodana tylko raz.

### Wymagania / ikony
- Brak dodatkowych zależności (korzysta z bibliotek HA).

##  Uwagi
- Nieoficjalna integracja. Wykorzystuje publiczne API używane przez strony internetowe PGE: `https://pgedystrybucja.pl/wylaczenia/planowane-wylaczenia` i `https://pgedystrybucja.pl/wylaczenia/aktualne-przerwy-w-dostawie-energii` (API URLs: `falcon.gkpge.pl`, `power-outage.gkpge.pl`)
- Autor: @gregopl.

---

## 🇬🇧 EN (English)

Custom integration for Home Assistant that fetches planned/active power outages for a selected **city + street** from **PGE Dystrybucja**.

### Features
- A sensor showing **number of hours until the next outage** (floored).
- Adds **all found outages** to the selected **calendar** (titles: _PGE Wyłączenie: Planowane_ / _PGE Wyłączenie: Awaria_).
- **Multi-step configuration** with city & street validation via the public API.
- You can monitor **multiple cities and streets** (add multiple instances).
- **Duplicate protection** (same city + street can be added only once).

### Manual installation
1. Copy `custom_components/pge_dystrybucja_outages` to `/config/custom_components/pge_dystrybucja_outages`.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.

### HACS (as a custom repository)
1. HACS → Integrations → **Custom repositories**.
2. Add repo URL: `https://github.com/gregopl/PGE-Dystrybucja-Outages`, Category: **Integration**.
3. Install, restart HA, add the integration.

### Configuration
- Step 1: Create local calendar in HA
- Step 2: Enter **City**  
- Step 3: Enter **Street**  
- Step 4: Choose the **local calendar entity** that will receive outage events (**REQUIRED**)  
- Each `city + street` combination can be added **only once**.

### Requirements / Icons
- No extra dependencies — uses Home Assistant’s built-in stack.

## Credits / Notes
- Unofficial integration. Uses public API used by the PGE’s websites: `https://pgedystrybucja.pl/wylaczenia/planowane-wylaczenia` and `https://pgedystrybucja.pl/wylaczenia/aktualne-przerwy-w-dostawie-energii` (API URLs: `falcon.gkpge.pl`, `power-outage.gkpge.pl`)
- Author: @gregopl.
