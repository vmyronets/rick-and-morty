import requests

from django.db.utils import IntegrityError
from characters.models import Character
from django.conf import settings


def scrape_characters() -> list[Character]:
    """Scrape characters from Rick and Morty API."""
    url_to_scrape_next = settings.RICK_AND_MORTY_API_CHARACTERS_URL
    characters = []
    while url_to_scrape_next is not None:
        characters_response = requests.get(url_to_scrape_next).json()
        for character_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_dict["id"],
                    name=character_dict["name"],
                    status=character_dict["status"],
                    species=character_dict["species"],
                    gender=character_dict["gender"],
                    image=character_dict["image"],
                )
            )
        url_to_scrape_next = characters_response["info"]["next"]

    return characters


def save_characters(characters: list[Character]) -> None:
    """Save characters to the DB."""
    for character in characters:
        try:
            character.save()
        except IntegrityError:
            print(
                f"Character with api_id: {character.api_id} "
                f"already exists in the DB!"
            )


def sync_characters_with_api() -> None:
    """Sync characters with Rick and Morty API."""
    characters = scrape_characters()
    save_characters(characters)
