<div align="center">

# Weather Mapper
</div>

This tool was created as a project for the AK8PO class.

## Abstrakt

Na internetu je k dospozici více zdrojů meteorologických dat, na které se libovolná aplikace může přes REST API připojit
a využít tyto data k vlastním účelům. Přepovědi počasí z těchto zdrojů však nemusí být nutně identické, neb pochází od
různých subjektů a z různých měřících stanic.

Cílem tohoto nástroje je získat dostupná meteorologická data z více zdrojů a následně poskytnout vizuální porovnání,
díky nemuž bude patrné, jaké odchylky (a v jaké míře) se mezi zdroji meteorologických dat vyskytují. Díky tomu se bude
vývojář moci jednodušeji rozhodnout, který zdroj meteorologických dat bude nejlépe vyhovovat účelům jeho aplikace.

## Požadavky

1. Získat meteorologická data z více zdrojů.
2. Vizualizovat časové řady jednotlivých metrik předpovědí.
3. Uživatel si může vybrat mezi porovnávanými zdroji.

## Technologie

* Python
  * SQLAlchemy (interface pro připojení k databázi)
  * Django (frontend framework)
* Docker (kontejnerizační platforma pro nasazení)
* PostgreSQL (relační databáze)
* Grafana (mockup frontendu pro ověření konceptu)
* [Clockify](https://app.clockify.me/) (vyhodnocení časové náročnosti plán vs skutečnost)

## Časový plán

Tento časový plán bude průběžně doplňován o již využitou časovou dotaci na jednotlivé činnosti. Předložený časový plán 
taktéž počítá s možností nadprací, pokud budou jednotlivé komponenty aplikace dokončeny v termínu nebo s časovou rezervou.

| Aktivita | Předpokládaná<br>časová náročnost<br>(hod) | Konečná<br>časová náročnost<br>(hod) | Nadpráce<br>(zbyde-li čas) |
|----------|--------------------------------------------|--------------------------------------|---------------------------|
| Plán požadavků a rozsahu prací | 1 | 1 |
| Rešerše zdrojů dat o počasí | 3 | 2 |
| Design architektury | 2 | 1 |
| Příprava prostředí | 1 | 0,5+ |
| Databáze - Struktura a zprovoznění | 3 | ... |
| Backend - Připojení k databázi | 1 | ... |
| Backend - Data scraping | 5 | 2+ |
| Backend - Endpoint pro frontend | 1 | ... |
| Frontend - Mockup v Grafaně | 2 | ... |
| Frontend - Připojení k backendu | 2 | ... |
| Frontend - Vizualizace v grafech | 10 | ... |
| Frontend - Vizualizace na mapě | 6 | ... | ANO
| Testy aplikace - Unit testy | 3 | ... |
| Testy aplikace - Integrační testy | 2 | ... |
| Testy aplikace - Uživatelské testy | 1 | ... |
| Nasazení v cloudu | 2 | ... | ANO
| Uživatelská dokumentace | 2 | ... | ANO
| **Celkem** | **37** (_47_) | ... |

## Otázky

Jakékoli otázy a připomínky je možné směřovat do [Issues](https://github.com/red-kangaroo/ak8po_proj/issues) zde na GitHubu.
