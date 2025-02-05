import socket
import threading

# Armazena as salas e os clientes em cada sala
salas = {}
lock = threading.Lock()

def handle_client(conn, addr):
    conn.send("Bem-vindo ao servidor de chat!\nDigite /salas para listar salas, /criar <nome> para criar uma nova sala, /entrar <nome> para entrar em uma sala e /sair para desconectar.\n".encode())
    sala_atual = None
    
    while True:
        try:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break
            
            if msg.startswith("/salas"):
                with lock:
                    conn.send(f"Salas disponíveis: {', '.join(salas.keys()) if salas else 'Nenhuma sala disponível'}\n".encode())
            
            elif msg.startswith("/criar "):
                _, nome_sala = msg.split(" ", 1)
                with lock:
                    if nome_sala in salas:
                        conn.send("Essa sala já existe!\n".encode())
                    else:
                        salas[nome_sala] = []
                        conn.send(f"Sala '{nome_sala}' criada!\n".encode())
            
            elif msg.startswith("/entrar "):
                _, nome_sala = msg.split(" ", 1)
                with lock:
                    if nome_sala not in salas:
                        conn.send("Sala não encontrada!\n".encode())
                    else:
                        if sala_atual:
                            salas[sala_atual].remove(conn)
                        sala_atual = nome_sala
                        salas[nome_sala].append(conn)
                        conn.send(f"Entrou na sala '{nome_sala}'!\n".encode())
            
            elif msg.startswith("/sair"):
                with lock:
                    if sala_atual:
                        salas[sala_atual].remove(conn)
                        conn.send(f"Saiu da sala '{sala_atual}'.\n".encode())
                        sala_atual = None
                    else:
                        conn.send("Você não está em nenhuma sala.\n".encode())
            
            else:
                if sala_atual:
                    with lock:
                        for cliente in salas[sala_atual]:
                            if cliente != conn:
                                cliente.send(f"{addr}: {msg}\n".encode())
                else:
                    conn.send("Você precisa entrar em uma sala para enviar mensagens!\n".encode())
        except:
            break
    
    with lock:
        if sala_atual and conn in salas[sala_atual]:
            salas[sala_atual].remove(conn)
    conn.close()

def start_server(host='127.0.0.1', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor rodando em {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        print(f"Nova conexão de {addr}")
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
