import pandas as pd
import pyalex as pa
import datetime
import re

def make_family_name_initials(display_name: str) -> str:
    """Convert a full display name into 'FamilyName Initials' format.
    Args:
        display_name (str): Full name of the author.
    Returns:
        str: Formatted name with family name and initials.
    """
    name_parts = display_name.split()
    if len(name_parts) == 0:
        return ""
    first_name = name_parts[0]
    first_initial = first_name[0].capitalize() + "."
    return f" {first_initial} {" ".join(name_parts[1:]).strip()}"

def create_refstrings_list(
    ids: list[str],
    authors_limit: int = 10,
    short_style: bool = False
):
    """Create a reference string list from a list of pyalex IDs.
    Args:
        ids (list[str]): List of pyalex IDs.
    Returns:
        yield str: Reference strings in a formatted style.
    """
    for id in ids:
        paper = pa.Works()[id]
        if not paper:
            print(f"Warning: Paper with ID {id} not found.")
            continue
        authors = paper["authorships"]
        author_str = ", ".join([make_family_name_initials(author['author']['display_name']) for
 author in authors[:authors_limit]])
        if len(authors) > authors_limit:
            author_str += ", et al."
        year = datetime.datetime.strptime(paper["publication_date"], "%Y-%m-%d").year
        title = paper["title"]
        doi = paper.get("doi", "")
        if not short_style:
            venue = ""
            if paper.get("primary_location") and paper["primary_location"].get("source"):
                venue = paper.get("primary_location", {}).get("source", {}).get("display_name", "")
            if not venue:
                venue = paper.get("primary_location", {}).get("raw_source_name", "")
            if not venue:
                yield ""
            biblio = paper.get("biblio", {}).get("volume", "")
            issue = paper.get("biblio", {}).get("issue", "")
            biblio = f"{biblio}({issue})" if issue else biblio
            first_page = paper.get("biblio", {}).get("first_page", "")
            last_page = paper.get("biblio", {}).get("last_page", "")
            if first_page and last_page:
                biblio = f"{biblio}, {first_page}-{last_page}"
            elif first_page:
                biblio = f"{biblio}, {first_page}"
            refstring = f"{author_str} ({year}). {title}. {venue}, {biblio}. {doi}"
        else:
            refstring = f"{author_str} ({year}). {title}. {doi}"
        # Remove any xml tags and double spaces from refstring
        refstring = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", refstring)).strip()
        yield refstring
