import tkinter as tk
from tkinter import messagebox, Tk, Label, Button
from PIL import Image, ImageTk
from tkcalendar import Calendar
import customtkinter
from datetime import datetime
import os
import subprocess

# Tamanhos da janela
TAMANHO_INICIAL = "300x150"  # Tamanho inicial da janela
TAMANHO_EXPANDIDO = "300x450"  # Tamanho expandido da janela

def agendar():
    # Verificar se o Checkbutton está ativado
    if not var.get():
        # Se não estiver ativado, salvar valor vazio no arquivo
        salvar_horario("")
        messagebox.showinfo("Agendamento", "Checkbox desativado. Valor vazio salvo em horario.txt.")
        return
    
    # Se o Checkbutton estiver ativado, prosseguir com o agendamento
    # Obter a data selecionada no calendário
    date_str = cal.get_date()  # Retorna no formato 'MM/DD/YY'
    
    # Converter a data para o formato datetime
    try:
        # Adicionar lógica para corrigir o ano de dois dígitos
        if len(date_str.split('/')[-1]) == 2:  # Verifica se o ano tem dois dígitos
            date_str = date_str[:-2] + '20' + date_str[-2:]  # Converte 'YY' para '20YY'
        
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')  # Formato corrigido
    except ValueError as e:
        messagebox.showerror("Erro", f"Formato de data inválido: {e}")
        return
    
    # Obter o horário inserido pelo usuário
    time_str = entry_horario.get()  # Espera-se que o usuário insira no formato 'HH:MM'
    
    if date_str and time_str:
        try:
            # Validar o horário inserido
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            # Combinar data e horário
            datetime_final = datetime.combine(date_obj, time_obj)
            # Formatar no padrão desejado
            datetime_formatado = datetime_final.strftime('%Y-%m-%d %H:%M:%S')
            
            # Salvar o horário no arquivo
            salvar_horario(datetime_formatado)
            messagebox.showinfo("Agendamento", f"Agendamento salvo com sucesso!\n{datetime_formatado}")
        except ValueError:
            messagebox.showerror("Erro", "Formato de horário inválido! Use HH:MM.")
    else:
        # Se não houver data e horário, salvar valor vazio
        salvar_horario("")
        messagebox.showwarning("Agendamento", "Nenhuma data e horário selecionados. Valor vazio salvo em horario.txt.")

def salvar_horario(horario):
    # Definir o caminho da pasta /horario
    pasta_horario = "horario"
    # Criar a pasta se ela não existir
    if not os.path.exists(pasta_horario):
        os.makedirs(pasta_horario)
    
    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_horario, "horario.txt")
    
    # Salvar no arquivo
    with open(caminho_arquivo, "w") as file:
        file.write(horario)

def expandir_calendario():
    if var.get():
        # Expandir a janela
        root.geometry(TAMANHO_EXPANDIDO)
        # Mostrar o calendário e os campos de horário
        cal.pack(pady=20)
        label_horario.pack()
        entry_horario.pack()
        button_agendar.pack(pady=10)
    else:
        # Reduzir a janela ao tamanho inicial
        root.geometry(TAMANHO_INICIAL)
        # Ocultar o calendário e os campos de horário
        cal.pack_forget()
        label_horario.pack_forget()
        entry_horario.pack_forget()
        button_agendar.pack_forget()

def executar_codigo():
    # Verificar se o Checkbutton está ativado
    if not var.get():
        # Se o Checkbutton estiver desativado, salvar valor vazio no arquivo
        salvar_horario("")
        messagebox.showinfo("Executar", "Checkbox desativado. Valor vazio salvo em horario.txt.")
    else:
        # Se o Checkbutton estiver ativado, apenas exibir o horário agendado
        caminho_arquivo = os.path.join("horario", "horario.txt")
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r") as file:
                horario_agendado = file.read()
            messagebox.showinfo("Horário Agendado", f"Horário agendado:\n{horario_agendado}")
        else:
            messagebox.showinfo("Horário Agendado", "Nenhum horário agendado encontrado.")
    
    # Executar o arquivo main.py
    caminho_main = "main.py"  # Substitua pelo caminho correto se necessário
    
    if not os.path.exists(caminho_main):
        messagebox.showerror("Erro", f"Arquivo {caminho_main} não encontrado!")
        return
    
    try:
        subprocess.run(["python", caminho_main], check=True)
        messagebox.showinfo("Executar", f"Arquivo {caminho_main} executado com sucesso!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao executar {caminho_main}:\n{e}")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Python não encontrado. Certifique-se de que o Python está instalado e no PATH.")

caminho_atual = os.getcwd()
titulo = os.path.basename(caminho_atual)

root = tk.Tk()
root.title(titulo)
root.geometry(TAMANHO_INICIAL)
root.resizable(False, False)

# Variável para o Checkbutton
var = tk.BooleanVar()

# Checkbutton para expandir o calendário
check_agendar = tk.Checkbutton(root, text="Agendar", variable=var, command=expandir_calendario)
check_agendar.pack(pady=20)

# Obter a data atual
hoje = datetime.now()
ano_atual = hoje.year
mes_atual = hoje.month
dia_atual = hoje.day

# Calendário configurado para abrir na data atual
cal = Calendar(root, selectmode='day', year=ano_atual, month=mes_atual, day=dia_atual)

cal.configure(background="lightgray", foreground="black")

# Entrada para o horário
label_horario = tk.Label(root, text="Horário (HH:MM):")
entry_horario = tk.Entry(root)

# Botão para salvar o agendamento
button_agendar = customtkinter.CTkButton(root, text="Salvar Agendamento", command=agendar, corner_radius=20, font=("undefined", 16))

# Botão para executar código
button_executar = customtkinter.CTkButton(root, text="Executar", command=executar_codigo, corner_radius=20, font=("undefined", 16))
button_executar.pack(pady=20)

# Iniciar a interface
root.mainloop()