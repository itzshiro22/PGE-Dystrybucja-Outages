
# PGE Dystrybucja Outages / PGE Dystrybucja Wyłączenia

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://hacs.xyz/)
![Version](https://img.shields.io/badge/version-0.1.0-green.svg)

Custom integration for Home Assistant that fetches planned/active power outages for a selected **city + street** from **PGE Dystrybucja**.

---

## 🇵🇱 PL (Polski)

### Funkcje
- Czujnik pokazujący **liczbę godzin do najbliższego wyłączenia** (wartość zaokrąglona w dół).
- Wszystkie znalezione zdarzenia dodawane są do wskazanego **kalendarza** (tytuły: _PGE Wyłączenie: Planowane_ / _PGE Wyłączenie: Awaria_).
- **Wielostopniowa konfiguracja** z weryfikacją miejscowości i ulicy przez API Falcon.
- Blokada duplikatów (unikalne `citySym_streetSym`).

### Instalacja (ręczna)
1. Skopiuj katalog `custom_components/pge_dystrybucja_outages` do `/config/custom_components/pge_dystrybucja_outages`.
2. Zrestartuj Home Assistant.
3. Dodaj integrację w **Ustawienia → Urządzenia i Usługi**.

### Instalacja przez HACS (repozytorium niestandardowe)
1. HACS → Integrations → **Custom repositories**.
2. URL repo: `https://github.com/gregopl/PGE-Dystrybucja-Outages`; **Category:** Integration.
3. Zainstaluj, zrestartuj HA, dodaj integrację.

### Konfiguracja
- Krok 1: Podaj nazwę miejscowości – integracja zaproponuje listę, jeśli jest wiele wyników.
- Krok 2: Podaj nazwę ulicy – również z wyborem, jeśli jest wiele wyników.
- Krok 3: Wybierz encję kalendarza, do którego zostaną dodane zdarzenia.
- Każda kombinacja `miasto + ulica` może być dodana tylko raz.

### Wymagania / ikony
- Brak dodatkowych zależności (korzysta z bibliotek HA).
- Ikony: `logo.png` i `icon.png` – plik PNG, kwadrat (256×256 lub 512×512), tło przezroczyste.

---

## 🇬🇧 EN (English)

### Features
- Sensor showing **hours until the next outage** (floored).
- Adds **all outages** to a chosen **calendar** (titles: _PGE Wyłączenie: Planowane_ / _PGE Wyłączenie: Awaria_).
- **Multi-step config** with city & street validation via Falcon API.
- Duplicate protection via unique `citySym_streetSym` per entry.

### Manual installation
1. Copy `custom_components/pge_dystrybucja_outages` to `/config/custom_components/pge_dystrybucja_outages`.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.

### HACS (as custom repository)
1. HACS → Integrations → **Custom repositories**.
2. Add repo URL: `https://github.com/gregopl/PGE-Dystrybucja-Outages`, Category: **Integration**.
3. Install, restart HA, add the integration.

### Requirements / Icons
- No extra Python requirements – uses Home Assistant’s stack.
- Provide `logo.png` & `icon.png` (PNG, square 256×256 or 512×512, transparent).

---

## Credits / Notes
- Unofficial integration. Uses public endpoints behind PGE’s website: Falcon (`falcon.gkpge.pl`) and outages API (`power-outage.gkpge.pl`).  
- Author: @gregopl.
