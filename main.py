from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import time
import random
from pynput.keyboard import Key, Controller

# Carregar a lista do arquivo .txt
def carregar_txt(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo.readlines() if linha.strip()]

# Caminho do arquivo de links
arquivo_links = "links/links.txt"

# Caminho do arquivo de páginas
arquivo_paginas = "paginas/paginas.txt"

# Caminho do arquivo botoes.txt
arquivo_botoes = "botoes/botoes.txt"

# Caminho do arquivo titulo.txt    
arquivo_titulos = "titulo/titulo.txt"

# Caminho do arquivo horario.txt    
arquivo_horarios = "horario/horario.txt"

# Carregar a lista de páginas
paginas = carregar_txt(arquivo_paginas)

# Carregar a lista de botões do arquivo
botoes = carregar_txt(arquivo_botoes)

# Carregar os títulos do arquivo
titulos = carregar_txt(arquivo_titulos)

# Carregar os horarios do arquivo
horario = carregar_txt(arquivo_horarios)

# Caminho do ChromeDriver
chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

# Inicia o navegador
browser = webdriver.Chrome(service=service)
browser.maximize_window()

total_paginas = len(paginas)

with open("xpath/xpath.txt", "r", encoding="utf-8") as arquivo:
    xpath_unico = arquivo.readline().strip()

