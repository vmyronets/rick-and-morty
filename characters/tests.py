from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from characters.models import Character


class CharacterViewsTests(APITestCase):
    def setUp(self):
        # Create a small set of characters to test against
        self.char_1 = Character.objects.create(
            api_id=1,
            name="Rick Sanchez",
            status=Character.StatusChoices.ALIVE,
            species="Human",
            gender=Character.GenderChoices.MALE,
            image="https://example.com/rick.png",
        )
        self.char_2 = Character.objects.create(
            api_id=2,
            name="Morty Smith",
            status=Character.StatusChoices.ALIVE,
            species="Human",
            gender=Character.GenderChoices.MALE,
            image="https://example.com/morty.png",
        )
        self.char_3 = Character.objects.create(
            api_id=3,
            name="Birdperson",
            status=Character.StatusChoices.UNKNOWN,
            species="Alien",
            gender=Character.GenderChoices.OTHER,
            image="https://example.com/birdperson.png",
        )

    def test_get_random_character_view_returns_valid_character(self):
        """Ensure the random character view returns a valid character."""

        url = reverse("characters:character-random")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the response has all serializer fields
        for field in (
                "id", "api_id", "name", "status", "species", "gender", "image"
        ):
            self.assertIn(field, response.data)

        # Ensure the id returned exists among created characters
        self.assertIn(
            response.data["id"],
            [self.char_1.id, self.char_2.id, self.char_3.id]
        )

    def test_character_list_view_returns_all_without_filter(self):
        """
        Ensure the character list view returns all characters without a filter.
        """
        url = reverse("characters:character-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # Check that known names are present
        names = {obj["name"] for obj in response.data}
        self.assertSetEqual(
            names, {"Rick Sanchez", "Morty Smith", "Birdperson"}
        )

    def test_character_list_view_filters_by_name_icontains(self):
        """Ensure the character list view filters by name."""

        url = reverse("characters:character-list")

        # Filter that should match Rick and Morty
        # by substring 'r' (case-insensitive)
        response = self.client.get(url, {"name": "r"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = {obj["name"] for obj in response.data}

        # 'r' is in Rick, Morty, and Birdperson -> all three
        self.assertSetEqual(
            names, {"Rick Sanchez", "Morty Smith", "Birdperson"}
        )

        # Filter that should only match Morty
        response = self.client.get(url, {"name": "morty"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [obj["name"] for obj in response.data]
        self.assertEqual(names, ["Morty Smith"])
