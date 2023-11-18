import socket
from PIL import Image
from io import BytesIO
import cv2
import pandas as pd

# Server configuration
HOST = '127.0.0.1'
PORT = 9876

def getname(imgpath):
    global img_path
    img_path=imgpath

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Server listening on {HOST}:{PORT}...")

clicked = False
r = g = b = xpos = ypos = 0
index=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

while True:
    # Receive filename from client
    filename, client_address = server_socket.recvfrom(1024)
    filename = filename.decode('utf-8').strip()

    print(f"Received filename from client: {filename}")
    
    # Load and display the image
    try:
        with open(filename, 'rb') as file:
            image_data = file.read()
            image = Image.open(BytesIO(image_data))
            getname(filename)
            img = cv2.imread(img_path)
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', draw_function)
            while True:
                cv2.imshow("image", img)
                if clicked:
                    cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1) 
                    text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
                    if r + g + b >= 600:
                        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                    else:
                        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                    clicked = False
                if cv2.waitKey(20) & 0xFF == 27:
                    break

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
server_socket.close()

