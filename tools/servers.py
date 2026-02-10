
import logging
import asyncio
from typing import Tuple
from config import PASSWORD

# Словник для зберігання доступних серверів
SERVERS = {
    'terraria': {
        'name': 'Terraria Server',
        'service_name': 'terraria'
    },
    'minecraft': {
        'name': 'Minecraft Server',
        'service_name': 'minecraft'
    },
    'factorio': {
        'name': 'Factorio Server',
        'service_name': 'factorio'
    },
    'valheim': {
        'name': 'Valheim Server',
        'service_name': 'valheim'
    }
}


async def execute_server_command(server_key: str, command: str, password: str = PASSWORD) -> Tuple[bool, str]:
    """
    Виконує команду керування сервером через sudo з паролем

    Args:
        server_key: Ключ сервера зі словника SERVERS
        command: Команда для виконання (start, stop, restart)
        password: Пароль для sudo (якщо потрібен)

    Returns:
        Tuple[bool, str]: (успішність, повідомлення)
    """
    try:
        if server_key not in SERVERS:
            return False, "❌ Сервер не знайдено!"

        service_name = SERVERS[server_key]['service_name']

        # Команда з sudo та опцією -S для читання пароля зі stdin
        cmd = f"sudo -S service {service_name} {command}"

        try:
            # Виконуємо команду асинхронно з timeout
            if password:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    # Передаємо пароль з новою лінією в stdin
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(input=f"{password}\n".encode()),
                        timeout=15
                    )
                    returncode = process.returncode
                    stdout_text = stdout.decode()
                    stderr_text = stderr.decode()
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    return False, "⏱️ Timeout: команда надто довго виконується"
            else:
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=15
                    )
                    returncode = process.returncode
                    stdout_text = stdout.decode()
                    stderr_text = stderr.decode()
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    return False, "⏱️ Timeout: команда надто довго виконується"

            if returncode == 0:
                logging.info(f"✅ Команда виконана: {cmd}")
                return True, get_success_message(command)
            else:
                error_msg = stderr_text if stderr_text else stdout_text
                logging.error(f"❌ Помилка при {command}: {error_msg}")

                # Перевіряємо, чи помилка пароля
                if "password is incorrect" in error_msg.lower() or "sudo:" in error_msg.lower():
                    return False, "❌ Помилка: невірний пароль або недостатня дозвіл"

                return False, f"❌ Помилка при виконанні команди"

        except Exception as e:
            logging.error(f"❌ Помилка при виконанні команди: {e}")
            return False, f"❌ Помилка: {str(e)}"

    except Exception as e:
        logging.error(f"❌ Критична помилка: {e}")
        return False, f"❌ Критична помилка: {str(e)}"


def get_success_message(command: str) -> str:
    """Повертає повідомлення про успішне виконання команди"""
    messages = {
        'start': '✅ Сервер успішно стартував',
        'stop': '✅ Сервер успішно зупинився',
        'restart': '✅ Сервер успішно перезавантажився',
        'reboot': '✅ Сервер успішно перезавантажився',
    }
    return messages.get(command, f'✅ Команда "{command}" успішно виконана')


def get_servers_list() -> dict:
    """Повертає словник доступних серверів"""
    return SERVERS


def server_exists(server_key: str) -> bool:
    """Перевіряє, чи існує сервер"""
    return server_key in SERVERS