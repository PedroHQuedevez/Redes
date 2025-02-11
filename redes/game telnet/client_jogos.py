import socket

# Configuração do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor (local)
PORT = 65432         # Porta onde o servidor está ouvindo

def start_client():
    # Cria o socket do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            # Recebe e exibe a mensagem inicial do servidor
            data = s.recv(1024).decode()
            print(data)

            # Solicita ao usuário uma tentativa de adivinhação
            guess = input("Tente adivinhar o número entre 1 e 100 (ou 'sair' para encerrar): ")
            
            # Envia a tentativa para o servidor
            s.sendall(guess.encode())

            # Recebe o feedback do servidor
            data = s.recv(1024).decode()
            print(data)

if __name__ == "__main__":
    start_client()
