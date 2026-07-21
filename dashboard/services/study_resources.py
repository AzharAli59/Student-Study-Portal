from __future__ import annotations

import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError, WikipediaException
from youtubesearchpython import VideosSearch


class StudyResourceError(Exception):
    """Raised when an external study-resource provider cannot return a result."""


def search_books(query: str) -> list[dict]:
    try:
        response = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": query, "maxResults": 10},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise StudyResourceError("Book search is temporarily unavailable.") from exc

    results = []
    for item in payload.get("items", []):
        volume = item.get("volumeInfo", {})
        image_links = volume.get("imageLinks") or {}
        results.append(
            {
                "title": volume.get("title", "Untitled"),
                "subtitle": volume.get("subtitle"),
                "description": volume.get("description"),
                "page_count": volume.get("pageCount"),
                "categories": volume.get("categories", []),
                "rating": volume.get("averageRating"),
                "thumbnail": image_links.get("thumbnail"),
                "preview": volume.get("previewLink"),
            }
        )
    return results


def lookup_dictionary_word(word: str) -> dict:
    try:
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=10,
        )
        response.raise_for_status()
        entry = response.json()[0]
        phonetic = next(
            (item for item in entry.get("phonetics", []) if item.get("text") or item.get("audio")),
            {},
        )
        definition = entry.get("meanings", [{}])[0].get("definitions", [{}])[0]
    except (IndexError, KeyError, requests.RequestException, ValueError) as exc:
        raise StudyResourceError("No dictionary result was found for that word.") from exc

    return {
        "word": entry.get("word", word),
        "phonetic": phonetic.get("text"),
        "audio": phonetic.get("audio"),
        "definition": definition.get("definition"),
        "example": definition.get("example"),
        "synonyms": definition.get("synonyms", []),
    }


def search_wikipedia(query: str) -> dict:
    try:
        page = wikipedia.page(query, auto_suggest=False)
    except DisambiguationError as exc:
        options = ", ".join(exc.options[:5])
        raise StudyResourceError(f"Search is ambiguous. Try one of: {options}") from exc
    except PageError as exc:
        raise StudyResourceError("No Wikipedia page was found for that search.") from exc
    except WikipediaException as exc:
        raise StudyResourceError("Wikipedia search is temporarily unavailable.") from exc

    return {
        "title": page.title,
        "link": page.url,
        "summary": page.summary,
    }


def search_youtube(query: str) -> list[dict]:
    try:
        videos = VideosSearch(query, limit=10).result().get("result", [])
    except Exception as exc:
        raise StudyResourceError("YouTube search is temporarily unavailable.") from exc

    results = []
    for video in videos:
        description = "".join(
            item.get("text", "") for item in video.get("descriptionSnippet") or []
        )
        thumbnails = video.get("thumbnails") or [{}]
        channel = video.get("channel") or {}
        view_count = video.get("viewCount") or {}
        results.append(
            {
                "title": video.get("title", "Untitled"),
                "duration": video.get("duration"),
                "thumbnail": thumbnails[0].get("url"),
                "channel": channel.get("name"),
                "link": video.get("link"),
                "views": view_count.get("short"),
                "published": video.get("publishedTime"),
                "description": description,
            }
        )
    return results
