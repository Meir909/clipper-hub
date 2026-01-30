"""
Тестовые сценарии для Clipper HQ
Реалистичные сценарии использования платформы
"""

# Тестовые аккаунты
TEST_ACCOUNTS = {
    "clipper_accounts": [
        {
            "email": "anna.schmidt@gmail.com",
            "password": "test123",
            "role": "clipper",
            "name": "Anna Schmidt",
            "bio": "Lifestyle & Fashion Content Creator from Berlin 🇩🇪",
            "followers": {
                "instagram": 125000,
                "youtube": 45000,
                "tiktok": 89000
            },
            "scenarios": [
                "Fashion Campaign Creator",
                "Lifestyle Content Producer",
                "Brand Ambassador"
            ]
        },
        {
            "email": "maria.garcia@yahoo.com",
            "password": "test123",
            "role": "clipper",
            "name": "Maria Garcia",
            "bio": "Tech Reviewer & Unboxing Expert 📱💻",
            "followers": {
                "instagram": 67000,
                "youtube": 234000,
                "tiktok": 156000
            },
            "scenarios": [
                "Tech Product Reviewer",
                "Unboxing Specialist",
                "Gadget Tester"
            ]
        },
        {
            "email": "lucas.mueller@outlook.com",
            "password": "test123",
            "role": "clipper",
            "name": "Lucas Mueller",
            "bio": "Food & Travel Content Creator 🍕✈️",
            "followers": {
                "instagram": 89000,
                "youtube": 123000,
                "tiktok": 234000
            },
            "scenarios": [
                "Food Blogger",
                "Travel Vlogger",
                "Restaurant Reviewer"
            ]
        },
        {
            "email": "sophia.wagner@gmail.com",
            "password": "test123",
            "role": "clipper",
            "name": "Sophia Wagner",
            "bio": "Fitness & Wellness Coach 💪🧘‍♀️",
            "followers": {
                "instagram": 156000,
                "youtube": 78000,
                "tiktok": 345000
            },
            "scenarios": [
                "Fitness Instructor",
                "Wellness Coach",
                "Workout Creator"
            ]
        }
    ],
    "admin_accounts": [
        {
            "email": "admin@clipperhq.com",
            "password": "admin123",
            "role": "admin",
            "name": "Admin User",
            "scenarios": ["Platform Administration"]
        }
    ],
    "manager_accounts": [
        {
            "email": "manager@clipperhq.com",
            "password": "manager123",
            "role": "manager",
            "name": "Project Manager",
            "scenarios": ["Campaign Management", "Content Review"]
        }
    ]
}

# Тестовые сценарии
TEST_SCENARIOS = {
    "fashion_campaign_scenario": {
        "name": "Fashion Campaign Creator",
        "description": "Anna Schmidt работает с модными брендами",
        "steps": [
            "1. Вход как anna.schmidt@gmail.com",
            "2. Просмотр доступных проектов в категории Fashion",
            "3. Выбор проекта 'Summer Fashion Campaign 2024'",
            "4. Подача заявки на проект",
            "5. Создание контента (3 Instagram posts + 5 stories)",
            "6. Сабмишн контента на проверку",
            "7. Получение одобрения от менеджера",
            "8. Получение платежа €450"
        ],
        "expected_outcomes": [
            "Успешное участие в fashion кампании",
            "Получение платежа в течение 24 часов",
            "Увеличение рейтинга клиппера",
            "Доступ к премиум проектам"
        ]
    },
    
    "tech_review_scenario": {
        "name": "Tech Product Reviewer",
        "description": "Maria Garcia тестирует новые гаджеты",
        "steps": [
            "1. Вход как maria.garcia@yahoo.com",
            "2. Поиск проектов в категории Technology",
            "3. Выбор проекта 'Tech Product Launch Review'",
            "4. Создание детального обзора смартфона",
            "5. Запись 10+ минутного видео",
            "6. Добавление unboxing footage",
            "7. Сабмишн на YouTube",
            "8. Получение фидбэка от менеджера",
            "9. Получение платежа €320"
        ],
        "expected_outcomes": [
            "Качественный технический обзор",
            "Положительный фидбэк от бренда",
            "Повторные предложения от бренда",
            "Рост подписчиков на YouTube"
        ]
    },
    
    "food_travel_scenario": {
        "name": "Food & Travel Creator",
        "description": "Lucas Mueller создает контент о еде и путешествиях",
        "steps": [
            "1. Вход как lucas.mueller@outlook.com",
            "2. Просмотр проектов в категориях Food и Travel",
            "3. Выбор проекта 'Restaurant Chain Promotion'",
            "4. Посещение ресторана",
            "5. Профессиональная фотосъемка блюд",
            "6. Создание честного отзыва",
            "7. Публикация в Instagram с гео-тегом",
            "8. Создание Instagram Reels",
            "9. Получение платежа €280"
        ],
        "expected_outcomes": [
            "Качественный фуд-контент",
            "Сотрудничество с ресторанной сетью",
            "Увеличение вовлеченности аудитории",
            "Получение предложений от других ресторанов"
        ]
    },
    
    "fitness_challenge_scenario": {
        "name": "Fitness Challenge Creator",
        "description": "Sophia Wagner проводит фитнес-челленджи",
        "steps": [
            "1. Вход как sophia.wagner@gmail.com",
            "2. Поиск проектов в категории Fitness",
            "3. Выбор проекта 'Fitness App Challenge'",
            "4. Создание 30-дневного челленджа",
            "5. Запись тренировочных видео",
            "6. Отслеживание прогресса",
            "7. Создание before/after контента",
            "8. Публикация в TikTok и Instagram",
            "9. Получение платежа €380"
        ],
        "expected_outcomes": [
            "Вирусный фитнес-контент",
            "Привлечение новых клиентов",
            "Сотрудничество с фитнес-приложением",
            "Рост личного бренда"
        ]
    },
    
    "manager_review_scenario": {
        "name": "Content Review Manager",
        "description": "Менеджер проверяет сабмишены",
        "steps": [
            "1. Вход как manager@clipperhq.com",
            "2. Просмотр дашборда с новыми сабмишенами",
            "3. Проверка контента от Anna Schmidt",
            "4. Оценка качества соответствия требованиям",
            "5. Отправка фидбэка через Telegram",
            "6. Одобрение или отклонение сабмишена",
            "7. Обработка платежа",
            "8. Создание отчета для бренда"
        ],
        "expected_outcomes": [
            "Качественная проверка контента",
            "Своевременная обратная связь",
            "Удовлетворенность брендов",
            "Эффективная работа платформы"
        ]
    },
    
    "admin_monitoring_scenario": {
        "name": "Platform Administration",
        "description": "Администратор управляет платформой",
        "steps": [
            "1. Вход как admin@clipperhq.com",
            "2. Просмотр общей статистики платформы",
            "3. Мониторинг активных пользователей",
            "4. Проверка финансовых транзакций",
            "5. Управление проектами",
            "6. Решение спорных ситуаций",
            "7. Обновление настроек платформы",
            "8. Создание отчетов"
        ],
        "expected_outcomes": [
            "Стабильная работа платформы",
            "Безопасные финансовые операции",
            "Удовлетворенность пользователей",
            "Масштабирование бизнеса"
        ]
    }
}

