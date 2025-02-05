import socket

HOST = '127.0.0.1'  # Altere para o IP do servidor, se necessário
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    
    # Recebe a mensagem inicial do servidor
    print(client_socket.recv(1024).decode())

    while True:
        guess = input("Digite um número: ")
        client_socket.sendall(guess.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if "Parabéns" in response:
            break
