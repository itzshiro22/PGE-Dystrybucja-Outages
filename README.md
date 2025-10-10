# PGE Dystrybucja Wyłączenia | PGE Dystrybucja Outages

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://hacs.xyz/)
![Version](https://img.shields.io/badge/version-0.1.4-green)
[![Issues](https://img.shields.io/github/issues/gregopl/PGE-Dystrybucja-Outages)](https://github.com/gregopl/PGE-Dystrybucja-Outages/issues)
[![Stars](https://img.shields.io/github/stars/gregopl/PGE-Dystrybucja-Outages?style=social)](https://github.com/gregopl/PGE-Dystrybucja-Outages/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/gregopl/PGE-Dystrybucja-Outages/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/gregopl/PGE-Dystrybucja-Outages)](https://github.com/gregopl/PGE-Dystrybucja-Outages/commits/main)

## 🇵🇱 PL (Polski)

Niestandardowa integracja dla Home Assistant pobierająca planowane/aktywne przerwy w dostawie prądu dla wybranej **miejscowości + ulicy** z **PGE Dystrybucja**.

### Funkcje
- Sensor pokazujący **liczbę godzin do najbliższego wyłączenia** (wartość zaokrąglona w dół).
- Wszystkie znalezione zdarzenia dodawane są do wskazanego **kalendarza** (tytuły: _PGE Wyłączenie: Planowane_ / _PGE Wyłączenie: Awaria_).
- **Wielostopniowa konfiguracja** z weryfikacją miejscowości i ulicy przez API PGE.
- Możliwość monitorowania wielu miejscowości i ulic.
- Blokada duplikatów.

### Instalacja (ręczna)
1. Skopiuj katalog `custom_components/pge_dystrybucja_outages` do `/config/custom_components/pge_dystrybucja_outages`.
2. Zrestartuj Home Assistant.
3. Dodaj integrację w **Ustawienia → Urządzenia i Usługi**.

### Instalacja przez HACS (repozytorium niestandardowe)
1. HACS → **Niestandardowe repozytoria**.
2. Repozytorium: `https://github.com/gregopl/PGE-Dystrybucja-Outages`; **Typ:** Integracja.
3. Kliknij **POBIERZ**.
4. Zrestartuj Home Assistant.
5. Dodaj integrację w **Ustawienia → Urządzenia i Usługi**.

### Konfiguracja
- Krok 1: Stwórz lokalny kalendarz w HA
- Krok 2: Podaj nazwę miejscowości  
- Krok 3: Podaj nazwę ulicy  
- Krok 4: Wybierz encję lokalnego kalendarza, do którego zostaną dodane zdarzenia. (**WYMAGANE**)
- Każda kombinacja `miejscowość + ulica` może być dodana tylko raz.

### Wymagania / ikony
- Brak dodatkowych zależności (korzysta z bibliotek HA).

##  Uwagi
- Nieoficjalna integracja. Wykorzystuje publiczne API używane przez strony internetowe PGE: `https://pgedystrybucja.pl/wylaczenia/planowane-wylaczenia` i `https://pgedystrybucja.pl/wylaczenia/aktualne-przerwy-w-dostawie-energii` (API URLs: `falcon.gkpge.pl`, `power-outage.gkpge.pl`)
- Autor: @gregopl. <a href="https://www.buymeacoffee.com/gregopl" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 27px !important;width: 98px !important;" ></a>

---

## 🇬🇧 EN (English)

Custom integration for Home Assistant that fetches planned/active power outages for a selected **city + street** from **PGE Dystrybucja**.

### Features
- A sensor showing **number of hours until the next outage** (floored).
- Adds **all found outages** to the selected **calendar** (titles: _PGE Wyłączenie: Planowane_ / _PGE Wyłączenie: Awaria_).
- **Multi-step configuration** with city & street validation via the public PGE API.
- You can monitor **multiple cities and streets** (add multiple instances).
- **Duplicate protection** (same city + street can be added only once).

### Manual installation
1. Copy `custom_components/pge_dystrybucja_outages` to `/config/custom_components/pge_dystrybucja_outages`.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.

### HACS (as a custom repository)
1. HACS → Integrations → **Custom repositories**.
2. Add repo URL: `https://github.com/gregopl/PGE-Dystrybucja-Outages`, Category: **Integration**.
3. Click **DOWNLOAD**.
4. Restart Home Assistant.
5. Add the integration from **Settings → Devices & Services**.

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
- Author: @gregopl. <a href="https://www.buymeacoffee.com/gregopl" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 27px !important;width: 98px !important;" ></a>

# Advanced usage

## Card example
Adding a card on HA dashboard showing planned and active outages based on <a href="https://github.com/idaho/hassio-trash-card">custom:trash-card</a>

<img width="671" height="245" alt="image" src="https://github.com/user-attachments/assets/8f6d0c44-1b6f-4d33-857b-955f42356984" />


#### Card code example:
```yaml
event_grouping: false
drop_todayevents_from: "10:00:00"
next_days: 30
pattern:
  - icon: mdi:alert
    color: red
    type: organic
    pattern: Awaria
    pattern_exact: false
  - icon: mdi:alert-circle
    color: orange
    type: custom
    pattern: Planowane
card_style: chip
alignment_style: center
color_mode: icon
items_per_row: 1
refresh_rate: 5
with_label: true
type: custom:trash-card
entities:
  - calendar.<your-local-calendar>
filter_events: false
hide_time_range: false
only_all_day_events: false
use_summary: false
grid_options:
  columns: full
  rows: auto

```

## Event updates
Integration is by default pulling new planned outages from PGE Dystrybucja every 120 minutes.
Update interval can be modified in "PGE Dystrybucja Outages" integration entity options.

<img width="662" height="246" alt="image" src="https://github.com/user-attachments/assets/61bc6d5c-5153-43e5-a38a-6d527c2c7aac" />


Update can be forced by reloading the integration entity.

<img width="654" height="599" alt="image" src="https://github.com/user-attachments/assets/1fb97d7b-4486-40fa-8356-a75357df8c5a" />

