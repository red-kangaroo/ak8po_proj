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
  * [SQLAlchemy](https://www.sqlalchemy.org/) (interface pro připojení k databázi)
  * [Django](https://www.djangoproject.com/) (frontend framework)
  * [matplotlib](https://matplotlib.org/) (vizualizační knihovna)
* [Docker](https://www.docker.com/) (kontejnerizační platforma pro nasazení)
* [PostgreSQL](https://www.postgresql.org/) (relační databáze)
* [Grafana](https://grafana.com/) (mockup frontendu pro ověření konceptu)
* [OpenStreetMap](https://www.openstreetmap.org/) (vizualizace v mapě)
* [Clockify](https://app.clockify.me/) (vyhodnocení časové náročnosti plán vs skutečnost)

## Časový plán

Tento časový plán bude průběžně doplňován o již využitou časovou dotaci na jednotlivé činnosti. Předložený časový plán 
taktéž počítá s možností nadprací, pokud budou jednotlivé komponenty aplikace dokončeny v termínu nebo s časovou rezervou.
Celková časová náročnost je tak uvedena **bez nadprací** a _s nadprácemi_.

Položky označené v konečné náročnosti jako `-` nebylo nakonec nutné zpracovávat, a tedy byl tento čas oproti plánu
ušetřen.

| Aktivita | Předpokládaná<br>časová náročnost<br>(hod) | Konečná<br>časová náročnost<br>(hod) | Nadpráce<br>(zbyde-li čas) |
|----------|--------------------------------------------|--------------------------------------|---------------------------|
| Plán požadavků a rozsahu prací | 1 | 1 |
| Rešerše zdrojů dat | 3 | 2,5 |
| Design architektury | 2 | 1 |
| Příprava prostředí | 1 | 0,5 |
| Databáze - Struktura a zprovoznění | 3 | 1,5 |
| Backend - Připojení k databázi | 1 | 1,5 |
| Backend - Data scraping | 5 | 5 |
| Backend - Endpoint pro frontend | 1 | - |
| Frontend - Mockup v Grafaně | 2 | 2 |
| Frontend - Připojení k backendu | 2 | - |
| Frontend - Příprava webových stránek | 5 | **7,5** |
| Frontend - Vizualizace v grafech | 5 | **10,5** |
| Frontend - Vizualizace na mapě | 10 | ... | ANO
| Testy aplikace - Unit testy a debugging | 2 | **5,5** |
| Testy aplikace - Integrační a aplikační testy | 2 | ... | ANO
| Nasazení v cloudu | 2 | ... | ANO
| Uživatelské konzultace | 1 | 0,5 |
| Uživatelská dokumentace | 2 | 1 | ANO
| Vyhodnocení projektu | 1 | ... |
| **Celkem** | **35** (_50_) | 40+ | 1

Plnění časového plánu jde taktéž vidět v Clockify reportu [zde](doc/report.pdf).

## Spuštění aplikace

Weather Mapper je rozdělený do několika kontejnerizovaných mikroslužeb, které je potřeba spustit v Docker prostředí.
Následně jde již pracovat s webovými rozhraními aplikace v libovolném prohlížeči. Pro development použití je možné
mít Docker nainstalovaný jako [Docker Desktop](https://www.docker.com/products/docker-desktop/) a pak stačí stáhnout si
tento projekt z GitHub.

Z kořenového adresáře projektu jde aplikace sestavit a spustit pomocí:

```
docker-compose up --build -d
```

Jednotlivá rozhraní aplikace jsou pak dostupná na portu (při defaultní adrese `localhost`):

| Rozhraní | Port | Popis |
|----------|------|-------|
| Django   | `8081` | Vizualizace vybraných dat.
| Grafana  | `5052` | Vizualizace časových řad v grafech.
| pgAdmin  | `5050` | Přímý dohled nad databází. Uživatelský přístup není doporučen.

Obdobným způsobem jde aplikaci spustit na libovolném serveru s Docker prostředím, a po přidání ingress mohou být
jednotlivé služby dostupné ze samostatných URL namísto portů.

### Webové rozhraní

![](doc/web.png "Webové rozhraní")

### Grafana

![](doc/grafana.png "Grafana")

## Budoucí funkce

* Více lokalit.
  * Možnost přidávat lokality od uživatele. Možná přes lon/lat souřadnice? 
* Časová řada pro každou předpověď (zdroj a hodina), zobrazující změny na předpovědi v průběhu času.
* Statistické zpracování přesnosti předpovědí.
* Vizualizace pouze v Grafaně, vyhodnocení dat v Django.
* Autorizace a anutentikace uživatelů.

## Problémy

**pgAdmin připojení k databázi**
Pokud po přihlášení do pgAdmin není možné otevřít spojení s PostreSQL databází, je možné že došlo k restartu kontejneru
a Docker nedokázal novému kontejneru přiřadit stejnou IP. V tom případě je nutné zkontrolovat IP databáze:

```
docker inspect postgres
```

S novou IP je pak možné se normálně připojit.

## Otázky

Jakékoli otázy a připomínky je možné směřovat do [Issues](https://github.com/red-kangaroo/ak8po_proj/issues) na GitHub.
