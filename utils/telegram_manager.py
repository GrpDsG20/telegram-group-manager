from telethon import TelegramClient, errors
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import Channel, Chat
import asyncio

class TelegramManager:
    def __init__(self, api_id, api_hash, phone, session_name='tg_session'):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.phone = phone
        self._is_authenticated = False

    async def start(self):
        """Inicia sesión en Telegram"""
        try:
            await self.client.start(
                phone=self.phone,
                code_callback=lambda: input("Ingresa el código de verificación: ")
            )
            me = await self.client.get_me()
            print(f"✅ Sesión iniciada como: @{me.username} (ID: {me.id})")
            self._is_authenticated = True
            return True
        except Exception as e:
            print(f"❌ Error de autenticación: {type(e).__name__} - {e}")
            return False

    async def disconnect(self):
        """Cierra la conexión"""
        try:
            if self._is_authenticated:
                await self.client.disconnect()
                print("🔌 Sesión cerrada correctamente")
        except Exception as e:
            print(f"⚠️ Error al desconectar: {e}")

    async def get_entity(self, identifier):
        """Obtiene una entidad (grupo/usuario) por ID, @username o nombre"""
        try:
            if isinstance(identifier, (int, str)) and str(identifier).lstrip('-').isdigit():
                return await self.client.get_entity(int(identifier))
            return await self.client.get_entity(identifier)
        except Exception as e:
            print(f"❌ Error buscando '{identifier}': {e}")
            return None

    async def get_active_users(self, chat, limit=200):
        """Obtiene usuarios activos de los últimos mensajes"""
        users = []
        try:
            async for message in self.client.iter_messages(chat, limit=limit):
                if message and message.sender:
                    if not any(u.id == message.sender.id for u in users):
                        users.append(message.sender)
            return users
        except Exception as e:
            print(f"❌ Error obteniendo mensajes: {e}")
            return []

    async def check_group_type(self, group):
        """Determina si es grupo normal, supergrupo o canal"""
        try:
            full_info = await self.client(GetFullChannelRequest(group))
            if full_info.full_chat.megagroup:
                return "supergroup"
            return "channel" if full_info.full_chat.broadcast else "group"
        except:
            return "group"

    async def safe_add_user(self, target_group, user, delay=2):
        """Versión corregida que maneja ambos tipos de grupos"""
        try:
            # Determinar el tipo de grupo
            if isinstance(target_group, Channel):
                # Para supergrupos/canales
                await self.client(InviteToChannelRequest(
                    channel=target_group,
                    users=[user]
                ))
            else:
                # Para grupos normales
                await self.client(AddChatUserRequest(
                    chat_id=target_group.id,
                    user_id=user.id,
                    fwd_limit=0
                ))
            
            username = f"@{user.username}" if user.username else f"ID:{user.id}"
            print(f"✅ Añadido: {username}")
            await asyncio.sleep(delay)
            return True
            
        except errors.UserPrivacyRestrictedError:
            print(f"🔒 Privacidad restringida (ID:{user.id})")
        except errors.FloodWaitError as e:
            print(f"⏳ Espera {e.seconds} segundos...")
            await asyncio.sleep(e.seconds)
        except errors.UserAlreadyParticipantError:
            print(f"⚠️ Usuario ya está en el grupo")
        except Exception as e:
            print(f"❌ Error: {type(e).__name__} - {e}")
        return False