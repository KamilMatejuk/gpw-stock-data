# Warsaw Stock Exchange (GPW)
This is a program written for [INDEX Investment Chellange](https://iichallenge.gpw.pl/). Program scrapes basic data about stocks at GPW (Warsaw Stock Exchange) avaliable for trading in above challange and displays it as html.

## Running
Run Flask application
```code=bash
python main.py
```
Open webpage in browser, with attributes you want to reload<br/>
http://127.0.0.1:5000/?reload=articles,predictions,volume,graphs<br/>
*Note: reload may take some time*

## Sources
* [stooq.pl](https://stooq.pl/q/g/?s=11B')
* [gpw.pl](https://www.gpw.pl/ajaxindex.php?start=indicatorsTab&format=html&action=GPWListaSp&gls_isin=PL11BTS00015&lang=EN)
* [infostrefa.com](http://infostrefa.com/infostrefa/pl/profil/2,11BIT)
* [marketscreener.com](https://www.marketscreener.com/quote/stock/11-BIT-STUDIOS-S-A-25398936/consensus/)
* [investing.com](https://pl.investing.com/equities/11bit)

## Avaliable information
* interantional code `PL11BTS00015`
* ticker `11B`
* company name `11BIT`
* market sector `Video games`
* number of all shares `2361445`
* market value of company `1206.7 mln`
* PE ratio `7.58`
* average daily volume `8078`
* short time predictions `buy`
* list of latest articles

## Stocks
* 11BIT `11B`
* ALIOR `ALR`
* ALLEGRO `ALE`
* AMICA `AMC`
* AMREST `EAT`
* ASSECOPOL `ACP`
* ASSECOSEE `ASE`
* BENEFIT `BFT`
* BIOMEDLUB `BML`
* BNPPPL `BNP`
* BUDIMEX `BDX`
* CCC `CCC`
* CDPROJEKT `CDR`
* CIECH `CIE`
* CIGAMES `CIG`
* CLNPHARMA `CLN`
* COMARCH `CMR`
* CORMAY `CRM`
* CYFRPLSAT `CPS`
* DATAWALK `DAT`
* DEVELIA `DVL`
* DINOPL `DNP`
* DOMDEV `DOM`
* ECHO `ECH`
* ENEA `ENA`
* EUROCASH `EUR`
* FAMUR `FMF`
* GPW `GPW`
* GRUPAAZOTY `ATT`
* GTC `GTC`
* HANDLOWY `BHW`
* INGBSK `ING`
* INTERCARS `CAR`
* JSW `JSW`
* KERNEL `KER`
* KETY `KTY`
* KGHM `KGH`
* KRUK `KRU`
* LIVECHAT `LVC`
* LOTOS `LTS`
* LPP `LPP`
* MABION `MAB`
* MBANK `MBK`
* MERCATOR `MRC`
* MILLENNIUM `MIL`
* NEUCA `NEU`
* ORANGEPL `OPL`
* PEKAO `PEO`
* PGE `PGE`
* PGNIG `PGN`
* PKNORLEN `PKN`
* PKOBP `PKO`
* PKPCARGO `PKP`
* PLAYWAY `PLW`
* PZU `PZU`
* SANPL `SPL`
* TAURONPE `TPE`
* TSGAMES `TEN`
* WIRTUALNA `WPL`
* XTB `XTB`