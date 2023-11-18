import socket

# Client configuration
HOST = '127.0.0.1'
PORT = 9876

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get the name of the image file from the user
    filename = input("Enter the name of the image file (or 'exit' to quit): ")

    # Check if the user wants to exit
    if filename.lower() == 'exit':
        break

    # Send the filename to the server
    client_socket.sendto(filename.encode('utf-8'), (HOST, PORT))

# Close the socket
client_socket.close()
