import json
import time
import requests
from bs4 import BeautifulSoup


def scrape_coursera_free_courses(
    total_pages=3,
    output_filename="coursera_courses.json"
):

    base_url = "https://www.coursera.org/courses?query=free"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0.0.0 Safari/537.36"
        )
    }

    scraped_courses = []

    # Used to remove duplicate courses
    seen_courses = set()

    for page in range(1, total_pages + 1):

        params = {
            "query": "free",
            "page": page
        }

        print(f"Fetching Page {page}...")

        response = requests.get(
            base_url,
            headers=headers,
            params=params
        )

        if response.status_code != 200:

            print(
                f"Failed to retrieve page {page}. "
                f"Status code: {response.status_code}"
            )

            continue

        response.encoding = "utf-8"

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find course cards
        cards = soup.select(
            "ul.cds-Results-list > li"
        )

        if not cards:

            cards = soup.find_all(
                "li",
                class_="cds-9"
            )

        # Process each course
        for card in cards:

            # Helper function
            def get_text_safe(
                selector,
                default="N/A"
            ):

                element = card.select_one(selector)

                if element:

                    text = element.get_text(
                        " ",
                        strip=True
                    )

                    # Remove encoding problem
                    text = text.replace("Â", "")

                    return text.strip()

                return default

            # 1. Course Name
            course_name = get_text_safe("h3")

            # 2. Organization Name
            organization_name = get_text_safe(
                "p.cds-ProductCard-partnerNames"
            )

            # Default values
            rating_score = "N/A"
            duration = "N/A"
            course_level = "N/A"
            course_type = "N/A"


            # 3. RATING SCORE
            rating_span = card.select_one(
                "div.cds-RatingStat-meter span"
            )

            if rating_span:

                rating_text = rating_span.get_text(
                    strip=True
                )

                rating_text = rating_text.replace(
                    "Â",
                    ""
                ).strip()

                try:

                    rating_score = float(
                        rating_text
                    )

                except ValueError:

                    rating_score = "N/A"

            # 4, 5, 6. LEVEL, TYPE, DURATION
            metadata = card.select_one(
                "div.cds-CommonCard-metadata p"
            )

            if metadata:

                metadata_text = metadata.get_text(
                    " ",
                    strip=True
                )

                metadata_text = metadata_text.replace(
                    "Â",
                    ""
                ).strip()

                parts = [
                    part.strip()
                    for part in metadata_text.split("·")
                    if part.strip()
                ]


                if len(parts) >= 3:

                    # Course level
                    course_level = parts[0]

                    # Course type
                    course_type = parts[1]

                    # Duration
                    duration = " · ".join(
                        parts[2:]
                    )

            # REMOVE DUPLICATES
            if course_name != "N/A":

                course_key = (
                    course_name.strip().lower(),
                    organization_name.strip().lower()
                )

                if course_key in seen_courses:

                    continue

                seen_courses.add(
                    course_key
                )

                # ADD COURSE TO LIST
                scraped_courses.append({

                    "course_name":
                        course_name,

                    "organization_name":
                        organization_name,

                    "rating_score":
                        rating_score,

                    "duration":
                        duration,

                    "course_level":
                        course_level,

                    "course_type":
                        course_type

                })


        print(
            f"Unique courses collected so far: "
            f"{len(scraped_courses)}"
        )

        # Delay between pages
        time.sleep(2)

    # SAVE DATA TO JSON
    with open(
        output_filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            scraped_courses,
            f,
            indent=4,
            ensure_ascii=False
        )


    print()
    print("=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)

    print(
        f"Saved {len(scraped_courses)} "
        f"unique courses to "
        f"'{output_filename}'."
    )

# MAIN
if __name__ == "__main__":

    scrape_coursera_free_courses(
        total_pages=12
    )