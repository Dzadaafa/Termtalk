import pyrebase
import os
import json

# import credential hehe
script_dir = os.path.dirname(os.path.abspath(__file__))
flag_file = os.path.join(script_dir, 'exit_flag')
config_file = os.path.join(script_dir, 'config.json')

with open(config_file, 'r') as f:
    config = json.load(f)

#colorama


firebase = pyrebase.initialize_app(config)
db = firebase.database()

latest_msg = ""
messages = []
online_user = 0

def status(login:bool=False, logout:bool=False) -> int:
    s = db.get().val()
    q = s["status"]

    if login:
            number = q + 1
            db.update({"status": number})
            return
    
    elif logout:
            number = q - 1
            db.update({"status": number})

    return q

    

def receive_message() -> list | None:
    messages_ref = db.child("message")
    
    def message_callback(message) -> list | None:
        global latest_msg, messages, online_user

        onlineUsr = status()
        
        result = message.val()
        if result:
            listed_result = list(result['messages'].items())
            last_key, main_val = listed_result[-1]
            
            # Determine db_color within the valid range
            db_color = main_val['color'] if main_val['color'] and 7 >= main_val['color'] >= 2 else 3
            
            if last_key != latest_msg:
                final_result = ((main_val['username'], main_val['message']), db_color)
                messages.append(final_result)
                latest_msg = last_key
                return final_result
            elif online_user != onlineUsr:
                online_user = onlineUsr
                return online_user
            else:
                return None
    
    while True:
        new_message = messages_ref.get()
        if new_message:
            message_callback(new_message)

def send_message(color:int, username:str, msg:str) -> bool:
    try:
        messages_ref = db.child("messages")

        messages_ref.push({
            "username": username,
            "message": msg,
            "color": color
        })

        return True
    except Exception as e:
        return False

# if __name__=="__main__":
#     a = receive_message()
    # status()
