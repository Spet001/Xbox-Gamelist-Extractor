from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_games_from_gamertagnation(url, driver_path="chromedriver.exe"):
    options = Options()
    # options.add_argument("--headless")  # DESATIVADO para debugar
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    all_games = []  # Lista para armazenar todos os jogos encontrados
    page_number = 1  # Página inicial
    game_counter = 1  # Contador para os jogos numerados

    # Obter o total de jogos
    driver.get(url)
    time.sleep(3)  # Esperar a página carregar
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")
    
    total_games = int(soup.select_one('h2 small.badge').text.strip())  # Total de jogos
    print(f"Total de jogos: {total_games}.")

    while game_counter <= total_games:
        print(f"Acessando página {page_number}...")
        driver.get(f"{url}&page={page_number}")
        time.sleep(5)  # Tempo maior para garantir o carregamento

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")

        game_titles = soup.select("h4.card-title a")
        print(f"Encontrados {len(game_titles)} jogos na página {page_number}.")

        if not game_titles:  # Se não houver mais jogos, saímos do loop
            break

        for link in game_titles:
            all_games.append(link.text.strip())
            game_counter += 1  # Aumenta o contador a cada jogo encontrado
            if game_counter > total_games:  # Se atingirmos o total de jogos, interrompe
                break

        page_number += 1  # Passa para a próxima página

    driver.quit()

    return all_games
