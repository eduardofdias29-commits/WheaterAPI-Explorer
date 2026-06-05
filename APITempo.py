import os
import customtkinter as ctk
import requests
from dotenv import load_dotenv

load_dotenv()
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")

PALETA_GELADA = {
    "fundo_janela": "#020b14",
    "fundo_card": "#091a29", 
    "borda_card": "#1b3a4b",
    "texto_destaque": "#3a8ebb",
    "border_inputs": "#162a3b",
    "botao": "#2563eb",
    "botao_hover": "#1d4ed8"
}

PALETA_QUENTE = {
    "fundo_janela": "#120600",
    "fundo_card": "#240f04",
    "borda_card": "#4a2306",
    "texto_destaque": "#f39c12",
    "border_inputs": "#2e1605",
    "botao": "#d35400",  
    "botao_hover": "#a04000"
}

class WeatherPremiumExplorer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weather API Explorer")
        self.geometry("460x650")
        self.resizable(False, False)
        
        self.cores_atuais = PALETA_QUENTE
        self.configure(fg_color=self.cores_atuais["fundo_janela"])

        self.label_titulo = ctk.CTkLabel(
            self, 
            text="☀️ WEATHER EXPLORER", 
            font=("Segoe UI", 14, "bold"),
            text_color=self.cores_atuais["texto_destaque"],
            fg_color="transparent",
            height=35
        )
        self.label_titulo.pack(pady=(30, 15))

        self.entry_cidade = ctk.CTkEntry(
            self, 
            placeholder_text="Cidade: (Ex: Sorocaba)", 
            width=360,
            height=45,
            corner_radius=12,
            fg_color="#0f0f0f",
            border_color=self.cores_atuais["border_inputs"],
            text_color="#FFFFFF",
            font=("Segoe UI", 14)
        )
        self.entry_cidade.pack(pady=8)
        self.entry_cidade.bind("<Return>", lambda event: self.buscar_clima())

        self.entry_pais = ctk.CTkEntry(
            self, 
            placeholder_text="País: (Opcional, Ex: BR)", 
            width=360,
            height=45,
            corner_radius=12,
            fg_color="#0f0f0f",
            border_color=self.cores_atuais["border_inputs"],
            text_color="#FFFFFF",
            font=("Segoe UI", 14)
        )
        self.entry_pais.pack(pady=8)
        self.entry_pais.bind("<Return>", lambda event: self.buscar_clima())

        self.btn_buscar = ctk.CTkButton(
            self, 
            text="BUSCAR CLIMA", 
            command=self.buscar_clima, 
            fg_color=self.cores_atuais["botao"], 
            hover_color=self.cores_atuais["botao_hover"],
            text_color="white",
            font=("Segoe UI", 14, "bold"),
            width=360,
            height=45,
            corner_radius=20
        )
        self.btn_buscar.pack(pady=20)

        self.card_resultado = ctk.CTkFrame(
            self, 
            fg_color=self.cores_atuais["fundo_card"], 
            border_color=self.cores_atuais["borda_card"],
            border_width=1,
            corner_radius=18,
            width=360,
            height=250
        )
        self.card_resultado.pack(pady=10, padx=40, fill="both", expand=True)
        self.card_resultado.pack_propagate(False)

        self.label_card_header = ctk.CTkLabel(
            self.card_resultado,
            text="DETALHES DO CLIMA",
            font=("Segoe UI", 12, "bold"),
            text_color="#888888"
        )
        self.label_card_header.pack(pady=(15, 5))

        self.grid_container = ctk.CTkFrame(self.card_resultado, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.grid_container.columnconfigure(0, weight=1)
        self.grid_container.columnconfigure(1, weight=1)
        self.grid_container.columnconfigure(2, weight=1)

        self.label_emoji = ctk.CTkLabel(self.grid_container, text="✨", font=("Segoe UI", 64))
        self.label_emoji.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.label_temp_titulo = ctk.CTkLabel(self.grid_container, text="Temperatura", font=("Segoe UI", 11), text_color="#aaaaaa")
        self.label_temp_titulo.grid(row=0, column=1, columnspan=2, sticky="sw", padx=10)

        self.label_temp_valor = ctk.CTkLabel(self.grid_container, text="--°C", font=("Segoe UI", 36, "bold"), text_color="#ffffff")
        self.label_temp_valor.grid(row=1, column=1, columnspan=2, sticky="nw", padx=10)

        self.label_condicao = ctk.CTkLabel(self.grid_container, text="Aguardando...", font=("Segoe UI", 13, "bold"), text_color="#ffffff")
        self.label_condicao.grid(row=2, column=0, pady=(20, 0), sticky="w")

        self.label_humidade = ctk.CTkLabel(self.grid_container, text="Umidade\n--", font=("Segoe UI", 12), text_color="#aaaaaa", justify="left")
        self.label_humidade.grid(row=2, column=1, pady=(20, 0), sticky="w", padx=10)

        self.label_vento = ctk.CTkLabel(self.grid_container, text="Vento\n--", font=("Segoe UI", 12), text_color="#aaaaaa", justify="left")
        self.grid_container.rowconfigure(2, weight=1)
        self.label_vento.grid(row=2, column=2, pady=(20, 0), sticky="w", padx=10)

    def aplicar_design_dinamico(self, temp, condicao_texto):
        self.cores_atuais = PALETA_GELADA if temp < 18 else PALETA_QUENTE
        emoji_clima = "❄️" if temp < 18 else "☀️"
        titulo_texto = "❄️ CLIMA GELADO" if temp < 18 else "☀️ CLIMA QUENTE"

        self.configure(fg_color=self.cores_atuais["fundo_janela"])
        self.label_titulo.configure(text=titulo_texto, text_color=self.cores_atuais["texto_destaque"])
        
        self.entry_cidade.configure(border_color=self.cores_atuais["border_inputs"])
        self.entry_pais.configure(border_color=self.cores_atuais["border_inputs"])
        
        self.btn_buscar.configure(fg_color=self.cores_atuais["botao"], hover_color=self.cores_atuais["botao_hover"])
        
        self.card_resultado.configure(
            fg_color=self.cores_atuais["fundo_card"], 
            border_color=self.cores_atuais["borda_card"]
        )

        signo_temp = "+" if temp > 0 else ""
        self.label_emoji.configure(text=emoji_clima)
        self.label_temp_valor.configure(text=f"{signo_temp}{int(temp)}°C")
        self.label_condicao.configure(text=condicao_texto)

    def buscar_clima(self):
        cidade = self.entry_cidade.get().strip()
        pais = self.entry_pais.get().strip()

        if not cidade:
            self.label_condicao.configure(text="Digite uma cidade!")
            return

        local_busca = f"{cidade},{pais}" if pais else cidade
        url = f"https://api.openweathermap.org/data/2.5/weather?q={local_busca}&appid={WEATHER_TOKEN}&units=metric&lang=pt_br"

        try:
            resposta = requests.get(url)
            dados = resposta.json()

            if dados.get("cod") == 200:
                temp = dados["main"]["temp"]
                humidade = dados["main"]["humidity"]
                vento = dados["wind"]["speed"]
                descricao = dados["weather"][0]["description"].capitalize()
                
                self.aplicar_design_dinamico(temp, descricao)

                self.label_humidade.configure(text=f"Umidade\n{humidade}%", text_color="#ffffff")
                self.label_vento.configure(text=f"Vento\n{int(vento * 3.6)} km/h", text_color="#ffffff")
            else:
                self.label_condicao.configure(text="Não encontrado!")

        except Exception as e:
            self.label_condicao.configure(text="Erro de conexão!")

if __name__ == "__main__":
    app = WeatherPremiumExplorer()
    app.mainloop()