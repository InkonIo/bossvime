import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from playsound import playsound


class ModernBossWindow:
    def __init__(self, boss_name, minutes, sound_file, image_file, color="#3498db"):
        self.boss_name = boss_name
        self.total_seconds = int(minutes * 60)
        self.remaining_seconds = self.total_seconds
        self.sound_file = sound_file
        self.image_file = image_file
        self.color = color
        self.is_paused = False
        self.is_active = False
        
        self.create_window()
    
    def create_window(self):
        """Создание современного окна таймера"""
        self.window = tk.Toplevel()
        self.window.title(f"{self.boss_name} - Таймер")
        self.window.geometry("400x500")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Центрирование окна
        self.center_window()
        
        # Заголовок
        header_frame = tk.Frame(self.window, bg='#34495e', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text=self.boss_name,
                              font=('Arial', 20, 'bold'),
                              bg='#34495e',
                              fg='#ecf0f1')
        title_label.pack(expand=True)
        
        # Изображение босса
        self.load_boss_image()
        
        # Основная область таймера
        timer_frame = tk.Frame(self.window, bg='#2c3e50')
        timer_frame.pack(pady=20)
        
        # Круговой прогресс-бар (имитация)
        self.progress_frame = tk.Frame(timer_frame, bg='#34495e', width=200, height=200)
        self.progress_frame.pack()
        self.progress_frame.pack_propagate(False)
        
        # Время в центре
        self.time_label = tk.Label(self.progress_frame,
                                  text=self.format_time(self.total_seconds),
                                  font=('Arial', 24, 'bold'),
                                  bg='#34495e',
                                  fg=self.color)
        self.time_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Статус
        self.status_label = tk.Label(timer_frame,
                                   text="Нажмите СТАРТ для запуска",
                                   font=('Arial', 12),
                                   bg='#2c3e50',
                                   fg='#95a5a6')
        self.status_label.pack(pady=10)
        
        # Прогресс бар
        self.create_progress_bar()
        
        # Кнопки управления
        self.create_control_buttons()
        
        # Информация о боссе
        self.create_info_panel()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"400x500+{x}+{y}")
    
    def load_boss_image(self):
        """Загрузка и отображение изображения босса"""
        try:
            img = Image.open(self.image_file)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            
            # Создаем круглую маску
            mask = Image.new('L', (100, 100), 0)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 100, 100), fill=255)
            
            # Применяем маску
            img.putalpha(mask)
            
            self.boss_photo = ImageTk.PhotoImage(img)
            
            image_label = tk.Label(self.window,
                                 image=self.boss_photo,
                                 bg='#2c3e50')
            image_label.pack(pady=10)
            
        except Exception as e:
            print(f"Ошибка загрузки изображения {self.image_file}: {e}")
            # Показываем эмодзи вместо изображения
            emoji_label = tk.Label(self.window,
                                 text="👾",
                                 font=('Arial', 60),
                                 bg='#2c3e50',
                                 fg=self.color)
            emoji_label.pack(pady=10)
    
    def create_progress_bar(self):
        """Создание прогресс бара"""
        progress_frame = tk.Frame(self.window, bg='#2c3e50')
        progress_frame.pack(pady=10, padx=40, fill='x')
        
        # Стиль для прогресс бара
        style = ttk.Style()
        style.configure("Boss.Horizontal.TProgressbar",
                       background=self.color,
                       troughcolor='#34495e',
                       borderwidth=0,
                       lightcolor=self.color,
                       darkcolor=self.color)
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          style="Boss.Horizontal.TProgressbar",
                                          mode='determinate',
                                          length=320)
        self.progress_bar.pack()
        self.progress_bar['maximum'] = self.total_seconds
        self.progress_bar['value'] = self.total_seconds
    
    def create_control_buttons(self):
        """Создание кнопок управления"""
        controls_frame = tk.Frame(self.window, bg='#2c3e50')
        controls_frame.pack(pady=20)
        
        # Кнопка старт/пауза
        self.start_pause_btn = tk.Button(controls_frame,
                                        text="▶ СТАРТ",
                                        font=('Arial', 14, 'bold'),
                                        bg=self.color,
                                        fg='white',
                                        relief='flat',
                                        padx=20,
                                        pady=10,
                                        cursor='hand2',
                                        command=self.toggle_timer)
        self.start_pause_btn.pack(side='left', padx=10)
        
        # Кнопка остановки
        self.stop_btn = tk.Button(controls_frame,
                                 text="⏹ СТОП",
                                 font=('Arial', 14, 'bold'),
                                 bg='#e74c3c',
                                 fg='white',
                                 relief='flat',
                                 padx=20,
                                 pady=10,
                                 cursor='hand2',
                                 command=self.stop_timer)
        self.stop_btn.pack(side='left', padx=10)
        
        # Кнопка сброса
        self.reset_btn = tk.Button(controls_frame,
                                  text="🔄 СБРОС",
                                  font=('Arial', 14, 'bold'),
                                  bg='#f39c12',
                                  fg='white',
                                  relief='flat',
                                  padx=20,
                                  pady=10,
                                  cursor='hand2',
                                  command=self.reset_timer)
        self.reset_btn.pack(side='left', padx=10)
        
        # Эффекты hover для кнопок
        self.add_hover_effects()
    
    def add_hover_effects(self):
        """Добавление эффектов наведения для кнопок"""
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.configure(bg=hover_color)
            def on_leave(e):
                button.configure(bg=normal_color)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        create_hover_effect(self.start_pause_btn, self.color, self.lighten_color(self.color))
        create_hover_effect(self.stop_btn, '#e74c3c', '#c0392b')
        create_hover_effect(self.reset_btn, '#f39c12', '#e67e22')
    
    def create_info_panel(self):
        """Создание информационной панели"""
        info_frame = tk.Frame(self.window, bg='#34495e')
        info_frame.pack(fill='x', pady=(20, 0))
        
        # Время респауна
        total_time = self.format_time(self.total_seconds)
        info_text = f"Время респауна: {total_time}"
        
        info_label = tk.Label(info_frame,
                            text=info_text,
                            font=('Arial', 11),
                            bg='#34495e',
                            fg='#bdc3c7')
        info_label.pack(pady=10)
        
        # Дополнительная информация
        tip_label = tk.Label(info_frame,
                           text="Совет: окно можно свернуть, звук будет воспроизведен",
                           font=('Arial', 9),
                           bg='#34495e',
                           fg='#7f8c8d')
        tip_label.pack(pady=(0, 15))
    
    def toggle_timer(self):
        """Переключение старт/пауза"""
        if not self.is_active:
            self.start_timer()
        else:
            if self.is_paused:
                self.resume_timer()
            else:
                self.pause_timer()
    
    def start_timer(self):
        """Запуск таймера"""
        self.is_active = True
        self.is_paused = False
        self.start_pause_btn.configure(text="⏸ ПАУЗА")
        self.status_label.configure(text="Таймер запущен", fg=self.color)
        self.countdown()
    
    def pause_timer(self):
        """Пауза таймера"""
        self.is_paused = True
        self.start_pause_btn.configure(text="▶ ПРОДОЛЖИТЬ")
        self.status_label.configure(text="Таймер на паузе", fg='#f39c12')
    
    def resume_timer(self):
        """Возобновление таймера"""
        self.is_paused = False
        self.start_pause_btn.configure(text="⏸ ПАУЗА")
        self.status_label.configure(text="Таймер запущен", fg=self.color)
        self.countdown()
    
    def stop_timer(self):
        """Остановка таймера"""
        self.is_active = False
        self.is_paused = False
        self.start_pause_btn.configure(text="▶ СТАРТ")
        self.status_label.configure(text="Таймер остановлен", fg='#e74c3c')
        self.window.destroy()
    
    def reset_timer(self):
        """Сброс таймера"""
        self.is_active = False
        self.is_paused = False
        self.remaining_seconds = self.total_seconds
        self.start_pause_btn.configure(text="▶ СТАРТ")
        self.status_label.configure(text="Таймер сброшен", fg='#95a5a6')
        self.update_display()
    
    def countdown(self):
        """Обратный отсчет"""
        if self.is_active and not self.is_paused and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            self.window.after(1000, self.countdown)
        elif self.remaining_seconds <= 0 and self.is_active:
            self.timer_finished()
    
    def update_display(self):
        """Обновление отображения времени и прогресса"""
        # Обновляем время
        self.time_label.configure(text=self.format_time(self.remaining_seconds))
        
        # Обновляем прогресс бар
        progress_value = self.total_seconds - self.remaining_seconds
        self.progress_bar['value'] = progress_value
        
        # Изменяем цвет времени в зависимости от оставшегося времени
        if self.remaining_seconds <= 60:  # Последняя минута
            self.time_label.configure(fg='#e74c3c')
        elif self.remaining_seconds <= 300:  # Последние 5 минут
            self.time_label.configure(fg='#f39c12')
        else:
            self.time_label.configure(fg=self.color)
    
    def timer_finished(self):
        """Обработка завершения таймера"""
        self.is_active = False
        self.time_label.configure(text="00:00:00", fg='#27ae60')
        self.status_label.configure(text="🎉 БОСС ПОЯВИЛСЯ!", fg='#27ae60')
        self.progress_bar['value'] = self.total_seconds
        
        # Изменяем кнопки
        self.start_pause_btn.configure(text="✓ ГОТОВО", state='disabled')
        
        # Проигрываем звук
        self.play_notification_sound()
        
        # Показываем уведомление
        self.show_completion_notification()
        
        # Автоматически закрываем через 10 секунд
        self.window.after(10000, self.auto_close)
    
    def play_notification_sound(self):
        """Воспроизведение звука уведомления"""
        def play_sound():
            try:
                playsound(self.sound_file)
            except Exception as e:
                print(f"Ошибка воспроизведения звука: {e}")
        
        threading.Thread(target=play_sound, daemon=True).start()
    
    def show_completion_notification(self):
        """Показ уведомления о завершении"""
        # Мигание окна
        self.flash_window()
        
        # Системное уведомление (если возможно)
        self.window.bell()  # Системный звук
        
        # Поднимаем окно наверх
        self.window.lift()
        self.window.focus_force()
    
    def flash_window(self):
        """Мигание окна для привлечения внимания"""
        original_bg = self.window.cget('bg')
        flash_color = '#27ae60'
        
        def flash(count=0):
            if count < 6:  # Мигаем 3 раза (6 изменений цвета)
                current_bg = flash_color if count % 2 == 0 else original_bg
                self.window.configure(bg=current_bg)
                self.window.after(300, lambda: flash(count + 1))
            else:
                self.window.configure(bg=original_bg)
        
        flash()
    
    def auto_close(self):
        """Автоматическое закрытие окна"""
        if self.window.winfo_exists():
            self.window.destroy()
    
    def format_time(self, seconds):
        """Форматирование времени в ЧЧ:ММ:СС"""
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def lighten_color(self, color):
        """Осветление цвета для эффекта hover"""
        color_map = {
            '#3498db': '#5dade2',
            '#27ae60': '#2ecc71',
            '#f39c12': '#f1c40f',
            '#8e44ad': '#9b59b6',
            '#16a085': '#1abc9c',
            '#c0392b': '#e74c3c',
            '#e74c3c': '#ec7063'
        }
        return color_map.get(color, color)


def create_boss_window(boss_name, minutes, sound_file, image_file, color="#3498db"):
    """Создание современного окна таймера босса"""
    return ModernBossWindow(boss_name, minutes, sound_file, image_file, color)