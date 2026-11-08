import socket
import os
import re

def get_local_ip():
    """
    Определяет локальный IP-адрес компьютера в сети.
    Использует трюк с UDP-сокетом: мы не отправляем данные, 
    но ОС вынуждена выбрать правильный сетевой интерфейс для выхода в интернет.
    """
    try:
        # Создаем UDP сокет
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # "Подключаемся" к публичному IP (данные не отправляются!)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Если сеть не настроена, возвращаем localhost
        return "127.0.0.1"

def update_config(ip_address):
    """
    Находит файл frontend/config.py и заменяет в нем IP-адрес.
    """
    config_path = os.path.join("frontend", "config.py")
    
    if not os.path.exists(config_path):
        print(f"❌ Ошибка: Файл {config_path} не найден. Запустите скрипт из корневой папки проекта.")
        return

    # Читаем текущий конфиг
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Формируем новую строку
    new_url = f'API_BASE_URL = "http://{ip_address}:8000/api"'
    
    # Используем регулярное выражение, чтобы найти и заменить старую строку API_BASE_URL
    # Это сработает даже если там было написано localhost или старый IP
    updated_content = re.sub(
        r'API_BASE_URL\s*=\s*["\'].*?["\']', 
        new_url, 
        content
    )

    # Если ничего не изменилось, значит строки не было (добавим её)
    if updated_content == content:
        updated_content += f'\n{new_url}\n'

    # Записываем обновленный конфиг
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("="*50)
    print(f"✅ Сеть настроена успешно!")
    print(f"📡 Ваш локальный IP: {ip_address}")
    print(f"⚙️  Файл frontend/config.py обновлен.")
    print(f"🔗 Теперь фронтенд будет стучаться на: http://{ip_address}:8000/api")
    print("="*50)

if __name__ == "__main__":
    print("🔍 Определение локального IP-адреса...")
    local_ip = get_local_ip()
    update_config(local_ip)