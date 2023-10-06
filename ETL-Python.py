import pandas as pd
import requests
import openai
import tkinter as tk

openai_api_key = "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"
openai.api_key = openai_api_key
sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"

# Leitura dos IDs do arquivo CSV
df = pd.read_csv("sdw2023.csv")
user_ids = df["UserID"].tolist()

def get_user_by_id(user_id):
    response = requests.get(f"{sdw2023_api_url}/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Buscar informações dos usuários na API usando os IDs do CSV
users = [get_user_by_id(user_id) for user_id in user_ids if get_user_by_id(user_id) is not None]

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Dicas sobre investimentos conservadores.",
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} fornecendo dicas sobre investimentos conservadores(máximo de 120 caracteres)",
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return response.status_code == 200

def on_generate_news():
    user_name = user_name_entry.get()
    user = next((u for u in users if u['name'] == user_name), None)
    if user is not None:
        news = generate_ai_news(user)
        user['news'].append({
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news
        })
        success = update_user(user)
        output_text.set(f"Dicas financeiras para {user['name']}: {news}\nUsuario {user['name']} Atualizado com sucesso! {success}")
    else:
        output_text.set(f"Usuario com o '{user_name}' not found!")

# Create the main window
root = tk.Tk()
root.title("Dicas fincanceiras personalizadas")
root.geometry("920x130")

# Create and configure input elements
user_name_label = tk.Label(root, text="Nome de Usuario:")
user_name_label.pack()
user_name_entry = tk.Entry(root)
user_name_entry.pack()

generate_button = tk.Button(root, text="Gerar dicas personalizadas", command=on_generate_news)
generate_button.pack()

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text)
output_label.pack()

# Start the GUI event loop
root.mainloop()
