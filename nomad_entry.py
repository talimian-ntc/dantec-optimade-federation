import requests
from typing import List


#  ---------------------------------------------------------------------------------------------------------------------
#  Functions
#  ---------------------------------------------------------------------------------------------------------------------

def fetch_materials_by_element(element: str, page_size: int) -> List:
    url = "https://nomad-lab.eu/prod/v1/api/v1/entries/query"

    query = {
        "query": {
            "results.material.elements": element
        },
        "required": {
            "entry_id": "*",
            "entry_name": "*",
            "results.material.chemical_formula_reduced": "*",
            "results.material.elements": "*",
            "authors": "*",
            "last_processing_time": "*"
        },
        "pagination": {
            "page_size": page_size
        }
    }

    response = requests.post(url, json=query)

    materials = []

    if response.status_code == 200:
        data = response.json()

        for entry in data.get("data", []):
            material = entry.get("results", {}).get("material", {})
            entry_id = entry.get("entry_id")
            title = entry.get("entry_name")
            authors = entry.get("authors", [])
            authors = [item['name'] for item in authors]
            upload_date_time = entry.get("last_processing_time")
            upload_date = upload_date_time.split('T')[0]

            materials.append({
                "formula": material.get("chemical_formula_reduced"),
                "elements": ", ".join(material.get("elements", [])),
                "id": entry_id,
                "title": title if title is not None else '⚠ No title is available!',
                "authors": ", ".join(authors) if authors else None,
                "date": upload_date
            })

    return materials
