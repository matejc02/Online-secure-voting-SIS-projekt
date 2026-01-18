# Online-secure-voting-SIS-projekt

Sustav za online glasanje s naglaskom na sigurnost: autentifikacija, integritet, povjerljivost, anonimnost i verifikacija procesa glasanja.
Glavna sigurnosna logika je implementirana u backendu. 

## Tehnologije

- [x] Backend: Python (Flask). 
- [x] Baza: SQLite. 
- [x] Frontend: React (odabrano kao tehnologija). 
- [x] JWT (autentifikacija/autorizacija). 
- [x] Secrets (kriptografski sigurni tokeni). 
- [x] RSA (par privatni/javni ključ). 
- [x] SHA-256 (hash lozinki / hashiranje). 
- [x] Digitalni potpis (privatni ključ potpis, javni ključ provjera).
- [x] “Blockchain” zapis u JSON datoteku (lanac blokova). 
- [~] ZKP koncept (commitment + secret + provjera), bez formalnog ZKP protokola.

## Što je implementirano

### Backend i baza
- [x] Implementiran backend u Flasku (centralno mjesto sigurnosne logike). 
- [x] SQLite baza s tablicama: `User`, `Candidate`, `VotingStatus`, `UsedTokens`. 
- [x] Nema direktne veze korisnik–kandidat u bazi (da se ne može spremiti/povezati za koga je tko glasao). 

### Korisnici, lozinke i ključevi
- [x] Registracija korisnika i generiranje RSA para ključeva (privatni/javni).
- [x] Hashiranje lozinke prije spremanja (SHA-256). 

### Autentifikacija i role
- [x] Login i izdavanje JWT tokena nakon uspješne prijave.
- [x] Role model: `VOTER` i `ADMIN`. 
- [x] Admin može upravljati stanjem glasanja (start/stop preko `VotingStatus`). 
### Token za glasanje i sprječavanje višestrukog glasanja
- [x] Admin pokretanjem glasanja dodjeljuje svim korisnicima token za glasanje. 
- [x] Token generiran kriptografski sigurnim generatorom (`secrets`). 
- [x] Prije predaje glasa provjera tokena (pravo glasa + “nije već glasao”). 
- [x] Nakon uspješne verifikacije token se briše/označava iskorištenim (sprječavanje višestrukog glasanja). 

### Zaštita glasa (commitment + “ZKP” vrijednost)
- [x] Kreiranje commitment-a (glas + secret) kako se ne bi spremio direktan odabir. 
- [x] Kreiranje dodatne “zkp” vrijednosti dodavanjem secreta radi kasnije validacije. 
- [~] Ovo je aplikacijska logika “dokaza”, ali nije implementiran formalni ZKP protokol (zk-SNARKs/zk-STARKs/Bulletproofs). 

### Digitalni potpis i verifikacija
- [x] Kreiranje poruke (commitment + zkp + token) i potpis privatnim ključem. 
- [x] Verifikacija potpisa javnim ključem prije prihvaćanja glasa. 

### “Blockchain” zapis glasova
- [x] Kreiranje bloka s: hash prethodnog bloka, commitment, token, zkp, glas, timestamp.
- [x] Računanje hash-a bloka kao identifikatora i spremanje u JSON “blockchain”. 
- [x] Kod novog glasanja briše se lanac i kreira genesis block. 

