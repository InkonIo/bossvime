from boss_template import create_boss_window

def test_window():
    return create_boss_window(
        boss_name="Тест",
        minutes=0.083,  # 5 секунд
        sound_file="sounds/rilo.mp3",
        image_file="images/test.png",
        color="#3498db"  # Синий цвет
    )