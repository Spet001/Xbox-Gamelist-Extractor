import tkinter as tk
from tkinter import messagebox
import os
from scraper import get_games_from_gamertagnation, get_games_from_psnprofiles

def extrair_jogos_xbox():
    user_id = entry_id.get().strip()
    if not user_id:
        messagebox.showerror("Erro", "Por favor, insira seu ID do Gamertag Nation (número após 'u=').")
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

    txt_resultado.delete("1.0", tk.END)
    for game in games:
        txt_resultado.insert(tk.END, f"- {game}\n")


def extrair_jogos_psn():
    username = entry_id.get().strip()
    if not username:
        messagebox.showerror("Erro", "Por favor, insira seu nome de usuário da PSN.")
        return

    file_name = f"jogos_psn_{username}.txt"

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            games = [line.strip() for line in f.readlines() if line.strip()]
        messagebox.showinfo("Sucesso", f"{len(games)} jogos carregados do arquivo salvo.")
    else:
        games = get_games_from_psnprofiles(username)

        if games:
            with open(file_name, "w", encoding="utf-8") as f:
                for game in games:
                    f.write(game + "\n")
            messagebox.showinfo("Sucesso", f"{len(games)} jogos extraídos e salvos.")
        else:
            messagebox.showwarning("Aviso", "Nenhum jogo encontrado.")
            return

    txt_resultado.delete("1.0", tk.END)
    for game in games:
        txt_resultado.insert(tk.END, f"- {game}\n")


# Interface gráfica com Tkinter
janela = tk.Tk()
janela.title("Xbox Gamelist Extractor")
janela.geometry("500x600")

label = tk.Label(janela, text="Insira seu ID (número da Gamertag Nation ou nome PSN):")
label.pack(pady=10)

entry_id = tk.Entry(janela, width=40)
entry_id.pack()

label_opcoes = tk.Label(janela, text="Extrair lista de jogos:")
label_opcoes.pack(pady=10)

btn_extrair_xbox = tk.Button(janela, text="Xbox", command=extrair_jogos_xbox, width=25)
btn_extrair_xbox.pack(pady=2)

btn_extrair_psn = tk.Button(janela, text="PSN", command=extrair_jogos_psn, width=25)
btn_extrair_psn.pack(pady=2)

btn_extrair_steam = tk.Button(janela, text="Steam (WIP)", state="disabled", width=25)
btn_extrair_steam.pack(pady=2)

txt_resultado = tk.Text(janela, height=25, width=58)
txt_resultado.pack(pady=10)

janela.mainloop()