# Инструкции для тестирования
TESTING_INSTRUCTIONS = """
🚀 ИНСТРУКЦИИ ПО ТЕСТИРОВАНИЮ CLIPPER HQ

1. СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ:
   python create_test_data.py

2. ЗАПУСК ПРИЛОЖЕНИЯ:
   python run.py

3. ДОСТУП К ПРИЛОЖЕНИЮ:
   http://localhost:5000

4. ТЕСТОВЫЕ АККАУНТЫ:

👩‍💼 CLIPPER ACCOUNTS:
   • Anna Schmidt: anna.schmidt@gmail.com / test123
   • Maria Garcia: maria.garcia@yahoo.com / test123  
   • Lucas Mueller: lucas.mueller@outlook.com / test123
   • Sophia Wagner: sophia.wagner@gmail.com / test123

👨‍💼 ADMIN ACCOUNTS:
   • Admin: admin@clipperhq.com / admin123
   • Manager: manager@clipperhq.com / manager123

5. РЕКОМЕНДУЕМЫЕ СЦЕНАРИИ ТЕСТИРОВАНИЯ:

📱 FASHION CAMPAIGN (Anna Schmidt):
   - Вход как Anna
   - Просмотр fashion проектов
   - Подача заявки на Summer Fashion Campaign
   - Создание и сабмишн контента

💻 TECH REVIEW (Maria Garcia):
   - Вход как Maria
   - Поиск tech проектов
   - Создание обзора гаджета
   - Загрузка видео на YouTube

🍕 FOOD & TRAVEL (Lucas Mueller):
   - Вход как Lucas
   - Работа с food проектами
   - Создание фуд-контента
   - Публикация в Instagram

💪 FITNESS CHALLENGE (Sophia Wagner):
   - Вход как Sophia
   - Фитнес-челлендж проекты
   - Создание тренировок
   - TikTok контент

👨‍💼 MANAGER WORKFLOW:
   - Вход как Manager
   - Проверка сабмишенов
   - Отправка фидбэка
   - Обработка платежей

🔧 ADMIN FUNCTIONS:
   - Вход как Admin
   - Просмотр статистики
   - Управление пользователями
   - Мониторинг платформы

6. КЛЮЧЕВЫЕ ФУНКЦИИ ДЛЯ ПРОВЕРКИ:
   ✅ Регистрация и вход
   ✅ Просмотр проектов
   ✅ Подача заявок
   ✅ Загрузка контента
   ✅ Проверка сабмишенов
   ✅ Получение платежей
   ✅ Уведомления
   ✅ Профиль пользователя
   ✅ Статистика и отчеты

7. ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ:
   - Плавная работа всех функций
   - Корректная обработка данных
   - Правильная работа уведомлений
   - Стабильная работа платежей
   - Удобный интерфейс

8. БРАУЗЕРЫ ДЛЯ ТЕСТИРОВАНИЯ:
   - Chrome (рекомендуется)
   - Firefox
   - Safari
   - Edge

9. МОБИЛЬНОЕ ТЕСТИРОВАНИЕ:
   - Chrome DevTools (Mobile View)
   - Реальные мобильные устройства
   - Проверка адаптивности

10. БЕЗОПАСНОСТЬ:
    - Проверка авторизации
    - Защита роутов
    - Валидация данных
    - CSRF защита

🎯 ЦЕЛЬ ТЕСТИРОВАНИЯ:
Убедиться, что все функции платформы работают корректно
и готовы для реального использования пользователями.
"""

if __name__ == '__main__':
    print(TESTING_INSTRUCTIONS)
