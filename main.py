import csv
import time
import random
import traceback
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerUser   # ✅ IMPORTANTE

from config import accounts, DELAY_BETWEEN_ADDS

# ============ LOGIN DE CUENTAS ===============
clients = []
for acc in accounts:
    client = TelegramClient(acc["phone"], acc["api_id"], acc["api_hash"])
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(acc["phone"])
            code = input(f"Ingrese el código de 5 dígitos enviado a {acc['phone']}: ")
            client.sign_in(acc["phone"], code)

            # Si la cuenta tiene 2FA
            if not client.is_user_authorized():
                try:
                    pwd = input(f"🔐 La cuenta {acc['phone']} tiene VERIFICACIÓN EN DOS PASOS.\nIngrese la contraseña 2FA: ")
                    client.sign_in(password=pwd)
                except Exception as e:
                    print(f"No se pudo iniciar sesión en {acc['phone']} con 2FA: {e}")
                    continue

        except SessionPasswordNeededError:
            pwd = input(f"🔐 La cuenta {acc['phone']} tiene VERIFICACIÓN EN DOS PASOS.\nIngrese la contraseña 2FA: ")
            client.sign_in(password=pwd)
        except Exception as e:
            print(f"No se pudo iniciar sesión en {acc['phone']}: {e}")
            continue

    clients.append(client)

if not clients:
    print("❌ Ninguna cuenta se pudo conectar.")
    exit()

# ============ FUNCIONES PRINCIPALES ============
def extraer_usuarios():
    grupos = simpledialog.askstring("Extraer usuarios", 
                                    "Ingrese los grupos separados por coma (@grupo o -ID):")
    if not grupos:
        return
    grupos = [g.strip() for g in grupos.split(",")]

    all_users = []
    for grupo in grupos:
        try:
            target_group = clients[0].get_entity(grupo)
            participants = clients[0].get_participants(target_group, aggressive=True)
            for user in participants:
                all_users.append([
                    user.id,
                    user.username or "",
                    user.access_hash,
                    (user.first_name or "") + " " + (user.last_name or "")
                ])
            print(f"✔ Extraídos {len(participants)} usuarios de {grupo}")
        except Exception as e:
            print(f"Error al extraer de {grupo}: {e}")
            traceback.print_exc()

    if all_users:
        with open("members.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "username", "access_hash", "name"])
            writer.writerows(all_users)
        messagebox.showinfo("Éxito", f"Usuarios guardados en members.csv ({len(all_users)} usuarios).")

def importar_usuarios():
    grupo_destino = simpledialog.askstring("Importar usuarios", 
                                           "Ingrese el @usuario o -ID del grupo destino:")
    if not grupo_destino:
        return

    csv_file = filedialog.askopenfilename(title="Seleccionar CSV", filetypes=[("CSV files", "*.csv")])
    if not csv_file:
        return

    try:
        target_group = clients[0].get_entity(grupo_destino)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo acceder al grupo destino: {e}")
        return

    with open(csv_file, "r", encoding="utf-8") as f:
        users = list(csv.reader(f))[1:]  # saltar header

    added = 0
    client_index = 0  # empieza en la primera cuenta

    for user in users:
        try:
            user_id = int(user[0])
            access_hash = int(user[2])
            entity = InputPeerUser(user_id=user_id, access_hash=access_hash)

            # usar la cuenta actual
            clients[client_index](InviteToChannelRequest(target_group, [entity]))
            print(f"✔ Usuario {user[3]} ({user[1]}) agregado con cuenta {accounts[client_index]['phone']}")
            added += 1

 

        except PeerFloodError:
            print(f"⚠ Flood detectado en {accounts[client_index]['phone']}, cambiando de cuenta...")
            client_index = (client_index + 1) % len(clients)  # rota a la siguiente cuenta
            if client_index == 0:
                print("⚠ Todas las cuentas alcanzaron el límite de invitaciones.")
                break
        except UserPrivacyRestrictedError:
            print(f"⚠ Usuario {user[3]} ({user[1]}) con privacidad, omitido.")
        except Exception as e:
            print(f"Error con {user[3]} ({user[1]}): {e}")

    messagebox.showinfo("Importación finalizada", f"Se intentó agregar {added} usuarios.")

# ============ INTERFAZ GRAFICA ============
root = tk.Tk()
root.title("Telegram Scraper & Adder")
root.geometry("400x200")

btn1 = tk.Button(root, text="📥 Extraer usuarios", command=extraer_usuarios, width=30, height=2)
btn1.pack(pady=20)

btn2 = tk.Button(root, text="📤 Importar usuarios", command=importar_usuarios, width=30, height=2)
btn2.pack(pady=20)

root.mainloop()
