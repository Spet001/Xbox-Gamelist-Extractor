### main.py ###
from scraper import get_games_from_gamertagnation

print("=== Xbox Game Recommender ===")
user_id = input("Digite o número após 'u=' na URL do seu perfil do Gamertag Nation: ")

file_name = f"jogos_usuario_{user_id}.txt"

try:
    with open(file_name, "r", encoding="utf-8") as f:
        games = [line.strip() for line in f.readlines() if line.strip()]
        print(f"{len(games)} jogos carregados do arquivo salvo.")
except FileNotFoundError:
    print("Extraindo jogos do perfil...")
    url = f"https://www.gamertagnation.com/member.php?u={user_id}&do=games"
    games = get_games_from_gamertagnation(url)

    if games:
        with open(file_name, "w", encoding="utf-8") as f:
            for game in games:
                f.write(game + "\n")
        print(f"{len(games)} jogos salvos em {file_name}.")
    else:
        print("Nenhum jogo encontrado.")

# Aqui você pode adicionar lógica de recomendação usando os jogos extraídos
print("Jogos extraídos:")
for game in games:
    print("-", game)
