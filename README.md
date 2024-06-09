# projektParking-
ProjektINF
Parking+ Projekt će implementirati web servis za upravljanje parkiralištem vozila. U tom kontekstu, klase bi bile Vozilo koja će sadržavati entitete kao što su registarska oznaka, marka i model vozila te ParkirnoMjesto koja će sadržavati entitete kao što su identifikator mjesta, status zauzeto/slobodno i vrijeme parkiranja. Te klase će omogućiti pohranu informacija o vozilima i parkirnim mjestima u bazu podataka.

-Klasa: Vozilo
-Entiteti; RegistarskaOznaka, Marka, Model, Boja, GodinaProizvodnje


-Klasa: ParkirnoMjesto
-Entiteti: IdentifikatorMjesdta, Status, VrijemeParkiranja (Vrijeme kada je vozilo parkirano, false ako je mjesto slobodno)

## INSTALACIJA PROJEKTA NA LOKALNO RAČUNALO
## Priprema okruženja

1. **potrebni alati:**
   - [Python](https://www.python.org/downloads/)
   - [Docker](https://www.docker.com/products/docker-desktop/)

## Postavljanje projekta u VS Code

1. **klonirajte sa GitHub-a:**
   -Dino175/projektParking- https://github.com/Dino175/projektParking-.git

2. **Postavljanje virtualnog okruženja:**
   - U terminalu, postavite virtualno okruženje

     python -m venv venv

   - Aktivirajte virtualno okruženje:
     - Na Windowsu:
       ```sh
       .\venv\Scripts\activate
       ```
     - Na macOS/Linuxu:
       ```sh
       source venv/bin/activate
       ```

3. **Instalirajte potrebne pakete:**
   - U terminalu, unutar aktiviranog virtualnog okruženja, instalirajte potrebne pakete:
     ```sh
     pip install flask
     ``
     
      pip install -r requirements.txt
   


3. **Izgradite Docker sliku:**
   - U terminalu, pokrenite naredbu:
     ```sh
     docker-compose up
     ```

4. **Pokrenite Docker container:**
   - Nakon izgradnje slike, pokrenite container:
     ```sh
     docker compose up
     ```

## Pokretanje aplikacije

1. **Pristup aplikaciji:**
   - Otvorite preglednik i idite na `http://localhost:5000`. ili samo nakon što se pokrene docker kroz terminal možemo pritisnuti (CTRL+lijevi klik) na adresu koju nam docker ponudi

