import requests
from bs4 import BeautifulSoup
import unicodedata
import tkinter as tk
from tkinter import messagebox, ttk

# URLs
URLS = {
    "relegation_teams": "https://www.mat.ufmg.br/futebol/rebaixamento_seriea/",
    "relegation_points": "https://www.mat.ufmg.br/futebol/rebaixamento_pontseriea/",
    "classification": "https://www.mat.ufmg.br/futebol/classificacao-geral_seriea/"
}

# Função para normalizar strings removendo acentos
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper()

# Função para buscar e processar dados
def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [data.getText() for data in soup.find_all(name="td")]

# Coletar dados
def collect_data():
    team_probabilities = fetch_data(URLS["relegation_teams"])
    point_probabilities = fetch_data(URLS["relegation_points"])
    classification_data = fetch_data(URLS["classification"])
    
    # Processar dados de rebaixamento por time
    teams = team_probabilities[1::3]
    probabilities = team_probabilities[2::3]
    dict_probabilities_relegation_teams = dict(zip(teams, probabilities))
    
    # Processar dados de rebaixamento por pontuação
    points = point_probabilities[0::2]
    point_probs = point_probabilities[1::2]
    dict_probabilities_relegation_points = dict(zip(points, point_probs))

    # Processar dados da classificação
    teams_list = []
    for i in range(0, len(classification_data), 11):
        team_data = classification_data[i:i+11]
        teams_list.append(Team(*team_data))
    
    return dict_probabilities_relegation_teams, dict_probabilities_relegation_points, teams_list

# Classe Time
class Team:
    def __init__(self, position, name, points, games, wins, draws, losses, goals_for, goals_against, goal_difference, efficiency):
        self.position = int(position)
        self.name = name
        self.points = int(points)
        self.games = int(games)
        self.wins = int(wins)
        self.draws = int(draws)
        self.losses = int(losses)
        self.goals_for = int(goals_for)
        self.goals_against = int(goals_against)
        self.goal_difference = int(goal_difference)
        self.efficiency = float(efficiency)

# Função para calcular a diferença e as vitórias/empates
def calculate_difference_and_wins_draws():
    result_text.delete(1.0, tk.END)
    team_name = combobox_team.get().strip()
    normalized_team_name = normalize_string(team_name)

    # Busca o time na lista
    found_team = next((team for team in teams if normalize_string(team.name) == normalized_team_name), None)
    
    if found_team:
        try:
            minimum_points = int(entry_points.get())
            difference = minimum_points - found_team.points
            
            # Adiciona a probabilidade de rebaixamento ao resultado
            relegation_probability = dict_probabilities_relegation_teams.get(found_team.name, "N/A")
            
            if found_team.points > minimum_points:
                result = (f"O {found_team.name} tem {found_team.points} pontos, "
                          f"o que é mais do que os {minimum_points} pontos mínimos. "
                          "Portanto, não há risco de rebaixamento.")
            else:
                result = (f"A diferença entre {minimum_points} pontos e os pontos atuais do "
                          f"{found_team.name} ({found_team.points} pontos) é: {difference}\n")
                
                remaining_games = 38 - found_team.games
                points_needed = minimum_points - found_team.points + 1
                results = []

                for wins in range(remaining_games + 1):
                    for draws in range(remaining_games - wins + 1):
                        if wins + draws <= remaining_games:
                            calculated_points = 3 * wins + draws
                            if calculated_points >= points_needed:
                                results.append((wins, draws))

                if results:
                    result += f"\nCombinações de vitórias e empates necessárias para o {found_team.name}:\n"
                    for w, d in results:
                        result += f" - {w} vitórias e {d} empates\n"
                else:
                    result += f"{found_team.name} não pode alcançar mais de {minimum_points} pontos com os jogos restantes."

            # Adiciona a probabilidade de rebaixamento ao resultado
            result += f"\nProbabilidade de rebaixamento: {relegation_probability}%"
            
            result_text.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido para os pontos mínimos.")
    else:
        messagebox.showerror("Erro", "Time não encontrado. Verifique o nome digitado.")

# Coleta de dados
dict_probabilities_relegation_teams, dict_probabilities_relegation_points, teams = collect_data()

# Criação da interface gráfica
root = tk.Tk()
root.title("Cálculo de Pontos e Combinações")

# Labels e entradas
tk.Label(root, text="Escolha o Time:").pack()

# Combobox para seleção do time
combobox_team = ttk.Combobox(root, values=[team.name for team in teams])
combobox_team.pack()

tk.Label(root, text="Pontos Mínimos:").pack()
entry_points = tk.Entry(root)
entry_points.pack()

# Botão para calcular
tk.Button(root, text="Calcular", command=calculate_difference_and_wins_draws).pack()

# Área de texto para mostrar os resultados
result_text = tk.Text(root, height=50, width=150)
result_text.pack()

# Iniciar a interface
root.mainloop()
