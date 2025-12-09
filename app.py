from flask import Flask
import threading
import os
import time

# Hum main.py se FF_CLIENT class ko import kar rahe hain
# Dhyan rahe ki main.py aur app.py ek hi folder mein hon
try:
    from main import FF_CLIENT
except ImportError:
    print("Error: 'main.py' nahi mila ya usme FF_CLIENT class nahi hai.")

app = Flask(__name__)

# =========================================================
# 👇 YAHAN APNI IDS AUR PASSWORDS DALEIN (Jaisa main.py mein tha) 👇
# =========================================================

ACCOUNTS = [
    # Account 1
    {
        "id": "4330909008", 
        "password": "5BAE6FA6CBF4AF36BEBE2786502FE101BC061819DA888F78EAB418FBA3E7B65F"
    },
    
    # Account 2
    {
        "id": "4303131007", 
        "password": "E9ADF3DD3230DDB603F54B7FEB89E0512CB89175A67D040C6ECB3D68BFA34725"
    },

    # Account 3
    {
        "id": "46156555118", 
        "password": "YOUR_PASSWORD_HERE"
    },
     # Account 4
    {
        "id": "46156555118", 
        "password": "YOUR_PASSWORD_HERE"
    }, 
      
    # Aur accounts add karne ke liye upar wala block copy-paste karein
    # Bas last wale bracket '}' ke baad comma ',' lagana mat bhulna
]

# =========================================================
# 👆 UPAR APNI DETAILS BHARNE KE BAAD CODE KO CHHEDEIN MAT 👆
# =========================================================


def run_bots():
    """
    Yeh function background mein saare bots ko start karega
    """
    print(f"--- Total {len(ACCOUNTS)} Accounts Detect Hue ---")
    
    for index, acc in enumerate(ACCOUNTS):
        user_id = acc.get("id")
        user_pass = acc.get("password")

        # Check agar user ne password change nahi kiya
        if user_pass == "YOUR_PASSWORD_HERE":
            print(f"[Skip] Account {user_id} skip kiya kyunki password set nahi hai.")
            continue

        try:
            print(f"[Starting] Bot {index + 1} start ho raha hai: ID {user_id}...")
            
            # FF_CLIENT ko call kar rahe hain (main.py se)
            client_thread = FF_CLIENT(id=user_id, password=user_pass)
            client_thread.start()
            
            # Thoda wait karte hain taaki server par load na pade
            time.sleep(2) 
            
        except Exception as e:
            print(f"[Error] Bot {user_id} start nahi hua: {e}")

# --- WEB SERVER ROUTES (Render ko khush rakhne ke liye) ---

@app.route('/')
def home():
    return f"Glory Bot is Running on {len(ACCOUNTS)} Accounts! 🚀"

@app.route('/health')
def health():
    return "OK", 200

def start_server():
    # Bots ko alag thread mein chalayenge
    bot_thread = threading.Thread(target=run_bots)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask Web Server start karte hain
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_server()  