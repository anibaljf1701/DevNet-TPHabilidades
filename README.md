# Cisco DevNet Associate: consulta de inventario Meraki

Ejercicio de automatización en Python realizado como trabajo práctico de habilidades para la certificación **Cisco DevNet Associate**. El programa consume la API REST de Cisco Meraki Dashboard y presenta información de organizaciones, redes, dispositivos y SSID.

## Objetivos del ejercicio

El script practica conceptos centrales de automatización y desarrollo para redes:

- Consumo de una API REST mediante solicitudes HTTP `GET`.
- Autenticación por clave de API en una cabecera HTTP.
- Construcción de rutas a partir de identificadores devueltos por la API.
- Lectura de respuestas JSON y presentación de datos en tablas.
- Selección interactiva de recursos y manejo de errores y resultados vacíos.

## Requisitos

- Python 3.8 o posterior.
- Una cuenta de Cisco Meraki Dashboard con acceso a una organización.
- Una clave de API de Meraki con permisos de lectura para los recursos consultados.
- Acceso de red a `api.meraki.com`.

La API debe estar habilitada para la cuenta en Dashboard. La clave se utiliza únicamente desde una variable de entorno; no la escribas en el código ni la subas al repositorio.

## Instalación

Desde la carpeta del repositorio, crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala la dependencia:

```bash
python -m pip install -r requirements.txt
```

## Configuración de la clave

Configura `MERAKI_DASHBOARD_API_KEY` en la terminal desde la que ejecutarás el programa.

Linux:

```bash
export MERAKI_DASHBOARD_API_KEY="tu_clave_de_api"
```

## Ejecución

Con el entorno virtual activo y la variable configurada:

```bash
python TP_Habilidades.py
```

El flujo muestra las organizaciones disponibles y solicita elegir una. Después lista las redes de esa organización y solicita elegir una. Para la red seleccionada consulta sus dispositivos y sus datos, y finalmente presenta los SSID y su estado. Si no hay dispositivos, se omite la consulta de detalle del dispositivo.

La selección se realiza ingresando el número mostrado en pantalla. El programa informa si falta la clave, si una petición HTTP falla o si un catálogo no contiene resultados. Para ejecución repetible o automatización, se pueden proporcionar IDs explícitamente:

```bash
python TP_Habilidades.py --organization-id "123456" --network-id "N_123456"
```

Los IDs deben pertenecer a la cuenta y organización disponibles para la clave configurada. El detalle de dispositivo continúa siendo interactivo cuando hay dispositivos en la red.

## Consultas a la API

El script utiliza estos endpoints de Meraki Dashboard API v1:

| Recurso | Endpoint |
| --- | --- |
| Organizaciones | `GET /organizations` |
| Redes de una organización | `GET /organizations/{organizationId}/networks` |
| Dispositivos de una red | `GET /networks/{networkId}/devices` |
| Detalle de una red | `GET /networks/{networkId}` |
| Detalle de un dispositivo | `GET /networks/{networkId}/devices/{serial}` |
| SSID de una red | `GET /networks/{networkId}/wireless/ssids` |

La URL base es `https://api.meraki.com/api/v1`. Las solicitudes tienen un tiempo máximo de espera de 30 segundos y se comprueba el estado HTTP antes de procesar el JSON.

## Estructura

| Archivo | Descripción |
| --- | --- |
| `TP_Habilidades.py` | Cliente interactivo que consulta la API de Meraki y muestra los resultados. |
| `requirements.txt` | Dependencias de Python necesarias para ejecutar el script. |
| `test_TP_Habilidades.py` | Pruebas unitarias locales; no requieren conectarse a Meraki. |
| `.gitignore` | Excluye entornos virtuales, cachés y archivos locales de configuración. |

## Pruebas

Ejecuta las pruebas desde la raíz del repositorio:

```bash
python -m unittest -v
```

## Solución de problemas

- **Falta la variable de entorno:** define `MERAKI_DASHBOARD_API_KEY` en la misma terminal y vuelve a ejecutar el script.
- **HTTP 401 o 403:** comprueba que la clave sea válida, que no haya sido revocada y que la cuenta tenga acceso a los recursos solicitados.
- **No aparecen organizaciones, redes o dispositivos:** confirma que la cuenta tenga inventario y permisos de lectura para esos recursos.
- **Error de conexión o timeout:** comprueba la conectividad con `api.meraki.com` y vuelve a intentarlo.

## Alcance

El programa es un ejercicio educativo de lectura de inventario. No modifica la configuración de la organización ni implementa paginación o reintentos automáticos. Las llamadas reales requieren credenciales válidas y acceso a una cuenta Meraki; no se incluyen credenciales ni datos de cuenta en este repositorio.
