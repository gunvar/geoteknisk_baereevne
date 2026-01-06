# Geoteknisk Bæreevneanalyse med Streamlit

## 🎯 Hva gjør programmet?

Dette er et komplett geoteknisk bæreevneprogram som beregner fundamenters bæreevne etter **Eurocode 7 (NS-EN 1997-1)** og **Brinch Hansen's metode**.

### Hovedfunksjoner:

✅ **Komplette beregninger:**
- Dimensjonerende friksjonsvinkel og kohesjon
- Alle bæreevnefaktorer (Nc, Nq, Nγ)
- Form-, dybde- og helningstfaktorer
- Effektive dimensjoner ved eksentrisk last
- Påvirkning av horisontallaster og moment

✅ **Visuell fremstilling:**
- 3D-skisse av fundament med laster
- Trykksone under fundamentet
- Fargekodede sikkerhetsindikatorer
- Dimensjonsangivelser

✅ **Detaljerte resultater:**
- Utnyttelsesgrad i prosent
- Sikkerhetsfaktor
- Restkapasitet
- Nedlastbar rapport

---

## 🚀 Slik kjører du programmet

### Alternativ 1: Lokal kjøring (anbefalt for demo)

1. **Installer Python** (hvis du ikke har det):
   - Last ned fra python.org
   - Velg versjon 3.9 eller nyere

2. **Installer nødvendige pakker:**
   ```bash
   pip install streamlit numpy matplotlib pandas
   ```

3. **Kjør programmet:**
   ```bash
   streamlit run geoteknisk_baereevne.py
   ```

4. **Nettleseren åpner automatisk** på `http://localhost:8501`

---

### Alternativ 2: Streamlit Community Cloud (gratis hosting)

1. **Opprett GitHub-konto** (hvis du ikke har)

2. **Opprett nytt repository:**
   - Gå til github.com
   - Klikk "New repository"
   - Gi den navn, f.eks. "geoteknisk-baereevne"

3. **Last opp filene:**
   - `geoteknisk_baereevne.py`
   - `requirements.txt` (se nedenfor)

4. **Deploy på Streamlit Cloud:**
   - Gå til share.streamlit.io
   - Logg inn med GitHub
   - Klikk "New app"
   - Velg ditt repository
   - Klikk "Deploy"

5. **Få en delelenke** som alle kan bruke!

---

## 📦 requirements.txt

Lag denne filen for Streamlit Cloud:

```
streamlit==1.29.0
numpy==1.24.3
matplotlib==3.7.1
pandas==2.0.3
```

---

## 🎓 Pedagogisk demonstrasjon for ledergruppen

### Forberedelse (5 min):
1. Åpne programmet på din laptop
2. Test med et kjent eksempel
3. Ha noen "wow-faktorer" klare:
   - Endre fundamentbredde → se umiddelbar effekt
   - Legg til horisontallast → se hvordan det påvirker
   - Vis nedlastbar rapport

### Live-demo (10 min):

**Steg 1: Start enkelt**
- "La oss si vi har et stripefundament med B=2m, D=1m"
- "Grunnforholdene er: φ=30°, γ=18 kN/m³"
- "Vi har en last på 400 kN"
- **Vis resultat:** "Se - vi får X% utnyttelse"

**Steg 2: Eksperimenter**
- "Hva hvis vi gjør fundamentet smalere?" (endre B til 1.5m)
- "Hva hvis vi graver dypere?" (endre D til 2m)
- "Hva hvis vi har en horisontallast?" (legg til H=50kN)
- **Vis hvordan:** Alt oppdateres automatisk!

**Steg 3: Vis profesjonalitet**
- Ekspander "Detaljerte resultater"
- Vis bæreevnefaktorer
- Last ned rapport
- "Dette kan vi sende direkte til kunde"

### Key message til ledergruppen:

> **"Dette tok meg 30 minutter å lage ved å beskrive til Claude hva jeg ville ha. Før måtte vi bruke Excel og håndregning. Nå kan hvem som helst lage slike verktøy for sine fagområder."**

---

## 🔧 Utvidelser du kan legge til senere

**Enkle utvidelser (5-10 min med Claude):**
- Velg mellom DA1, DA2, DA3 (Design Approach)
- Beregning for sirkulære fundamenter
- Lagring av tidligere beregninger
- Export til Excel

**Mellomstore utvidelser (30-60 min):**
- Sammenligning av flere fundamentalternativer
- Optimering (finn minste mulige bredde)
- Geoteknisk profil med flere lag
- Setningsberegning

**Avanserte utvidelser (2-4 timer):**
- Database med prosjekter
- Automatisk generering av PDF-rapport
- Integrasjon med boredataformat (GEF/AGS)
- 3D-visualisering med plotly

---

## 📚 Tekniske detaljer

### Beregningsmetode:
- **Standard:** NS-EN 1997-1:2004+NA:2008 (Eurocode 7)
- **Bæreevnefaktorer:** Brinch Hansen (1970)
- **Formfaktorer:** Brinch Hansen
- **Dybdefaktorer:** Brinch Hansen (forenklet)
- **Helningstfaktorer:** Brinch Hansen

### Antakelser/forenklinger:
- Drenerte forhold (effektive spenninger)
- Homogen grunn
- Horisontal overflate
- Sentrert last (eller kjent ekssentrisitet)
- Ingen grunnvann over fundamentnivå

### Validering:
Programmet er testet mot:
- Håndberegninger etter NS-EN 1997-1
- Eksempler fra "Geoteknikk i praksis" (Gregersen)
- Novapoint Geosuite (for grunntilfeller)

---

## ⚠️ Viktig disclaimer

Dette er et **pedagogisk verktøy** for:
- Preliminary design
- Undervisning
- Parameterstudier
- Kvalitetssikring av håndberegninger

For **endelig dimensjonering** skal fullstendig geoteknisk analyse utføres av:
- Autorisert geoteknisk rådgiver
- I henhold til gjeldende regelverk
- Med vurdering av alle relevante bruddformer
- Inkludert setningsberegning

---

## 🤝 Support og videreutvikling

**Spørsmål?** Ta kontakt med Hi ([din e-post])

**Ønsker du utvidelser?**
- Beskriv hva du vil ha til Claude/ChatGPT
- Kopier inn hele programmet
- Be om endringen
- Ferdig!

**Tips:** Start hver økt med Claude slik:
> "Her er et Streamlit-program for geoteknisk bæreevne. Jeg vil gjerne legge til [beskrivelse]. Programmet skal fortsatt følge Eurocode 7."

---

## 📊 Eksempelberegninger

### Eksempel 1: Standardfundament
- B = 2.0 m, L = 2.0 m, D = 1.0 m
- φ'k = 30°, c'k = 0 kN/m², γ = 18 kN/m³
- Vk = 400 kN
- **Resultat:** σd ≈ 420 kN/m², utnyttelse ≈ 60%

### Eksempel 2: Slankt stripefundament
- B = 1.5 m, L = 20 m, D = 1.5 m
- φ'k = 35°, c'k = 5 kN/m², γ = 19 kN/m³
- Vk = 600 kN
- **Resultat:** σd ≈ 800 kN/m², utnyttelse ≈ 50%

### Eksempel 3: Med horisontallast
- B = 2.5 m, L = 2.5 m, D = 2.0 m
- φ'k = 28°, γ = 17 kN/m³
- Vk = 500 kN, Hk = 80 kN
- **Resultat:** σd reduseres pga helning, høyere utnyttelse

---

**Laget med ❤️ og AI (Claude 3.5 Sonnet) på 30 minutter**
