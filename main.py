### main.py ###
import tkinter as tk
from tkinter import messagebox, scrolledtext
from scraper import get_games_from_gamertagnation
import os

def extrair_jogos():
    user_id = entry_id.get().strip()
    if not user_id.isdigit():
        messagebox.showerror("Erro", "Por favor, insira apenas números no ID do perfil.")
        return

    file_name = f"jogos_usuario_{user_id}.txt"

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            games = [line.strip() for line in f.readlines() if line.strip()]
        messagebox.showinfo("Sucesso", f"{len(games)} jogos carregados do arquivo salvo.")
    else:
        url = f"https://www.gamertagnation.com/member.php?u={user_id}&do=games"
        games = get_games_from_gamertagnation(url)

        if games:
            with open(file_name, "w", encoding="utf-8") as f:
                for game in games:
                    f.write(game + "\n")
            messagebox.showinfo("Sucesso", f"{len(games)} jogos extraídos e salvos.")
        else:
            messagebox.showwarning("Aviso", "Nenhum jogo encontrado.")
            return

    # Mostra os jogos extraídos na interface
    txt_resultado.delete("1.0", tk.END)
    for game in games:
        txt_resultado.insert(tk.END, f"- {game}\n")

# Criação da interface
janela = tk.Tk()
janela.title("Xbox Gamelist Extractor")

lbl_instrucao = tk.Label(janela, text="Digite o número após 'u=' na URL do seu perfil do Gamertag Nation:")
lbl_instrucao.pack(pady=5)

entry_id = tk.Entry(janela, width=30)
entry_id.pack()

btn_extrair = tk.Button(janela, text="Extrair Jogos", command=extrair_jogos)
btn_extrair.pack(pady=10)

txt_resultado = scrolledtext.ScrolledText(janela, width=60, height=20)
txt_resultado.pack(padx=10, pady=10)

janela.mainloop()