try:
    # Abre o site
    browser.get("https://velocibot.leadsense.com.br/messenger_bot_enhancers/subscriber_broadcast_campaign")

    # Espera explícita para garantir que o campo de e-mail esteja carregado
    wait = WebDriverWait(browser, 10)

    # Preencher e-mail
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
    email_input.send_keys("broademprestimoes.nivaldocliente@gmail.com")

    # Preencher senha
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
    password_input.send_keys("senha@123")

    # Clicar no botão de login
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    # Espera até que a página principal carregue após o login
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Clicar no link de radiodifusão
    radiodifusao_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://velocibot.leadsense.com.br/messenger_bot_broadcast']")))
    radiodifusao_link.click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Clicar no link de transmissão de assinante
    transmissao_assinante_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://velocibot.leadsense.com.br/messenger_bot_enhancers/subscriber_broadcast_campaign']")))
    transmissao_assinante_link.click()

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-toggle='dropdown' and contains(@class, 'dropdown-toggle')]")))
    dropdown.click()
    
    perfil_desejado = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_unico)))
    perfil_nome = perfil_desejado.text.strip()
    perfil_desejado.click()

    # Percorrer os XPaths carregados e criar a campanha
    for pagina_atual in range(total_paginas):
        print(f"\n🔷 Iniciando processo para a página {pagina_atual + 1} de {total_paginas}")

        # Selecionar o perfil pelo XPath carregado
        try:
            # 🔑 Recarregar o botão após a troca de perfil
            time.sleep(2)  # Pequeno delay para garantir atualização do DOM
            criar_campanha_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'create_subscriber_broadcast_campaign')]")))

            # 🔹 Verificar se o botão está visível antes de clicar
            if criar_campanha_botao.is_displayed():
                browser.execute_script("window.scrollTo(0, 0);")
                criar_campanha_botao.click()
                print("Botão 'Criar Campanha' clicado com sucesso.")
            else:
                print("Botão 'Criar Campanha' não está visível.")
                
            # Preencher o campo "Nome da Campanha"
            nome_campanha = f"Campanha_{perfil_nome.replace(' ', '_')}"
            campaign_input = wait.until(EC.presence_of_element_located((By.ID, "campaign_name")))
            campaign_input.clear()
            campaign_input.send_keys(nome_campanha)

            # Espera para a página de criação carregar
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Clicar no dropdown para escolher uma página
            select_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='select2-selection select2-selection--single']")))
            select_dropdown.click()

            if paginas:
                try:
                    # Pegar o primeiro valor da lista de páginas
                    pagina = paginas[pagina_atual]

                    # Esperar o dropdown estar visível
                    wait = WebDriverWait(browser, 10)

                    # Clicar no valor do dropdown usando o perfil selecionado
                    xpath_dropdown = f"//li[contains(text(), '{pagina} [{perfil_nome}]')]"
                    perfil_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dropdown)))
                    perfil_dropdown.click()

                    print(f"✅ Página '{pagina} [{perfil_nome}]' selecionada com sucesso!")

                except Exception as e:
                    print(f"❌ Erro ao processar a página '{pagina} [{perfil_nome}]': {e}")
            else:
                print("⚠️ O arquivo 'paginas.txt' está vazio ou não foi encontrado.")
            
            # 🔑 Selecionar "Account Update" no dropdown
            account_update_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='select2-message_tag-container']")))
            account_update_dropdown.click()

            # Selecionar a opção desejada
            account_update_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Account Update')]")))
            account_update_option.click()
            
            select_element = wait.until(EC.presence_of_element_located((By.ID, "template_type_1")))
            wait.until(EC.element_to_be_clickable((By.ID, "template_type_1")))

            # Tentar selecionar o carrossel com retry
            tentativas = 3
            selecionado = False
            
            for tentativa in range(tentativas):
                try:
                    print(f"Tentativa {tentativa + 1} para selecionar 'carrossel'...")

                    # Abrir o dropdown para garantir visibilidade
                    select_element.click()
                    time.sleep(1)

                    # Selecionar pelo valor
                    select = Select(select_element)
                    select.select_by_value("carousel")
                    print("Opção 'carrossel' foi selecionada com sucesso!")
                    selecionado = True
                    break  # Sai do loop se for bem-sucedido

                except Exception as e:
                    print(f"Falha na tentativa {tentativa + 1}: {e}")
                    time.sleep(2)

            if not selecionado:
                raise Exception("Não foi possível selecionar a opção 'carrossel' após várias tentativas.")
            
            #enviar imagem
            
            try:
                # Esperar o botão de upload estar visível na DOM (mas não necessariamente clicável)
                wait = WebDriverWait(browser, 10)
                input_file = wait.until(EC.presence_of_element_located((By.NAME, "myfile")))

                # Forçar o clique usando JavaScript
                browser.execute_script('document.querySelector("#generic_imageupload_1_1>div>div>form>input").click()')

                print("Botão 'Upload' clicado com sucesso!")

                # Simular entrada do teclado para escolher o arquivo
                imagem = random.randint(1, 13)
                keyboard = Controller()
                time.sleep(1)
                keyboard.type(os.path.join(os.getcwd(), f'imagens\\{imagem}.png'))
                time.sleep(1)
                keyboard.press(Key.enter)
                time.sleep(1)
                keyboard.release(Key.enter)
                time.sleep(2)

            except Exception as e:
                print(f"Erro ao clicar no botão de upload: {e}")
            
            # Esperar o input estar visível e clicável
            try:
                input_link = wait.until(EC.element_to_be_clickable((By.ID, "carousel_image_destination_link_1_1")))

                # Carregar os links do arquivo
                lista_links = carregar_txt(arquivo_links)

                if lista_links:
                    # Escolher um link aleatório
                    link_aleatorio = random.choice(lista_links)
                    print(f"Preenchendo com o link: {link_aleatorio}")

                    # Preencher o campo
                    input_link.clear()
                    input_link.send_keys(link_aleatorio)

                    print("Link preenchido com sucesso!")
                else:
                    print("O arquivo 'links.txt' está vazio ou não foi encontrado.")

            except Exception as e:
                print(f"Erro ao preencher o link: {e}")
                
            # Verificar se existem títulos no arquivo
            if titulos:
                # Escolher um título aleatório
                titulo_aleatorio = random.choice(titulos)
                print(f"Título escolhido: {titulo_aleatorio}")

                try:
                    # Esperar o campo de título estar disponível
                    wait = WebDriverWait(browser, 10)
                    campo_titulo = wait.until(EC.element_to_be_clickable((By.ID, "carousel_title_1_1")))

                    # Preencher o campo de título
                    campo_titulo.clear()
                    campo_titulo.send_keys(titulo_aleatorio)

                    print("Título preenchido com sucesso!")
                except Exception as e:
                    print(f"Erro ao preencher o título: {e}")
            else:
                print("O arquivo 'titulo.txt' está vazio ou não foi encontrado.")
                
            if botoes:
                # Escolher um valor aleatório da lista
                botao_aleatorio = random.choice(botoes)
                print(f"Botão escolhido: {botao_aleatorio}")

                try:
                    # Esperar o campo estar disponível e visível
                    wait = WebDriverWait(browser, 10)
                    campo_botao = wait.until(EC.element_to_be_clickable((By.ID, "carousel_button_text_1_1_1")))

                    # Preencher o campo com o valor aleatório
                    campo_botao.clear()
                    campo_botao.send_keys(botao_aleatorio)

                    print("Campo preenchido com sucesso!")
                except Exception as e:
                    print(f"Erro ao preencher o campo do botão: {e}")
            else:
                print("O arquivo 'botoes.txt' está vazio ou não foi encontrado.")
                
            try:
                # Esperar o campo select estar presente e clicável
                wait = WebDriverWait(browser, 10)
                select_element = wait.until(EC.element_to_be_clickable((By.ID, "carousel_button_type_1_1_1")))

                # Criar um objeto Select para o dropdown
                select = Select(select_element)

                # Selecionar pelo valor (opção mais confiável)
                select.select_by_value("web_url")
                print("Opção 'URL da Web' selecionada com sucesso!")

            except Exception as e:
                print(f"Erro ao selecionar a opção: {e}")
                
            try:
                # Esperar o campo do link da imagem estar presente
                wait = WebDriverWait(browser, 10)
                campo_link_imagem = wait.until(EC.presence_of_element_located((By.ID, "carousel_image_destination_link_1_1")))

                # Capturar o valor do input do link da imagem
                valor_link = campo_link_imagem.get_attribute("value")

                if valor_link:
                    print(f"Valor capturado do campo de link da imagem: {valor_link}")

                    # Esperar o campo do botão estar disponível
                    campo_botao_url = wait.until(EC.presence_of_element_located((By.ID, "carousel_button_web_url_1_1_1")))

                    # Preencher o campo do botão com o valor capturado
                    campo_botao_url.clear()
                    campo_botao_url.send_keys(valor_link)

                    print("Campo do botão preenchido com sucesso!")
                else:
                    print("O campo de link da imagem está vazio.")

            except Exception as e:
                print(f"Erro durante o preenchimento: {e}")
                
            try:
                if horario:
                    # Esperar até que o botão esteja visível e clicável
                    wait = WebDriverWait(browser, 10)
                    botao_agendar_campanha = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='schedule_time_block']/div/label[2]/span[1]")))
                    # Clicar no botão
                    botao_agendar_campanha.click()
                    try:
                        # Esperar o campo de título estar disponível
                        wait = WebDriverWait(browser, 10)
                        campo_agendamento = wait.until(EC.element_to_be_clickable((By.ID, "schedule_time")))

                        # Preencher o campo de título
                        campo_agendamento.clear()
                        campo_agendamento.send_keys(horario)
                        
                        print("Horario preenchido com sucesso!")
                    except Exception as e:
                        print(f"Erro ao preencher o horario: {e}")
                else:
                    print("O campo de horario está vazio.")
            except Exception as e:
                print(f"Erro ao agendar horario: {e}")

            try:
                # Esperar até que o botão esteja visível e clicável
                wait = WebDriverWait(browser, 10)
                botao_criar_campanha = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
                time.sleep(2)
                # Clicar no botão
                browser.execute_script("arguments[0].click();", botao_criar_campanha)

                print("Botão 'Criar Campanha' clicado com sucesso!")

            except Exception as e:
                print(f"Erro ao clicar no botão: {e}")

            print(f"Campanha criada para: {perfil_nome}")
            
            try:
                # Esperar até que o botão 'OK' esteja visível e clicável
                wait = WebDriverWait(browser, 10)
                botao_ok = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal-button--confirm')]")))

                # Clicar no botão
                botao_ok.click()

                print("Botão 'OK' clicado com sucesso!")

            except Exception as e:
                print(f"Erro ao clicar no botão 'OK': {e}")
        
        except Exception as e:
            print(f"Erro ao processar o XPath '{xpath}': {e}")

except Exception as e:
    print(f"Ocorreu um erro geral: {e}")

finally:
    # Fecha o navegador
    browser.quit()
