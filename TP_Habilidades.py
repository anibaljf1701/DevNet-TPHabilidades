import argparse
import os
import sys

import requests


API_BASE_URL = "https://api.meraki.com/api/v1"
TIMEOUT_SECONDS = 30


class ItemNotFoundError(Exception):
    pass


def get_json(session, path):
    response = session.get(
        f"{API_BASE_URL}/{path.lstrip('/')}", timeout=TIMEOUT_SECONDS
    )
    response.raise_for_status()
    return response.json()


def print_table(title, columns, rows):
    values = [[str(value) for value in row] for row in rows]
    widths = [
        max([len(str(column)), *(len(row[index]) for row in values)])
        for index, column in enumerate(columns)
    ]
    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    header = "| " + " | ".join(
        str(column).ljust(width) for column, width in zip(columns, widths)
    ) + " |"
    print(f"{title}:")
    if values:
        print(separator)
        print(header)
        print(separator)
        for row in values:
            print("| " + " | ".join(value.ljust(width) for value, width in zip(row, widths)) + " |")
        print(separator)
    else:
        print("No se encontraron resultados.")
    print()


def choose_item(items, label, selected_id=None):
    if selected_id is not None:
        for item in items:
            if item.get("id") == selected_id:
                return item
        raise ItemNotFoundError(f"No se encontró {label} con ID {selected_id}.")

    if not items:
        return None

    for index, item in enumerate(items, start=1):
        print(f"{index}. {item.get('name', '(sin nombre)')} [{item.get('id', '')}]")

    while True:
        selection = input(f"Seleccione {label} (1-{len(items)}): ").strip()
        try:
            selected_index = int(selection) - 1
        except ValueError:
            selected_index = -1
        if 0 <= selected_index < len(items):
            return items[selected_index]
        print("Selección no válida. Intente nuevamente.")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Consulta inventario de Cisco Meraki Dashboard."
    )
    parser.add_argument(
        "--organization-id",
        help="ID de organización; si se omite, se elige de forma interactiva.",
    )
    parser.add_argument(
        "--network-id",
        help="ID de red; si se omite, se elige de forma interactiva.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    api_key = os.environ.get("MERAKI_DASHBOARD_API_KEY")
    if not api_key:
        print(
            "Falta la variable de entorno MERAKI_DASHBOARD_API_KEY.",
            file=sys.stderr,
        )
        return 1

    with requests.Session() as session:
        session.headers.update({"X-Cisco-Meraki-API-Key": api_key})

        organizations = get_json(session, "organizations")
        print_table(
            "Organizaciones",
            ["ID", "Nombre"],
            [[item.get("id", ""), item.get("name", "")] for item in organizations],
        )
        organization = choose_item(
            organizations, "una organización", args.organization_id
        )
        if organization is None:
            print("La cuenta no tiene organizaciones disponibles.")
            return 0

        networks = get_json(session, f"organizations/{organization['id']}/networks")
        print_table(
            "Redes de la organización",
            ["ID", "Nombre"],
            [[item.get("id", ""), item.get("name", "")] for item in networks],
        )
        network = choose_item(networks, "una red", args.network_id)
        if network is None:
            print("La organización no tiene redes disponibles.")
            return 0

        network_id = network["id"]
        devices = get_json(session, f"networks/{network_id}/devices")
        print_table(
            "Dispositivos de la red",
            ["Nombre", "Modelo", "Serial"],
            [
                [item.get("name", ""), item.get("model", ""), item.get("serial", "")]
                for item in devices
            ],
        )

        network_info = get_json(session, f"networks/{network_id}")
        print("Información de la red:")
        for label, field in (
            ("Nombre", "name"),
            ("ID", "id"),
            ("ID de organización", "organizationId"),
            ("Zona horaria", "timeZone"),
        ):
            print(f"{label}: {network_info.get(field, 'No disponible')}")
        print()

        device = choose_item(devices, "un dispositivo")
        if device is not None:
            device_info = get_json(
                session, f"networks/{network_id}/devices/{device['serial']}"
            )
            print("Información del dispositivo:")
            for label, field in (
                ("Nombre", "name"),
                ("Serial", "serial"),
                ("MAC", "mac"),
                ("Modelo", "model"),
                ("Firmware", "firmware"),
            ):
                print(f"{label}: {device_info.get(field, 'No disponible')}")
            print()

        ssids = get_json(session, f"networks/{network_id}/wireless/ssids")
        print_table(
            "SSID de la red",
            ["Número", "Nombre", "Habilitado"],
            [
                [item.get("number", ""), item.get("name", ""), item.get("enabled", "")]
                for item in ssids
            ],
        )

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except requests.RequestException as error:
        print(f"Error al consultar la API de Meraki: {error}", file=sys.stderr)
        sys.exit(1)
    except ItemNotFoundError as error:
        print(error, file=sys.stderr)
        sys.exit(2)
    except ValueError as error:
        print(f"La API devolvió una respuesta JSON no válida: {error}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperación cancelada.", file=sys.stderr)
        sys.exit(130)