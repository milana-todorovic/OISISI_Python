# OISISI Search Engine
*Testirano sa verzijama interpretera:* **3.7.3**, **3.7.6**, **3.8.1**  
*Korištene bilioteke:* **parglare** (detaljnije u *requirements.txt*)  
  
*Pokretanje programa:*
```
python -m searchengine
```

## Strukture podataka
### Set
Implementacija seta je zasnovana na upotrebi ugrađenog tipa *dictionary*. Elementi seta su kljucevi, i omogućeno je pridruživanje vrednosti uz ključ pri dodavanju u set (potrebno za čuvanje podataka za rangiranje).  
Procena kompleksnosti operacija, uz pretpostavku da je za operacije sa 2 skupa *n* je broj elemenata levog, a *m* desnog operanda:
* Dodavanje: **O(1)**
* Razlika: **O(n)**
* Presek: **O(min(n, m))**
* Unija: **O(n + m)**
### Graf
Za čuvanje informacija o linkovima između stranica korišten je usmeren graf, čija je implementacija zasnovana na ugrađenom tipu *dictionary* i gore opisanom tipu Set. Za predstavljanje stranica kao čvorova grafa korištena je njihova apsolutna putanja. Čvorovi grafa su čuvani kao ključevi u dict-u, uz koje su pridružene vrednosti tipa Set. Elementi Set-a su takođe apsolutne putanje stranica, i predstavljaju grane u grafu, pri čemu je grana izlazna za čvor čija je putanja ključ kom je Set pridružen, a ulazna za čvor čija je putanja element Set-a.  
Procena kompleksnosti operacija, pri čemu je *v* broj čvorova, a *e* broj grana grafa:
* Dodavanje čvora u graf: **O(1)**
* Dodavanje grane u graf: **O(1)**
* Formiranje grafa pri pokretanju aplikacije: **O(v + e)**
* Izdvajanje izlaznih grana zadatog čvora: **O(1)**
* Izdvajanje ulaznih grana zadatog čvora: **O(v)**

Izdvajanje izlaznih grana se koristi pri računanju uticaja linkova na rang, dok se izdvajanje ulaznih grana ne koristi u datoj aplikaciji, pa je u implementaciji grafa favorizovana prva operacija.
### Trie
Čvor Trie stabla sadrži dictionary, čiji su ključevi karakteri, a vrednost pridružena uz svaki ključ je čvor koji predstavlja dati karakter u strukturi. Svaki čvor takođe sadrži vrednosti tipa Set, koji je inicijalno prazan. Stranica predstavljena apsolutnom putanjom se dodaje u Set čvora, ako taj čvor predstavlja kraj reči koju stranica sadrži.
Procena kompleksnosti operacija, pri čemu je *l* dužina reči koja se dodaje ili traži:
* Dodavanje reči u stablo: **O(l)**
* Pronalaženje reči u stablu: **O(l)**  

Kako je dužina reči ograničena, može se smatrati da je navedena kompleksnost **O(1)**.  


## Algoritmi

### Pretraga po osnovnom upitu
Koraci za upit od *m* reči, uz navedenu kompleksnost:
* Izdvajanje reči : **O(m)**
* Pretraga po rečima: Za svaku pojedinačnu reč vrši se pretraga u trie stablu kompleksnosti **O(1)**, pa je ukupna kompleknost **O(m)**
* Primena skupovnih operatora: Zavisi od broja stranica u skupu pronađenom za svaku reč i operatora. Za binarne operacije, pogledati kompleksnost operacija tipa Set. 

### Rangiranje

### Sortiranje
Korišteni algoritam je radix sort, uz modifikaciju zbog promenljive dužine integera u Python-u. Koraci za sortiranje niza od *n* elemenata, uz kompleksnost:
* Traženje maksimalnog elementa u nizu koji se sortira, kako bi se odredilo kada treba zaustaviti algoritam: **O(n)**
* Radix algoritam: **O(n)**

### Inicijalno parsiranje fajlova i formiranje struktura
Vrši se jednom, tokom učitavanja direktorijuma koji se pretražuje.  
Koraci, uz navedenu kompleksnost:  
* Pronalaženje svih html stranica u direktorijumu, upotrebom funkcije os.walk: **O(d)**, gde je *d* ukupan broj fajlova i poddirektorijuma u zadatom direktorijumu
* Ubacivanje čvorova u graf: **O(v)**, gde je *v* ukupan broj pronađenih html stranica
* Parsiranje stranica upotrebom datog parsera, uz izdvajanje linkova i reci iz stranica
* Ubacivanje grana u graf: **O(e)**, gde je *e* ukupan broj linkova u stranicama
* Ubacivanje reci u trie: **O(v*w)**, gde je *w* maksimalan broj reči u stranici
* Formiranje skupa svih stranica (za potrebe napredne pretrage): **O(v)**
* Računanje inicijalnog uticaja linkova na rang: između **O(e)** i **O(v*e)**
