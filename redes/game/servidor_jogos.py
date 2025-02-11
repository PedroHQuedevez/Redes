import random
import socket
import threading

# Configuração do servidor
HOST = '0.0.0.0'
PORT = 65432

target_number = random.randint(1, 100)
print(f"Número secreto gerado: {target_number}")

clients = {}
turns_list = []
lock = threading.Lock()
guessed_numbers = []

# Função para enviar mensagens para um cliente específico
def send_message(client, message):
    try:
        client.sendall(message.encode())
    except:
        remove_player(client)

# Função para enviar mensagens para todos os clientes
def broadcast(message):
    for client in list(clients.values()):
        send_message(client, message)

# Função para atualizar a ordem dos turnos
def update_turn():
    global turns_list
    if turns_list:
        turns_list.append(turns_list.pop(0))
    if turns_list:
        next_player = turns_list[0]
        
        broadcast(f"Agora é a vez do Jogador {next_player}.\n")
        broadcast(f"Números já tentados: {', '.join(map(str, guessed_numbers))}\n")

# Função para remover um jogador
def remove_player(client):
    global turns_list, clients
    with lock:
        player_id = None
        for pid, c in clients.items():
            if c == client:
                player_id = pid
                break
        if player_id is not None:
            del clients[player_id]
            turns_list.remove(player_id)
            broadcast(f"O jogador {player_id} saiu do jogo.\n")
            update_turn()
    client.close()

# Função para lidar com um cliente
def handle_client(conn, addr, player_id):
    global target_number, guessed_numbers

    with lock:
        clients[player_id] = conn
        turns_list.append(player_id)
    
    print(f"Nova conexão: {addr} como Jogador {player_id}")
    send_message(conn, f"Bem-vindo ao jogo, Jogador {player_id}! Adivinhe um número entre 1 e 100.\n")

    while True:
        with lock:
            if turns_list[0] != player_id:
                continue
        
        send_message(conn, "Sua vez de jogar! Digite um número ou 'sair'.\n")
        try:
            guess = conn.recv(1024).decode().strip()
            print(f"Jogador {player_id} enviou: {guess}")  # Adicionando debug
            if not guess:
                break
            
            if guess.lower() == 'sair':
                send_message(conn, "Você saiu do jogo. Até mais!\n")
                break
            
            if not guess.isdigit():
                send_message(conn, "Número inválido. Tente novamente.\n")
                continue
            
            guess = int(guess)
            guessed_numbers.append(guess)
            
            if guess < target_number:
                broadcast(f"O jogador {player_id} tentou {guess}. Muito baixo.\n")
            elif guess > target_number:
                broadcast(f"O jogador {player_id} tentou {guess}. Muito alto.\n")
            else:
                broadcast(f"Parabéns! O jogador {player_id} acertou o número {target_number}! Reiniciando...\n")
                target_number = random.randint(1, 100)
                guessed_numbers.clear()
                print(f"Novo número secreto: {target_number}")
            
            update_turn()
        except Exception as e:
            print(f"Erro ao receber dado de Jogador {player_id}: {e}")  # Adicionando debug
            break

    remove_player(conn)

# Inicialização do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Servidor rodando em {HOST}:{PORT}")

player_id = 0
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
    thread.start()
    player_id += 1
