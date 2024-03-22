import time
import phonenumbers
from phonenumbers import geocoder, timezone, carrier
from colorama import init, Fore
from alive_progress import alive_bar
from geopy.geocoders import Nominatim

# Cache for geolocation data
geolocation_cache = {}

def get_geolocation(city_name: str) -> tuple:
    """
    Get latitude, longitude, and neighborhood of a city.

    Args:
        city_name (str): The name of the city.

    Returns:
        tuple: A tuple containing latitude, longitude, and neighborhood.
    """
    if city_name in geolocation_cache:
        return geolocation_cache[city_name]
    
    geolocator = Nominatim(user_agent="evil_agent")
    location = geolocator.geocode(city_name)
    latitude, longitude = location.latitude, location.longitude
    neighborhood = location.raw.get('address', {}).get('neighbourhood')
    
    geolocation_cache[city_name] = (latitude, longitude, neighborhood)
    return latitude, longitude, neighborhood

def get_ethio_telecom_info(number: str) -> str:
    """
    Get information about an Ethio Telecom number.

    Args:
        number (str): The Ethio Telecom number.

    Returns:
        str: Information about the number.
    """
    parsed_number = phonenumbers.parse(number, "ET")

    if not phonenumbers.is_valid_number(parsed_number):
        return "Invalid Ethio Telecom number."

    region_name = geocoder.description_for_number(parsed_number, "en")
    city_name = geocoder.description_for_number(parsed_number, "en", "city")
    timezone_info = timezone.time_zones_for_number(parsed_number)
    operator_name = carrier.name_for_number(parsed_number, "en")

    init(autoreset=True)  # Initialize colorama for colorful output

    info = f"The mysterious number '{number}' is registered in the mystical region of {Fore.YELLOW}{region_name}{Fore.RESET},"
    info += f" in the city of {Fore.YELLOW}{city_name}{Fore.RESET}."

    with alive_bar(5, bar='classic') as bar:
        bar.text('Fetching information...')
        time.sleep(1)
        bar.text('Enigmatic region and city found.')
        time.sleep(1)
        
        latitude, longitude, neighborhood = get_geolocation(city_name)
        
        bar.text('Unveiling enigmatic latitude, longitude, and neighborhood.')
        time.sleep(1)
        bar.text('Summoning the operator of mystery.')
        time.sleep(1)
        bar.text('Mysterious location and operator revealed. Prepare for arcane plans.')
        time.sleep(1)

    result = f"\n\n{info}"
    result += f"\n\nThe mystical location is at latitude {Fore.GREEN}{latitude}{Fore.RESET} and longitude {Fore.GREEN}{longitude}{Fore.RESET}."
    result += f"\n\nIt resides in the {Fore.CYAN}{', '.join(timezone_info)}{Fore.RESET} time zone, where secrets are kept hidden."

    if neighborhood:
        result += f"\n\nThe mysterious neighborhood is: {Fore.MAGENTA}{neighborhood}{Fore.RESET}"

    result += f"\n\nThe enigmatic operator of this number is: {Fore.RED}{operator_name}{Fore.RESET}"

    return result

# Usage example
number = input("Enter the mysterious Ethio Telecom number: ")
result = get_ethio_telecom_info(number)
print(result)
