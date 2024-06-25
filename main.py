import os, time, subprocess, psutil
import customtkinter as ctk

server_ip_old = "192.168.3.250"

if os.path.exists('C:/Program Files (x86)/RustDesk'):
    print("É X86")
    rustdesk_app = "C:/Program Files (x86)/RustDesk/rustdesk.exe"
elif os.path.exists('C:/Program Files/RustDesk'):
    print("É X64")
    rustdesk_app = "C:/Program Files/RustDesk/rustdesk.exe"


#o python não reconhece as variaveis de ambiente do Windows, por conta disso a linha 8 será usada para tratar esse erro
directory_file_pre = r"%appdata%/RustDesk/config/RustDesk2.toml"
directory_file = os.path.expandvars(directory_file_pre)


def terminate_rustdesk_processes():
    # Percorre todos os processos ativos
    print("Finalizando os processos do rustdesk")
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            # Verifica se "rustdesk" está no nome do processo ou no comando executado
            if 'rustdesk' in proc.info['name']:
                print(f"Finalizando processo {proc.info['name']} (PID: {proc.info['pid']})")
                proc.terminate()  # Tenta finalizar o processo
                proc.wait(timeout=5)  # Espera até 5 segundos para que o processo finalize
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Erro ao tentar finalizar processo: {e}")


def button_rust_stop():
    print("abrindo o rustdesk")
    os.popen(rustdesk_app)
    print("iniciando serviço para possibilitar para-lo")
    result_stop = subprocess.run('NET START "RustDesk Service"', shell=True, capture_output=True, text=True)
    #os.popen('NET START "RustDesk Service"')
    time.sleep(3)
    #os.popen('NET STOP "RustDesk Service"')
    print("Parando o serviço do Rust")
    result_stop = subprocess.run('NET STOP "RustDesk Service"', shell=True, capture_output=True, text=True)
    time.sleep(2)
    terminate_rustdesk_processes()


def button_rust_start():
    result_stop = subprocess.run(rustdesk_app, shell=True, capture_output=True, text=True)
    time.sleep(4)
    result_stop = subprocess.run('NET START "RustDesk Service"', shell=True, capture_output=True, text=True)
    #os.popen('NET START "RustDesk Service"')

def update_linha(lista, item_a_procurar, item_a_substituir):
    item_encontrado = False
    # Percorre a lista para procurar o item especificado
    for i, item in enumerate(lista):
        if item_a_procurar in item:
            print(f'Será feito mudanças no: {item_a_procurar}')
            # Substitui a ocorrência do item encontrado pelo item a substituir
            lista[i] = item_a_substituir
            item_encontrado = True
            break
    # Se não encontrou o item, adiciona o item a adicionar ao final
    if not item_encontrado:
        lista.append(item_a_substituir)
        print(f'foi adicionado a linha: {item_a_substituir}')
    return lista


def button_up():
    #replace foi necessário pois o input vem com quebra de linha
    new_ip = str(input_ip.get("0.0", "end")).replace('\n','')
    # Abra o arquivo e leia seu conteúdo
    print(f'Abrindo arquivo: {directory_file}')
    with open(directory_file, 'r') as file:
        linhas = file.readlines()

    lista = update_linha(lista=linhas, item_a_procurar='rendezvous_server', item_a_substituir=f"rendezvous_server = '{new_ip}:21116'\n")
    lista = update_linha(lista=linhas, item_a_procurar='custom-rendezvous', item_a_substituir=f"custom-rendezvous-server = '{new_ip}'\n")
    lista = update_linha(lista=linhas, item_a_procurar='nat_type', item_a_substituir=f"nat_type = 2\n")
    lista = update_linha(lista=linhas, item_a_procurar='key =', item_a_substituir=f"key = '4bhxkWdg4LmpObdoWtuDBS4BhLPThExE8N040OEdPHE='\n")
    lista = update_linha(lista=linhas, item_a_procurar='relay-server', item_a_substituir=f"relay-server = '{new_ip}'\n")
    

    # Salve as linhas modificadas de volta no arquivo
    with open(directory_file, 'w') as file:
        file.writelines(linhas)
    print(f'Arquivo "{directory_file}" modificado com sucesso.')


################################################################# PARTE VISUAL #################################################################
janela = ctk.CTk()
janela.geometry("300x300")
janela.title("Instalador Anydesk")
janela.resizable(width=False, height=False)
janela._set_appearance_mode("dark")

label_title = ctk.CTkLabel(janela, text="Só funciona se for executado \nem modo Administrador", fg_color="transparent").pack()
button = ctk.CTkButton(janela, width=50, text="Rust  Stop", fg_color="red", hover_color="black", command=button_rust_stop).place(x=120, y=50)

label = ctk.CTkLabel(janela, text="Endereço IP:", fg_color="transparent").place(x=10, y=90)
input_ip = ctk.CTkTextbox(janela, width=140, height=20)
input_ip.place(x=100, y=90)
input_ip.insert("0.0", server_ip_old)
button = ctk.CTkButton(janela, width=50, text="Up", command=button_up).place(x=245, y=90)


button = ctk.CTkButton(janela, width=50, text="Rust Start", fg_color="green", hover_color="black", command=button_rust_start).place(x=120, y=130)

frame_status = ctk.CTkFrame(master=janela, width=290, height=130).place(x=5, y=165)

janela.mainloop()

#para criar o arquivo EXE
# pyinstaler main.py --onefile
