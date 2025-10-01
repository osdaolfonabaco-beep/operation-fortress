import requests
from bs4 import BeautifulSoup

URL = "https://techcrunch.com/category/startups/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

main_page_response = requests.get(URL, headers=headers)

if main_page_response.status_code != 200:
    print(f"Error al conectar. Código: {main_page_response.status_code}")
else:
    main_soup = BeautifulSoup(main_page_response.content, "html.parser")
    article_cards = main_soup.find_all("div", class_="loop-card")

    print(f"✅ Se encontraron {len(article_cards)} artículos.")
    print("Procesando los primeros 3...\n")

    for card in article_cards[:3]:
        title_link_element = card.find("a", class_="loop-card__title-link")

        if not title_link_element:
            continue

        title = title_link_element.get_text(strip=True)
        link = title_link_element["href"]

        print("--- Artículo ---")
        print(f"Título: {title}")
        print(f"Enlace: {link}")

        article_response = requests.get(link, headers=headers)
        if article_response.status_code != 200:
            print("No se pudo obtener el resumen.\n")
            continue

        article_soup = BeautifulSoup(article_response.content, "html.parser")
        summary_element = article_soup.find("p", class_="wp-block-paragraph")

        if summary_element:
            summary = summary_element.get_text(strip=True)
            if len(summary) > 70:
                summary_preview = summary[:70] + "..."
            else:
                summary_preview = summary
            print(f"Resumen: {summary_preview}\n")
        else:
            print("Resumen: No encontrado.\n")
