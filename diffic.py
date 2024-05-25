DIFFICULTIES = {
    "standart": {"ball_speed": 2.3, "cpu_speed": 2, "pl_speed": 3},
}

def choose_difficulty(screen):
    """Функция выбора уровня сложности (просто возвращает параметры для уровня medium)"""
    return DIFFICULTIES["standart"]
