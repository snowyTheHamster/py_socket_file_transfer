import socket
import tqdm
import os
import PySimpleGUI as sg


def sendit():
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step

    port = 5001
    filesize = os.path.getsize(filename) # get filesize

    # create the client socket
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())


    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()


layout = [
    [sg.Text('Receiver\'s hostname or ip address:')],
    [sg.InputText(key='_IPADDRESSORHOSTNAME_', size=(40,1))],
    [sg.Text('Select File to Transfer:')],
    [sg.Input(key='_THEPAYLOAD_'), sg.FileBrowse()],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(70, 10))],
]

window: object = sg.Window('Python Socket File Transfer', layout, element_justification='left')

while True:
    event, values = window.read()
    if event is None:
        break
    if event == '_PROCESS_':
        filename = values['_THEPAYLOAD_']
        host = values['_IPADDRESSORHOSTNAME_']

        if filename == '':
            print('You must add a file for transfer')
        else:
            sendit()