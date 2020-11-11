import tornado.ioloop
import tornado.websocket
import requests
import json
import sys
import tornado.gen
import pandas as pd
from tornado.escape import json_encode

class Client(object):
    def __init__(self, join_url, play_url):
        self.wsconn = None
        self.join_url = join_url
        self.play_url = play_url
        self.user_details = {}
        self.all_data_from_excel = {}
        self.json_data_list = []

    def interact(self):
        fn = input("Enter a filename(must be a .xlsx file): ")
        return fn

    def load_maze(self, filename):
        try:
            df = pd.read_excel(filename, na_values=None)
            data = df.iloc[:].values
            for entry in data:
                try:
                    self.all_data_from_excel['instituția sursă'] = entry[0]
                    self.all_data_from_excel['sex'] = entry[1]
                    self.all_data_from_excel['vârstă'] = entry[2]
                    self.all_data_from_excel['dată debut simptome declarate'] = entry[3]
                    self.all_data_from_excel['simptome declarate'] = entry[4]
                    self.all_data_from_excel['dată internare'] = entry[5]
                    self.all_data_from_excel['simptome raportate la internare'] = entry[6]
                    self.all_data_from_excel['diagnostic și semne de internare'] = entry[7]
                    self.all_data_from_excel['istoric de călătorie'] = entry[8]
                    self.all_data_from_excel['mijloace de transport folosite'] = entry[9]
                    self.all_data_from_excel['confirmare contact cu o persoană infectată'] = entry[10]
                    self.all_data_from_excel['data rezultat testare'] = entry[11]
                    self.all_data_from_excel['rezultat testare'] = entry[12]
                    self.json_data_list.append(self.all_data_from_excel)
                except AttributeError as e:
                    print(e)
            # file_to_write_JSON_ARRAY = open("JSON_ARRAY.txt", "w+")
            # file_to_write_JSON_ARRAY.write( json.dumps(self.json_data_list, indent=4, default=str, ensure_ascii=False))
            # file_to_write_JSON_ARRAY.close()
            print("YOUR JSON ARRAY date from excel you receive is in file JSON_ARRAY.txt and variable json_data_list")
        except FileNotFoundError as er:
            print(er)
            print(self.load_maze(self.interact()))

    def get_user_input(self, question=None):
        str_choice = input(question)
        while any((str_choice is None, not str_choice.strip())):
            print("You entered an empty answer")
            str_choice = input(question)
        return str_choice 

    def generate_wsmessage(self):
        while True:
            print("What you send to server?")
            msg_type = self.get_user_input("Type M for a simple message or type J to send json_array -> \n")
            if (msg_type == 'M'):
                msg_line = self.get_user_input("Enter message to send to server -> \n")
                msg = {}
                msg['type'] = 'M'
                msg['message'] = msg_line
                print("Message to send: ", msg)
                return msg
            elif (msg_type == 'J'):
                msg = {}
                msg['type'] = 'J'
                msg['message'] =  json.dumps(self.json_data_list, indent=4, default=str, ensure_ascii=False)
                msg1 = "Message to send: send JSON array to server"
                print(msg1)
                return msg
            

    def init(self):
        print("Getting initial user details")
        print(self.load_maze(self.interact()))

    @tornado.gen.coroutine
    def connect_on_websocket(self):
        try:
            self.wsconn = yield tornado.websocket.websocket_connect(self.play_url)
        except Exception as e:
            print("Connection error: {}".format(e))
            sys.exit()
        else:
            print("CLient has connected to Server")
            yield self.send_wsmessage()

    @tornado.gen.coroutine
    def send_wsmessage(self):
        msg = self.generate_wsmessage()
        if not self.wsconn:
            raise RuntimeError('Web socket connection is closed.')
        yield self.wsconn.write_message(message=json_encode(msg))
        yield self.communicate_with_websocket()

    @tornado.gen.coroutine
    def communicate_with_websocket(self):
        recv_msg = None
        while True:
            recv_msg = yield self.wsconn.read_message()
            if recv_msg is None: 
                self.wsconn.close()
                break
            print("Server has replied with message=", recv_msg)
            yield self.send_wsmessage()
        print("IoLoop terminate")
        sys.exit()

    @tornado.gen.coroutine
    def main(self):
        choice = input("Do you want to continue(y/n)? ")
        if choice == "y":
            self.init()
            yield self.connect_on_websocket()
        else:
            sys.exit()

if __name__ == "__main__":
    try:
        client = Client("http://localhost:8888/join", "ws://localhost:8888/game")
        tornado.ioloop.IOLoop.instance().add_callback(client.main)
        tornado.ioloop.IOLoop.instance().start()
    except (SystemExit, KeyboardInterrupt):
        print("Client closed")