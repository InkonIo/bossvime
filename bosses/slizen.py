from boss_template import create_boss_window

def slizen_window():
    return create_boss_window(
        boss_name="Сточный слизень",
        minutes=90,
        sound_file="sounds/slizen.mp3",
        image_file="images/slime.png",
        color="#16a085"  # Бирюзовый цвет
    )