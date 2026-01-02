# balizasv16

Script en Python que descarga y procesa el feed **DATEX II v3.6** de incidencias de la DGT (NAP) y lista por consola las **balizas (V16) activas** publicadas con `sourceIdentification = DGT3.0`.

- Fuente de datos: NAP DGT – *SituationPublication (DATEX2 v3.6)*  
  https://nap.dgt.es/dataset/incidencias-dgt-datex2-v3-6

## Qué hace

1. Descarga el XML desde:
   - `https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v36.xml`
2. Parsea el XML en streaming (`ET.iterparse`) para no cargarlo entero en memoria.
3. Filtra registros `situationRecord` cuyo `sourceIdentification` sea **DGT3.0**.
4. Extrae y muestra por consola una tabla con:
   - **ID** (atributo `id` del `situationRecord`)
   - **FECHA** (`overallStartTime` → formato `dd/mm HH:MM`)
   - **VÍA** (`roadName`)
   - **PK** (`kilometerPoint`)
   - **SENTIDO** (`tpegDirectionRoad` mapeado)
   - **MUNICIPIO** (`municipality`)
   - **PROVINCIA** (`province`)
5. Imprime el total de registros listados como **Total Activas**.

## Requisitos

- Python **3.9+** (recomendado 3.10+)
- Dependencia:
  - `requests`

## Instalación
> ```bash
> pip install requests
> ```

## Uso

```bash
python balizasv16.py
```

### Ejemplo de salida

```
ID         FECHA        VIA          PK       SENTIDO          MUNICIPIO            PROVINCIA
--------------------------------------------------------------------------------------------------------------
123456     02/01 18:45  A-8          132.4    Creciente        TORRELAVEGA          CANTABRIA

Total Activas: 1
```
