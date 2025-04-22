import socket
from http import HTTPStatus

end_of_stream = '\r\n\r\n'


def handle_client(connection):
    client_data = ''
    with connection:
        while True:
            data = connection.recv(1024)
            print(data)
            if not data:
                break
            client_data += data.decode('utf-8')
            if end_of_stream in client_data:
                break

        first_line = client_data.split('\r\n')[0]
        method = first_line.split(' ')[0]
        host = client_data.split('\r\n')[1].replace(' ', '')
        host_parts = host.split(':')

        ip = host_parts[1]
        port = int(host_parts[2])
        source = (ip, port)

        headers = client_data.split('\r\n')[2:-1]
        result_headers = '\r\n'.join(headers)

        status = 200
        try:
            status_str = client_data.split(' ')[1]
            query = status_str.split('?')[-1]
            query_parts = query.split('&')
            for part in query_parts:
                if 'status' in part:
                    try:
                        status_str = part.split('=')[1]
                        status = int(status_str)
                    except (IndexError, ValueError) as e:
                        print(e)
        except (IndexError, ValueError) as e:
            print(e)

        status_phrase = HTTPStatus(status).phrase

        http_response = (
            f"HTTP/1.0 {status} {status_phrase}\r\n"
            f"Content-Type: text/plain\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"Request Method: {method}\r\n"
            f"Request Source: {source}\r\n"
            f"Response Status: {status} {status_phrase}\r\n"
            f"{result_headers}\r\n"
            )

        connection.send(http_response.encode()
                        + f"\r\n\r\n".encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("127.0.0.1", 40404))
    server_socket.listen(10)

    while True:
        client_connection, client_address = server_socket.accept()
        handle_client(client_connection)
        print(f"Sent data to {client_address}")
        client_connection.close()
