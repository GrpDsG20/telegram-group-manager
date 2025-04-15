import asyncio
from utils.config_loader import load_config
from utils.telegram_manager import TelegramManager

async def main():
    print("🔄 Iniciando proceso de transferencia de usuarios...")
    
    try:
        # Cargar configuración
        print("\n📁 Cargando configuración...")
        config = load_config()
        creds = config['credentials']['telegram']
        settings = config['settings']
        print("✅ Configuración cargada correctamente")

        # Validar credenciales
        required_creds = ['api_id', 'api_hash', 'phone_number']
        if missing := [k for k in required_creds if not creds.get(k)]:
            raise ValueError(f"Faltan credenciales: {', '.join(missing)}")

        # Inicializar manager
        print("\n🔑 Autenticando en Telegram...")
        manager = TelegramManager(
            api_id=creds['api_id'],
            api_hash=creds['api_hash'],
            phone=creds['phone_number']
        )

        if not await manager.start():
            raise ConnectionError("No se pudo autenticar")

        # Obtener grupos
        print("\n🔍 Localizando grupos...")
        source = await manager.get_entity(settings['group_source'])
        if not source:
            raise ValueError(f"Grupo origen no encontrado: {settings['group_source']}")
        print(f"✅ Grupo origen: {source.title}")

        target = await manager.get_entity(settings['group_target'])
        if not target:
            raise ValueError(f"Grupo destino no encontrado: {settings['group_target']}")
        
        target_type = await manager.check_group_type(target)
        print(f"✅ Grupo destino: {target.title} (Tipo: {target_type})")

        # Obtener usuarios activos
        print(f"\n🔎 Analizando últimos {settings['message_limit']} mensajes...")
        participants = await manager.get_active_users(source, settings['message_limit'])
        
        if not participants:
            print("⚠️ No se encontraron usuarios activos")
            print("ℹ️ Prueba aumentar 'message_limit' o verificar permisos")
            return

        # Filtrar usuarios
        print("\n🧹 Filtrando usuarios...")
        users_to_add = [
            p for p in participants
            if not p.bot and (p.username or str(p.id)) not in settings.get('excluded_users', [])
        ]
        print(f"👤 Usuarios válidos encontrados: {len(users_to_add)}")

        # Procesar añadidos
        print(f"\n🚀 Comenzando transferencia (delay: {settings.get('delay_seconds', 2)}s)...")
        added = 0
        for i, user in enumerate(users_to_add, 1):
            username = f"@{user.username}" if user.username else f"ID:{user.id}"
            print(f"\n[{i}/{len(users_to_add)}] Procesando: {username}")
            
            if await manager.safe_add_user(target, user, settings.get('delay_seconds', 2)):
                added += 1

        # Resultados
        print(f"\n🎉 Resultado final:")
        print(f"✅ Usuarios añadidos: {added}")
        print(f"❌ No añadidos: {len(users_to_add) - added}")

    except Exception as e:
        print(f"\n❌ Error crítico: {type(e).__name__}")
        print(f"📄 Detalles: {str(e)}")
        print("\n💡 Soluciones posibles:")
        print("- Verifica los IDs/nombres de los grupos")
        print("- Asegúrate de tener permisos de administrador")
        print("- Reduce 'message_limit' o aumenta 'delay_seconds'")
    finally:
        if 'manager' in locals():
            await manager.disconnect()
        print("\n🏁 Proceso completado")

if __name__ == "__main__":
    asyncio.run(main())