# Класс узла для связанного списка, используемого в очереди
class QueueNode:
    def __init__(self, value):
        self.value = value  # Значение узла
        self.next = None    # Ссылка на следующий узел


# Определяем класс Queue (очередь) для хранения карт игроков
class Queue:
    # Инициализация пустой очереди
    def __init__(self):
        self.head = None  # Указатель на начало очереди 
        self.tail = None  # Указатель на конец очереди
       
    
    # Метод добавления элемента в конец очереди
    def enqueue(self, item):
        # Создаем новый узел с заданным значением
        new_node = QueueNode(item)
        # Если очередь пуста, новый узел становится и головой и хвостом
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            # Иначе добавляем новый узел после текущего хвоста
            self.tail.next = new_node
            self.tail = new_node
        
    
    # Метод извлечения элемента из начала очереди
    def dequeue(self):
        # Если очередь пуста, возвращаем None
        if self.head is None:
            return None
        
        # Сохраняем значение головного узла
        value = self.head.value
        # Перемещаем указатель головы на следующий узел
        self.head = self.head.next
        
        # Если голова стала None, значит очередь опустела - обнуляем хвост
        if self.head is None:
            self.tail = None
        
        # Возвращаем значение извлеченного элемента
        return value
    
    # Метод проверки очереди на пустоту
    def is_empty(self):
        # Очередь пуста, если голова None
        return self.head is None


# Определяем класс Player для представления игрока
class Player:
    # Инициализация игрока с именем
    def __init__(self, name):
        self.name = name  # Имя игрока (first или second)
        self.deck = Queue()  # Колода карт игрока (экземпляр Queue)
    
    # Метод добавления списка карт в колоду игрока
    def add_cards(self, cards):
        for card in cards:  # Добавляем каждую карту по очереди
            self.deck.enqueue(card)
    
    # Метод проверки, пуста ли колода игрока
    def is_empty(self):
        return self.deck.is_empty()  # Используем метод Queue
    
    # Метод розыгрыша верхней карты
    def play_card(self):
        return self.deck.dequeue()  # Извлекаем карту из колоды
    
    # Метод взятия карт после выигранного раунда
    def take_cards(self, card1, card2):
        self.deck.enqueue(card1)  # Сначала кладем карту первого игрока
        self.deck.enqueue(card2)  # Затем карту второго игрока


# Функция проверки корректности введенных данных
def validate_input(cards_str, player_name):
    try:
        # Пробуем преобразовать строку в список чисел
        cards = list(map(int, cards_str.split()))
    except ValueError:
        # Если преобразование не удалось - ошибка ввода
        raise ValueError(f"У игрока {player_name} введены нечисловые данные")
    
    # Проверяем, что карт ровно 5
    if len(cards) != 5:
        raise ValueError(f"У игрока {player_name} должно быть ровно 5 карт")
    
    # Проверяем, что все карты в диапазоне 0-9
    if any(card < 0 or card > 9 for card in cards):
        raise ValueError(f"У игрока {player_name} карты должны быть числами от 0 до 9")
    
    # Проверяем на уникальность карт
    if len(set(cards)) != len(cards):
        raise ValueError(f"У игрока {player_name} есть повторяющиеся карты")
    
    return cards  # Возвращаем валидный список карт


# Функция получения корректных карт от пользователя
def get_valid_cards(player_name, existing_cards=None):
    while True:  # Бесконечный цикл, пока не получим правильные данные
        try:
            # Запрашиваем ввод карт
            cards_str = input(f"Введите 5 уникальных карт (0-9) для игрока {player_name}: ")
            # Проверяем введенные данные
            cards = validate_input(cards_str, player_name)
            
            # Если переданы существующие карты, проверяем на пересечение
            if existing_cards:
                common = set(cards) & set(existing_cards)
                if common:
                    raise ValueError(f"Карты {common} уже есть у другого игрока")
            
            return cards  # Возвращаем корректные карты
        except ValueError as e:
            print(f"Ошибка: {e}")  # Выводим сообщение об ошибке


# Основная функция симуляции игры
def drunken_simulator():
    # Получаем карты первого игрока
    first_cards = get_valid_cards("first")
    
    # Получаем карты второго игрока с дополнительной проверкой
    while True:
        second_cards = get_valid_cards("second", first_cards)
        
        # Проверяем, что карты не пересекаются
        common = set(first_cards) & set(second_cards)
        if not common:
            break  # Выходим из цикла, если пересечений нет
        
        # Иначе сообщаем об ошибке
        print(f"Ошибка: карты {common} присутствуют у обоих игроков")
        print("Пожалуйста, измените карты для второго игрока")
    
    # Создаем игроков
    first_player = Player("first")
    second_player = Player("second")
    
    # Добавляем карты игрокам
    first_player.add_cards(first_cards)
    second_player.add_cards(second_cards)
    
    max_moves = 10**6  # Максимальное количество ходов
    moves = 0  # Счетчик ходов
    
    # Основной игровой цикл
    while moves <= max_moves:
        # Проверяем окончание игры
        if first_player.is_empty():
            print(f"second {moves}")
            return
        if second_player.is_empty():
            print(f"first {moves}")
            return
        
        # Игроки разыгрывают карты
        card1 = first_player.play_card()
        card2 = second_player.play_card()
        
        # Определяем победителя раунда
        if (card1 == 0 and card2 == 9):
            winner = first_player  # Особый случай: 0 бьет 9
        elif (card1 == 9 and card2 == 0):
            winner = second_player  # Особый случай: 0 бьет 9
        elif card1 > card2:
            winner = first_player  # Старшая карта побеждает
        else:
            winner = second_player  # Иначе побеждает второй игрок
        
        # Победитель забирает карты
        winner.take_cards(card1, card2)
        
        moves += 1  # Увеличиваем счетчик ходов
    
    # Если превышено максимальное число ходов
    print("botva")


drunken_simulator()
