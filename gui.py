import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from playsound import playsound


class ModernBossTimer:
    def __init__(self):
        self.active_timers = {}  # Словарь активных таймеров
        self.timer_windows = {}  # Окна таймеров
        
    def create_main_window(self):
        """Создание главного окна с современным дизайном"""
        self.root = tk.Tk()
        self.root.title("Boss Timers - Управление боссами")
        self.root.geometry("600x850")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Стиль для ttk элементов
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка стилей
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 20, 'bold'))
        
        style.configure('Boss.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=(10, 10))
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, 
                              text="🎮 BOSS TIMERS", 
                              font=('Arial', 24, 'bold'),
                              bg='#2c3e50', 
                              fg='#e74c3c')
        title_label.pack()
        
        subtitle = tk.Label(title_frame,
                           text="Выберите босса для отслеживания",
                           font=('Arial', 12),
                           bg='#2c3e50',
                           fg='#bdc3c7')
        subtitle.pack(pady=5)
        
        # Основной контейнер для боссов
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Список боссов с данными
        self.bosses_data = [
            ("Зомби", 24, "🧟", "#27ae60", "sounds/zombie.mp3", "images/zombie.jpg"),
            ("Рыло", 40, "🐷", "#f39c12", "sounds/rilo.mp3", "images/pig.jpg"),
            ("Холуй", 60, "👤", "#8e44ad", "sounds/xoluy.mp3", "images/villager.jpg"),
            ("Сточный слизень", 90, "🟢", "#16a085", "sounds/slizen.mp3", "images/slime.png"),
            ("Матка", 120, "🕷️", "#c0392b", "sounds/matka.mp3", "images/spider.jpg"),
            ("Тест", 0.083, "⚡", "#3498db", "sounds/rilo.mp3", "images/test.png"),
        ]
        
        # Создание карточек боссов
        for i, (name, minutes, emoji, color, sound, image) in enumerate(self.bosses_data):
            self.create_boss_card(main_container, name, minutes, emoji, color, sound, image, i)
        
        # Панель активных таймеров
        self.create_active_timers_panel()
        
        return self.root
    
    def create_boss_card(self, parent, name, minutes, emoji, color, sound_file, image_file, index):
        """Создание красивой карточки для каждого босса"""
        # Основная карточка
        card_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        card_frame.pack(fill='x', pady=8, padx=10)
        
        # Внутренний контейнер
        inner_frame = tk.Frame(card_frame, bg='#34495e')
        inner_frame.pack(fill='x', padx=15, pady=15)
        
        # Левая часть - иконка и информация
        left_frame = tk.Frame(inner_frame, bg='#34495e')
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Эмодзи и название
        header_frame = tk.Frame(left_frame, bg='#34495e')
        header_frame.pack(fill='x')
        
        emoji_label = tk.Label(header_frame, 
                              text=emoji, 
                              font=('Arial', 24),
                              bg='#34495e')
        emoji_label.pack(side='left', padx=(0, 10))
        
        name_label = tk.Label(header_frame,
                             text=name,
                             font=('Arial', 16, 'bold'),
                             bg='#34495e',
                             fg='#ecf0f1')
        name_label.pack(side='left')
        
        # Время респауна
        if minutes >= 60:
            time_text = f"{int(minutes//60)}ч {int(minutes%60)}м" if minutes % 60 != 0 else f"{int(minutes//60)}ч"
        elif minutes >= 1:
            time_text = f"{int(minutes)}м"
        else:
            time_text = f"{int(minutes*60)}с"
            
        time_label = tk.Label(left_frame,
                             text=f"Респаун: {time_text}",
                             font=('Arial', 11),
                             bg='#34495e',
                             fg='#95a5a6')
        time_label.pack(anchor='w', pady=(5, 0))
        
        # Лейбл для обратного отсчета (изначально скрыт)
        countdown_label = tk.Label(left_frame,
                                  text="",
                                  font=('Arial', 11, 'bold'),
                                  bg='#34495e',
                                  fg=color)
        countdown_label.pack(anchor='w')
        
        # Сохраняем ссылки для обновления
        setattr(self, f'{name.replace(" ", "_").lower()}_countdown_label', countdown_label)
        
        # Правая часть - кнопка запуска
        right_frame = tk.Frame(inner_frame, bg='#34495e')
        right_frame.pack(side='right')
        
        start_btn = tk.Button(right_frame,
                             text="▶ СТАРТ",
                             font=('Arial', 12, 'bold'),
                             bg=color,
                             fg='white',
                             relief='flat',
                             padx=20,
                             pady=10,
                             cursor='hand2',
                             command=lambda: self.start_boss_timer(name, minutes, sound_file, image_file, color))
        start_btn.pack()
        
        # Эффект hover
        def on_enter(e):
            start_btn.configure(bg=self.lighten_color(color))
        def on_leave(e):
            start_btn.configure(bg=color)
            
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)
    
    def create_active_timers_panel(self):
        """Панель активных таймеров"""
        # Разделитель
        separator = tk.Frame(self.root, height=2, bg='#7f8c8d')
        separator.pack(fill='x', pady=20)
        
        # Заголовок панели
        timers_frame = tk.Frame(self.root, bg='#2c3e50')
        timers_frame.pack(fill='both', expand=True, padx=40)
        
        timers_title = tk.Label(timers_frame,
                               text="🕐 Активные таймеры",
                               font=('Arial', 16, 'bold'),
                               bg='#2c3e50',
                               fg='#ecf0f1')
        timers_title.pack(pady=(0, 10))
        
        # Скроллируемая область для активных таймеров
        self.timers_container = tk.Frame(timers_frame, bg='#2c3e50')
        self.timers_container.pack(fill='both', expand=True)
        
        # Изначально показываем сообщение о том, что таймеров нет
        self.no_timers_label = tk.Label(self.timers_container,
                                       text="Нет активных таймеров",
                                       font=('Arial', 12),
                                       bg='#2c3e50',
                                       fg='#7f8c8d')
        self.no_timers_label.pack(pady=20)
    
    def start_boss_timer(self, boss_name, minutes, sound_file, image_file, color):
        """Запуск таймера для босса"""
        if boss_name in self.active_timers:
            # Если таймер уже запущен, показываем предупреждение
            self.show_warning(f"Таймер для {boss_name} уже активен!")
            return
        
        # Создаем данные таймера
        total_seconds = int(minutes * 60)
        timer_data = {
            'name': boss_name,
            'total_seconds': total_seconds,
            'remaining_seconds': total_seconds,
            'sound_file': sound_file,
            'image_file': image_file,
            'color': color,
            'active': True
        }
        
        self.active_timers[boss_name] = timer_data
        
        # Создаем визуальную карточку таймера
        self.create_timer_card(boss_name, timer_data)
        
        # Запускаем обратный отсчет
        self.start_countdown(boss_name)
        
        # Скрываем сообщение "нет таймеров"
        if hasattr(self, 'no_timers_label'):
            self.no_timers_label.pack_forget()
    
    def create_timer_card(self, boss_name, timer_data):
        """Создание карточки активного таймера"""
        card = tk.Frame(self.timers_container, bg='#34495e', relief='raised', bd=1)
        card.pack(fill='x', pady=5, padx=10)
        
        inner = tk.Frame(card, bg='#34495e')
        inner.pack(fill='x', padx=15, pady=10)
        
        # Левая часть - название и время
        left = tk.Frame(inner, bg='#34495e')
        left.pack(side='left', fill='both', expand=True)
        
        name_label = tk.Label(left,
                             text=boss_name,
                             font=('Arial', 14, 'bold'),
                             bg='#34495e',
                             fg='#ecf0f1')
        name_label.pack(anchor='w')
        
        time_label = tk.Label(left,
                             text="00:00:00",
                             font=('Arial', 12),
                             bg='#34495e',
                             fg=timer_data['color'])
        time_label.pack(anchor='w')
        
        # Правая часть - кнопки управления
        right = tk.Frame(inner, bg='#34495e')
        right.pack(side='right')
        
        stop_btn = tk.Button(right,
                            text="⏹ СТОП",
                            font=('Arial', 10, 'bold'),
                            bg='#e74c3c',
                            fg='white',
                            relief='flat',
                            padx=15,
                            pady=5,
                            cursor='hand2',
                            command=lambda: self.stop_timer(boss_name))
        stop_btn.pack(side='right', padx=(5, 0))
        
        pause_btn = tk.Button(right,
                             text="⏸ ПАУЗА",
                             font=('Arial', 10, 'bold'),
                             bg='#f39c12',
                             fg='white',
                             relief='flat',
                             padx=15,
                             pady=5,
                             cursor='hand2',
                             command=lambda: self.toggle_pause(boss_name))
        pause_btn.pack(side='right')
        
        # Сохраняем ссылки на элементы
        timer_data['card'] = card
        timer_data['time_label'] = time_label
        timer_data['pause_btn'] = pause_btn
        timer_data['paused'] = False
    
    def start_countdown(self, boss_name):
        """Запуск обратного отсчета"""
        def countdown():
            timer_data = self.active_timers.get(boss_name)
            if not timer_data or not timer_data['active']:
                return
            
            if not timer_data.get('paused', False) and timer_data['remaining_seconds'] > 0:
                timer_data['remaining_seconds'] -= 1
                
                # Обновляем отображение времени
                remaining = timer_data['remaining_seconds']
                hours, remainder = divmod(remaining, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                # Обновляем время в панели активных таймеров
                if 'time_label' in timer_data:
                    timer_data['time_label'].config(text=time_str)
                
                # Обновляем время в карточке босса на главном экране
                self.update_boss_card_countdown(boss_name, time_str, timer_data.get('paused', False))
                
                # Продолжаем отсчет
                self.root.after(1000, countdown)
                
            elif timer_data['remaining_seconds'] <= 0:
                # Таймер завершен
                self.timer_finished(boss_name)
        
        countdown()
    
    def update_boss_card_countdown(self, boss_name, time_str, is_paused):
        """Обновление обратного отсчета в карточке босса"""
        # Получаем лейбл для обратного отсчета
        countdown_label_name = f'{boss_name.replace(" ", "_").lower()}_countdown_label'
        countdown_label = getattr(self, countdown_label_name, None)
        
        if countdown_label:
            if is_paused:
                countdown_label.config(text=f"⏸ Отсчет: {time_str}", fg='#f39c12')
            else:
                countdown_label.config(text=f"⏰ Отсчет: {time_str}")
    
    def timer_finished(self, boss_name):
        """Обработка завершения таймера"""
        timer_data = self.active_timers.get(boss_name)
        if not timer_data:
            return
        
        # Обновляем текст в панели активных таймеров
        if 'time_label' in timer_data:
            timer_data['time_label'].config(text="ПОЯВИЛСЯ!", fg='#27ae60')
        
        # Обновляем текст в карточке босса
        countdown_label_name = f'{boss_name.replace(" ", "_").lower()}_countdown_label'
        countdown_label = getattr(self, countdown_label_name, None)
        if countdown_label:
            countdown_label.config(text="🎉 БОСС ПОЯВИЛСЯ!", fg='#27ae60')
        
        # Проигрываем звук в отдельном потоке
        def play_sound():
            try:
                playsound(timer_data['sound_file'])
            except Exception as e:
                print(f"Ошибка воспроизведения звука: {e}")
        
        threading.Thread(target=play_sound, daemon=True).start()
        
        # Показываем уведомление
        self.show_notification(boss_name)
        
        # Автоматически удаляем таймер через 10 секунд
        self.root.after(10000, lambda: self.stop_timer(boss_name))
    
    def stop_timer(self, boss_name):
        """Остановка и удаление таймера"""
        if boss_name in self.active_timers:
            timer_data = self.active_timers[boss_name]
            timer_data['active'] = False
            
            # Удаляем карточку из панели активных таймеров
            if 'card' in timer_data:
                timer_data['card'].destroy()
            
            # Очищаем обратный отсчет в карточке босса
            countdown_label_name = f'{boss_name.replace(" ", "_").lower()}_countdown_label'
            countdown_label = getattr(self, countdown_label_name, None)
            if countdown_label:
                countdown_label.config(text="")
            
            # Удаляем из словаря
            del self.active_timers[boss_name]
            
            # Если больше нет активных таймеров, показываем сообщение
            if not self.active_timers and hasattr(self, 'no_timers_label'):
                self.no_timers_label.pack(pady=20)
    
    def toggle_pause(self, boss_name):
        """Переключение паузы таймера"""
        timer_data = self.active_timers.get(boss_name)
        if not timer_data:
            return
        
        timer_data['paused'] = not timer_data.get('paused', False)
        
        if timer_data['paused']:
            timer_data['pause_btn'].config(text="▶ ПРОДОЛЖИТЬ", bg='#27ae60')
            # Обновляем статус в карточке босса
            countdown_label_name = f'{boss_name.replace(" ", "_").lower()}_countdown_label'
            countdown_label = getattr(self, countdown_label_name, None)
            if countdown_label:
                remaining = timer_data['remaining_seconds']
                hours, remainder = divmod(remaining, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                countdown_label.config(text=f"⏸ Отсчет: {time_str}", fg='#f39c12')
        else:
            timer_data['pause_btn'].config(text="⏸ ПАУЗА", bg='#f39c12')
            # Возобновляем отсчет
            self.start_countdown(boss_name)
    
    def show_notification(self, boss_name):
        """Показ уведомления о появлении босса"""
        notification = tk.Toplevel(self.root)
        notification.title("Босс появился!")
        notification.geometry("350x200")
        notification.configure(bg='#27ae60')
        notification.transient(self.root)
        notification.grab_set()
        
        # Центрирование окна
        notification.geometry("+{}+{}".format(
            int(notification.winfo_screenwidth()/2 - 175),
            int(notification.winfo_screenheight()/2 - 100)
        ))
        
        tk.Label(notification,
                text="🎉",
                font=('Arial', 40),
                bg='#27ae60',
                fg='white').pack(pady=20)
        
        tk.Label(notification,
                text=f"{boss_name} появился!",
                font=('Arial', 16, 'bold'),
                bg='#27ae60',
                fg='white').pack()
        
        tk.Button(notification,
                 text="OK",
                 font=('Arial', 12, 'bold'),
                 bg='white',
                 fg='#27ae60',
                 relief='flat',
                 padx=30,
                 pady=5,
                 command=notification.destroy).pack(pady=20)
        
        # Автоматическое закрытие через 5 секунд
        notification.after(5000, notification.destroy)
    
    def show_warning(self, message):
        """Показ предупреждения"""
        warning = tk.Toplevel(self.root)
        warning.title("Предупреждение")
        warning.geometry("300x150")
        warning.configure(bg='#e74c3c')
        warning.transient(self.root)
        warning.grab_set()
        
        # Центрирование
        warning.geometry("+{}+{}".format(
            int(warning.winfo_screenwidth()/2 - 150),
            int(warning.winfo_screenheight()/2 - 75)
        ))
        
        tk.Label(warning,
                text="⚠️",
                font=('Arial', 30),
                bg='#e74c3c',
                fg='white').pack(pady=10)
        
        tk.Label(warning,
                text=message,
                font=('Arial', 11),
                bg='#e74c3c',
                fg='white',
                wraplength=250).pack(pady=10)
        
        tk.Button(warning,
                 text="OK",
                 font=('Arial', 10, 'bold'),
                 bg='white',
                 fg='#e74c3c',
                 relief='flat',
                 padx=20,
                 command=warning.destroy).pack()
    
    def lighten_color(self, color):
        """Осветление цвета для эффекта hover"""
        color_map = {
            '#27ae60': '#2ecc71',
            '#f39c12': '#f1c40f',
            '#8e44ad': '#9b59b6',
            '#16a085': '#1abc9c',
            '#c0392b': '#e74c3c',
            '#3498db': '#5dade2'
        }
        return color_map.get(color, color)


def main_window():
    """Главная функция запуска приложения"""
    app = ModernBossTimer()
    root = app.create_main_window()
    root.mainloop()


if __name__ == "__main__":
    main_window()