#sikirin yonatan 311292122 סיקירין יונתן
import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client():
    Num_of_wrong_b_time = 0
    Num_of_wrong_inputs = 1
    client_socket.connect((HOST, PORT))  # Connecting to server's socket
    while True:
        try:
            data = client_socket.recv(1024).decode()  # Receiving data from server
            if data == 're-enter number of wins':
                Num_of_wrong_inputs = Num_of_wrong_inputs + 1
                if Num_of_wrong_inputs >= 6:
                    print(f"blocked for {60 * pow(2,Num_of_wrong_b_time)} seconds")
                    time.sleep(5)
                    Num_of_wrong_b_time += 1
                    Num_of_wrong_inputs = 1
            if data == 'Goodbye client':
                client_socket.close()  # Closing client's connection with server (<=> closing socket)
                print("\n[CLOSING CONNECTION] client closed socket!")
                time.sleep(0.5)
                exit()
            print(f"{data}\n")
            time.sleep(0.05) # waits 0.05 seconds so that the server has enough time to send all data
            new_message = input("Please enter message for server: ")
            client_socket.send(new_message.encode())
            time.sleep(0.05)
        except:
            client_socket.send("test".encode())
            print("failed")
            client_socket.close()  # Closing client's connection with server (<=> closing socket)
            print("\n[CLOSING CONNECTION] client closed socket!")
            return




if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")
