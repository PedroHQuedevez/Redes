import random
import socket
import threading

#fazer um client

# Configuração do servidor
HOST = '0.0.0.0'
PORT = 65432

# Número a ser adivinhado
target_number = random.randint(1, 100)
print(f"Número secreto gerado: {target_number}")

clients = []
turns_list = []  # Lista que mantém a ordem dos turnos
lock = threading.Lock()
player_waiting = set()
guessed_numbers = []

# Função para lidar com um cliente
def handle_client(conn, addr, player_id):
    global target_number, player_waiting, guessed_numbers

    print(f"Nova conexão: {addr} como Jogador {player_id}")
    conn.sendall(f"Bem-vindo ao jogo de adivinhação, Jogador {player_id}! Tente adivinhar o número entre 1 e 100.\n".encode())

    while True:
        try:
            with lock:
                if turns_list[0] != player_id:
                    if player_id not in player_waiting:
                        conn.sendall("Aguarde sua vez.\n".encode())
                        player_waiting.add(player_id)
                    continue
                player_waiting.discard(player_id)

            guess = conn.recv(1024).decode().strip()
            if not guess:
                break

            if not guess.isdigit():
                conn.sendall("Por favor, envie um número válido.\n".encode())
                continue
            
            conn.sendall("Sua vez de jogar\n".encode())
            guess = int(guess)
            guessed_numbers.append(guess)

            if guess < target_number:
                broadcast(f"O jogador {player_id} tentou o número {guess}. Muito baixo.\n")
            elif guess > target_number:
                broadcast(f"O jogador {player_id} tentou o número {guess}. Muito alto.\n")
            else:
                broadcast(f"Parabéns! O jogador {player_id} acertou o número {target_number}! Reiniciando o jogo...\n")
                target_number = random.randint(1, 100)
                guessed_numbers.clear()
                print(f"Novo número secreto: {target_number}")

            with lock:
                update_turn()

        except:
            break

    with lock:
        remove_player(conn, player_id)

    conn.close()
    print(f"Conexão encerrada: {addr}")

# Função para atualizar a ordem dos turnos
def update_turn():
    global turns_list
    if turns_list:
        turns_list.append(turns_list.pop(0))  # Move o primeiro jogador para o final
    if turns_list:
        broadcast(f"Agora é a vez do Jogador {turns_list[0]}.\n")
        broadcast(f"Números já tentados: {', '.join(map(str, guessed_numbers))}\n\n")

# Função para remover um jogador
def remove_player(conn, player_id):
    global clients, turns_list
    clients = [(c, p) for c, p in clients if p != player_id]
    turns_list = [p for p in turns_list if p != player_id]
    
    broadcast(f"O jogador {player_id} saiu do jogo.\n")
    
    if turns_list:
        update_turn()

# Função para enviar mensagens para todos os clientes
def broadcast(message):
    to_remove = []
    for client, _ in clients:
        try:
            client.sendall(message.encode())
        except:
            to_remove.append(client)

    # Remover clientes desconectados
    for client in to_remove:
        clients[:] = [(c, p) for c, p in clients if c != client]

# Configuração do socket do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Servidor rodando em {HOST}:{PORT}")

player_id = 0
while True:
    conn, addr = server.accept()
    with lock:
        clients.append((conn, player_id))
        turns_list.append(player_id)
    
    thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
    thread.start()
    player_id += 1
