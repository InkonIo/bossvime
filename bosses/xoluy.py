from boss_template import create_boss_window

def xoluy_window():
    return create_boss_window(
        boss_name="Холуй",
        minutes=60,
        sound_file="sounds/xoluy.mp3",
        image_file="images/villager.jpg", 
        color="#8e44ad"  # Фиолетовый цвет
    )