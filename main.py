class Queue: # создание класса очередь
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


# проверка входных данных на корректность
def validate_input(cards_str, player_name):
    try:
        cards = list(map(int, cards_str.split()))
    except ValueError:
        raise ValueError(f"У игрока {player_name} введены нечисловые данные")
    
    if len(cards) != 5:
        raise ValueError(f"У игрока {player_name} должно быть ровно 5 карт")
    
    if any(card < 0 or card > 9 for card in cards):
        raise ValueError(f"У игрока {player_name} карты должны быть числами от 0 до 9")
    
    if len(set(cards)) != len(cards):
        raise ValueError(f"У игрока {player_name} есть повторяющиеся карты")
    
    return cards

# получение списка карт игрока 
def get_valid_cards(player_name, existing_cards=None):
    while True:
        try:
            cards_str = input(f"Введите карты для игрока {player_name} (5 уникальных чисел 0-9 через пробел): ")
            cards = validate_input(cards_str, player_name)
            
            if existing_cards:
                common = set(cards) & set(existing_cards)
                if common:
                    raise ValueError(f"Карты {common} уже есть у другого игрока")
            
            return cards
        except ValueError as e:
            print(f"Ошибка: {e}")

# основная логика игры
def drunken_simulator():    
    # Получаем карты первого игрока
    first_cards = get_valid_cards("first")
    
    # Получаем карты второго игрока с проверкой на пересечение
    while True:
        second_cards = get_valid_cards("second", first_cards)
        
        # Дополнительная проверка, что первый игрок не имеет карт второго
        common = set(first_cards) & set(second_cards)
        if not common:
            break
            
        print(f"Ошибка: карты {common} присутствуют у обоих игроков")
        print("Пожалуйста, измените карты для второго игрока")
    
    # Инициализация колод
    first = Queue()
    second = Queue()
    
    for card in first_cards:
        first.enqueue(card)
    for card in second_cards:
        second.enqueue(card)
    
    max_moves = 10**6
    moves = 0
    
    while moves <= max_moves:
        if first.is_empty():
            print(f"second  {moves}")
            return
        if second.is_empty():
            print(f"first за {moves}")
            return
        
        card1 = first.dequeue()
        card2 = second.dequeue()
        
        # Определяем победителя раунда
        if (card1 == 0 and card2 == 9):
            winner = 1
        elif (card1 == 9 and card2 == 0):
            winner = 2
        elif card1 > card2:
            winner = 1
        else:
            winner = 2
        
        # Кладем карты в колоду победителя
        if winner == 1:
            first.enqueue(card1)
            first.enqueue(card2)
        else:
            second.enqueue(card1)
            second.enqueue(card2)
        
        moves += 1
    
    print("Botva")



drunken_simulator()
