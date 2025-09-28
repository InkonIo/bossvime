#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boss Timers - Приложение для отслеживания времени респауна боссов
Версия: 2.0
Автор: Boss Timer Team
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime


class BossTimerApp:
    def __init__(self):
        self.config_file = "boss_timer_config.json"
        self.config = self.load_config()
        
    def load_config(self):
        """Загрузка конфигурации приложения"""
        default_config = {
            "theme": "dark",
            "sound_enabled": True,
            "auto_minimize": False,
            "show_notifications": True,
            "last_used": datetime.now().isoformat()
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Обновляем конфиг новыми ключами, если их нет
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                return default_config
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            return default_config
    
    def save_config(self):
        """Сохранение конфигурации"""
        try:
            self.config["last_used"] = datetime.now().isoformat()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
    
    def check_dependencies(self):
        """Проверка наличия необходимых зависимостей"""
        missing_deps = []
        
        try:
            import tkinter
        except ImportError:
            missing_deps.append("tkinter")
        
        try:
            from PIL import Image, ImageTk
        except ImportError:
            missing_deps.append("Pillow")
        
        try:
            from playsound import playsound
        except ImportError:
            missing_deps.append("playsound")
        
        if missing_deps:
            error_msg = f"""
Отсутствуют необходимые зависимости:
{chr(10).join('• ' + dep for dep in missing_deps)}

Установите их командой:
pip install {' '.join(missing_deps)}
"""
            messagebox.showerror("Ошибка зависимостей", error_msg)
            return False
        
        return True
    
    def check_resources(self):
        """Проверка наличия ресурсов (звуки, изображения)"""
        required_dirs = ["sounds", "images"]
        missing_dirs = []
        
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            warning_msg = f"""
Не найдены папки с ресурсами:
{chr(10).join('• ' + d for d in missing_dirs)}

Приложение может работать некорректно.
Создать недостающие папки?
"""
            if messagebox.askyesno("Предупреждение", warning_msg):
                for dir_name in missing_dirs:
                    try:
                        os.makedirs(dir_name, exist_ok=True)
                        print(f"Создана папка: {dir_name}")
                    except Exception as e:
                        print(f"Ошибка создания папки {dir_name}: {e}")
    
    def create_splash_screen(self):
        """Создание экрана загрузки"""
        splash = tk.Tk()
        splash.title("Boss Timers")
        splash.geometry("400x300")
        splash.configure(bg='#2c3e50')
        splash.overrideredirect(True)  # Убираем рамку окна
        
        # Центрирование
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (400 // 2)
        y = (splash.winfo_screenheight() // 2) - (300 // 2)
        splash.geometry(f"400x300+{x}+{y}")
        
        # Логотип и текст
        tk.Label(splash, 
                text="🎮", 
                font=('Arial', 48), 
                bg='#2c3e50', 
                fg='#e74c3c').pack(pady=50)
        
        tk.Label(splash, 
                text="BOSS TIMERS", 
                font=('Arial', 20, 'bold'), 
                bg='#2c3e50', 
                fg='#ecf0f1').pack()
        
        tk.Label(splash, 
                text="Загрузка приложения...", 
                font=('Arial', 12), 
                bg='#2c3e50', 
                fg='#95a5a6').pack(pady=20)
        
        # Прогресс бар (имитация)
        progress_frame = tk.Frame(splash, bg='#2c3e50')
        progress_frame.pack(pady=20)
        
        progress_bg = tk.Frame(progress_frame, bg='#34495e', height=10, width=300)
        progress_bg.pack()
        
        progress_fg = tk.Frame(progress_bg, bg='#e74c3c', height=10, width=0)
        progress_fg.place(x=0, y=0)
        
        # Анимация загрузки
        def animate_progress(width=0):
            if width <= 300:
                progress_fg.configure(width=width)
                splash.after(10, lambda: animate_progress(width + 5))
            else:
                splash.after(500, splash.destroy)
        
        animate_progress()
        
        # Информация о версии
        tk.Label(splash, 
                text="Версия 2.0 | Boss Timer Team", 
                font=('Arial', 8), 
                bg='#2c3e50', 
                fg='#7f8c8d').pack(side='bottom', pady=10)
        
        return splash
    
    def setup_exception_handler(self):
        """Настройка обработчика исключений"""
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            error_msg = f"""
Произошла непредвиденная ошибка:

Тип: {exc_type.__name__}
Сообщение: {str(exc_value)}

Приложение будет закрыто.
"""
            messagebox.showerror("Критическая ошибка", error_msg)
            sys.exit(1)
        
        sys.excepthook = handle_exception
    
    def run(self):
        """Главная функция запуска приложения"""
        print("🎮 Запуск Boss Timers v2.0")
        print("=" * 40)
        
        # Настройка обработчика исключений
        self.setup_exception_handler()
        
        # Показываем splash screen
        splash = self.create_splash_screen()
        splash.mainloop()
        
        # Проверка зависимостей
        print("📦 Проверка зависимостей...")
        if not self.check_dependencies():
            return
        
        # Проверка ресурсов
        print("🔍 Проверка ресурсов...")
        self.check_resources()
        
        # Импортируем главное окно только после проверок
        try:
            print("🚀 Загрузка главного окна...")
            from gui import main_window
            
            # Запускаем главное окно
            print("✅ Приложение готово к работе!")
            main_window()
            
        except ImportError as e:
            error_msg = f"Ошибка импорта модуля gui: {e}"
            messagebox.showerror("Ошибка импорта", error_msg)
            print(f"❌ {error_msg}")
        except Exception as e:
            error_msg = f"Ошибка запуска приложения: {e}"
            messagebox.showerror("Ошибка", error_msg)
            print(f"❌ {error_msg}")
        finally:
            # Сохраняем конфигурацию при выходе
            self.save_config()
            print("💾 Конфигурация сохранена")
            print("👋 Приложение завершено")


def main():
    """Точка входа в приложение"""
    app = BossTimerApp()
    app.run()


if __name__ == "__main__":
    main()