from boss_template import create_boss_window

def zombie_window():
    return create_boss_window(
        boss_name="Зомби",
        minutes=24,
        sound_file="sounds/zombie.mp3",
        image_file="images/zombie.jpg",
        color="#27ae60"  # Зеленый цвет
    )
