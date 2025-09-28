from boss_template import create_boss_window

def matka_window():
    return create_boss_window(
        boss_name="Матка",
        minutes=120,
        sound_file="sounds/matka.mp3",
        image_file="images/spider.jpg",
        color="#c0392b"  # Красный цвет
    )