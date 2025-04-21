from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def get_games_from_gamertagnation(url, driver_path="chromedriver.exe"):
    options = Options()
    # options.add_argument("--headless")  # Desativado para debug
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    all_games = []
    page_number = 1
    total_expected = None

    try:
        while True:
            print(f"Acessando página {page_number}...")
            driver.get(f"{url}&page={page_number}")
            time.sleep(4)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            if total_expected is None:
                badge = soup.select_one("h2 > small.badge")
                if badge:
                    total_expected = int(badge.text.strip())

            game_titles = soup.select("h4.card-title a")
            print(f"Encontrados {len(game_titles)} jogos na página {page_number}.")

            if not game_titles:
                break

            for link in game_titles:
                title = link.text.strip()
                if title not in all_games:
                    all_games.append(title)

            if total_expected and len(all_games) >= total_expected:
                break

            page_number += 1

    finally:
        driver.quit()

    return all_games


def get_games_from_psnprofiles(username, driver_path="chromedriver.exe"):
    options = Options()
    # options.add_argument("--headless")  # Ative para deixar invisível
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    url = f"https://psnprofiles.com/{username}"
    print(f"Acessando {url}")
    driver.get(url)
    time.sleep(2)

    # Scroll infinito até o fim da página
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse final da página carregada
    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles = soup.select("a.title")

    all_games = []
    for t in titles:
        game_title = t.text.strip()
        if game_title and game_title not in all_games:
            all_games.append(game_title)

    driver.quit()

    return all_games
