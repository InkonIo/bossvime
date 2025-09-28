from boss_template import create_boss_window

def rilo_window():
    return create_boss_window(
        boss_name="Рыло",
        minutes=40,
        sound_file="sounds/rilo.mp3", 
        image_file="images/pig.jpg",
        color="#f39c12"  # Оранжевый цвет
    )