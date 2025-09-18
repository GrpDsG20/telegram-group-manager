¿Dónde obtener el api_id y api_hash?
- Visita: https://my.telegram.org/apps
- Inicia sesión con tu número de Telegram.
- Crea una nueva aplicación y obtendrás el api_id y api_hash necesarios para el archivo config.yaml.

![Image](https://github.com/user-attachments/assets/8e0ae089-523d-4729-9abc-5bb14145f44d)

Es importante tener instalado y configurado Telegram Desktop.

1. Ejecuta el script con el siguiente comando:
   python main.py

2. Se solicitará el código de verificación Y MFA de Telegram si lo tiene.
   - Sigue las instrucciones de la consola.

3. El script comenzará a ejecutarse (INTERFAZ):
   - Extraerá los miembros del grupo origen.
   - Agregara el csv al grupo destino.

4. Requisitos importantes:
   - Debes ser administrador en el grupo destino y mienbro en el grupo origen.
   - puedes agregar mas de 1 numero, para no saturar las apis
   - Funcionara sin problema si minimo uno de los numeros es mienbro del grupo origen

5. Consideraciones:
   - Solo se pueden añadir usuarios que permitan ser agregados por otros.
   - Telegram impone límites diarios, por eso es recomendable usar varios numeros para ir intercalando.


