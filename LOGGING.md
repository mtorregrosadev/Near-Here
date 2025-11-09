# Sistema de Logging - Near Here

## Descripció

L'aplicació Near Here ara inclou un sistema complet de logging per facilitar la depuració i el seguiment del comportament de l'aplicació.

## Configuració

El sistema de logging està configurat per:
- **Nivell**: DEBUG (mostra tots els missatges)
- **Format**: `YYYY-MM-DD HH:MM:SS [NIVELL] NomLogger: Missatge`
- **Sortides**:
  - **Console (stdout)**: Mostra els logs a la terminal
  - **Fitxer**: Guarda tots els logs a `near_here.log`

## Nivells de Log

- **DEBUG**: Informació detallada per depuració (coordenades, paràmetres, dades processades)
- **INFO**: Events importants del flux normal (inici d'aplicació, cerca de llocs, resultats)
- **WARNING**: Situacions inusuals però manejades (sense resultats, permisos pendents)
- **ERROR**: Errors que impedeixen funcionalitat (API fallida, dades invàlides)

## Zones amb Logging

### 1. Inicialització de l'Aplicació
- Inici de l'app
- Configuració de la finestra
- Permisos de geolocalització
- Inicialització de variables

### 2. Classe LLocs_sostenibles (Llocs Sostenibles)
- Inicialització amb paràmetres
- Càrrega del fitxer JSON
- Filtratge per distància i categories
- Resultats finals

**Exemple de logs:**
```
2025-10-14 10:30:15 [INFO] NearHere: LLocs_sostenibles inicialitzat - Lat: 41.9766, Long: 2.8229, Radius: 1000m, Limit: 50, Categories: []
2025-10-14 10:30:15 [INFO] NearHere: Fitxer JSON carregat correctament - Total llocs: 234
2025-10-14 10:30:15 [INFO] NearHere: Buscant llocs dins un radi de 1000m des de (41.9766, 2.8229)
2025-10-14 10:30:15 [INFO] NearHere: Llocs trobats dins el radi: 5
2025-10-14 10:30:15 [INFO] NearHere: Total llocs processats i retornats: 5
```

### 3. Classe Llocs (Foursquare API)
- Inicialització
- Coordenades randomitzades
- Peticions a l'API
- Errors i respostes

**Exemple de logs:**
```
2025-10-14 10:30:20 [INFO] NearHere: Llocs (Foursquare) inicialitzat - Lat: 41.9766, Long: 2.8229, Radius: 1000m, Limit: 50, Sort: RELEVANCE, Preu: 0, Near: None
2025-10-14 10:30:20 [INFO] NearHere: Enviant peticio a Foursquare API - Radius: 1000m, Limit: 50
2025-10-14 10:30:21 [INFO] NearHere: Resposta Foursquare API: Status 200 OK
2025-10-14 10:30:21 [INFO] NearHere: Resultats rebuts: 25
2025-10-14 10:30:21 [INFO] NearHere: Llocs nous (no visitats): 25
```

### 4. Classe Llocs_yelp (Yelp API)
- Inicialització
- Processament de categories
- Peticions a l'API
- Processament de resultats

**Exemple de logs:**
```
2025-10-14 10:30:25 [INFO] NearHere: Llocs_yelp inicialitzat - Lat: 41.9766, Long: 2.8229, Radius: 1000m, Limit: 50, Sort: RELEVANCE, Preu: 0, Near: None
2025-10-14 10:30:25 [INFO] NearHere: Enviant peticio a Yelp API - Radius: 1000m, Limit: 50
2025-10-14 10:30:26 [INFO] NearHere: Resposta Yelp API: Status 200 OK
2025-10-14 10:30:26 [INFO] NearHere: Resultats rebuts de Yelp: 30
```

### 5. Funció update_cards()
- Flux de cerca (Sostenible → Yelp → Foursquare)
- Verificació de dades
- Creació de cards
- Gestió d'errors

**Exemple de logs del flux complet:**
```
2025-10-14 10:30:15 [INFO] NearHere: === INICI UPDATE_CARDS ===
2025-10-14 10:30:15 [DEBUG] NearHere: Variables globals - canvi: True, sostenible: True, sostenible_2: True
2025-10-14 10:30:15 [INFO] NearHere: Intent 1: Cercant llocs sostenibles
2025-10-14 10:30:15 [WARNING] NearHere: Cap lloc sostenible trobat amb els criteris actuals
2025-10-14 10:30:15 [INFO] NearHere: Intent 2: Cercant llocs amb Yelp API
2025-10-14 10:30:16 [INFO] NearHere: EXIT: Llocs trobats: 25 - Origen: Yelp
2025-10-14 10:30:16 [INFO] NearHere: Iniciant creacio de 25 cards
```

### 6. Rutes de l'Aplicació
- Navegació entre pàgines
- Errors i redireccions

**Exemple de logs:**
```
2025-10-14 10:30:30 [INFO] NearHere: === RUTA: / (Pantalla principal) ===
2025-10-14 10:30:30 [INFO] NearHere: Mostrant 25 cards
```

## Com Utilitzar els Logs

### 1. Visualitzar logs en temps real a la terminal
```bash
flet run -d
```

### 2. Consultar el fitxer de log
```bash
cat near_here.log
# o
tail -f near_here.log  # Per veure en temps real
```

### 3. Filtrar logs per nivell
```bash
# Només errors
grep "ERROR" near_here.log

# Només warnings i errors  
grep -E "WARNING|ERROR" near_here.log

# Només info d'APIs
grep "API" near_here.log
```

### 4. Buscar logs d'una funció específica
```bash
# Llocs sostenibles
grep "LLocs_sostenibles" near_here.log

# Update cards
grep "UPDATE_CARDS" near_here.log

# Foursquare
grep "Foursquare" near_here.log
```

## Diagnòstic de Problemes Comuns

### Problema: "ERROR FINAL: Cap API ha retornat resultats valids"

**Buscar:**
```bash
grep -B 10 "ERROR FINAL" near_here.log
```

**Possible causa**: 
- No hi ha llocs sostenibles al radi
- Yelp retorna error 400
- Foursquare retorna error 400

### Problema: "Cap lloc sostenible trobat"

**Buscar:**
```bash
grep "Llocs trobats dins el radi" near_here.log
```

**Solució**: Augmenta el radi de cerca (radius_sel) a 5000m o més

### Problema: TypeError al processar dades

**Buscar:**
```bash
grep "Tipus dada:" near_here.log
```

**Verificar**: El tipus de `dadesLlocs` abans del bucle

## Neteja de Logs

Per eliminar logs antics:
```bash
rm near_here.log
```

El fitxer es crearà de nou automàticament en la propera execució.
