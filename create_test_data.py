"""
Тестовые сценарии и аккаунты для Clipper HQ
Создание реалистичных данных для демонстрации платформы
"""

from app import create_app, db
from app.models import User, Project, Submission, PayoutRequest, BalanceTransaction, Role, PaymentType, ProjectAccess, SubmissionStatus, PlatformType, PayoutStatus, BalanceType
from datetime import datetime, timedelta
import random

def create_test_data():
    """Создание тестовых данных"""
    app = create_app()
    
    with app.app_context():
        # Очистка существующих данных
        db.drop_all()
        db.create_all()
        
        # Создание тестовых пользователей
        users = create_test_users()
        
        # Создание проектов
        projects = create_test_projects()
        
        # Создание сабмишенов
        create_test_submissions(users, projects)
        
        # Создание выплат
        create_test_payouts(users)
        
        # Создание транзакций баланса
        create_test_balance_transactions(users)
        
        db.session.commit()
        
        print("✅ Тестовые данные успешно созданы!")
        print("📊 Статистика:")
        print(f"   Пользователей: {len(users)}")
        print(f"   Проектов: {len(projects)}")
        print(f"   Сабмишенов: {Submission.query.count()}")
        print(f"   Выплат: {PayoutRequest.query.count()}")
        print(f"   Транзакций: {BalanceTransaction.query.count()}")
        
        print("\n👤 Тестовые аккаунты:")
        print("   Anna Schmidt: anna.schmidt@gmail.com / test123")
        print("   Maria Garcia: maria.garcia@yahoo.com / test123")
        print("   Lucas Mueller: lucas.mueller@outlook.com / test123")
        print("   Sophia Wagner: sophia.wagner@gmail.com / test123")
        print("   Admin: admin@clipperhq.com / admin123")
        print("   Manager: manager@clipperhq.com / manager123")

def create_test_users():
    """Создание тестовых пользователей"""
    users_data = [
        {
            'email': 'anna.schmidt@gmail.com',
            'display_name': 'Anna Schmidt',
            'password': 'test123',
            'role': Role.CLIPPER,
            'balance_cents': 124000,  # €1,240
            'total_earned_cents': 2847000  # €28,470
        },
        {
            'email': 'maria.garcia@yahoo.com',
            'display_name': 'Maria Garcia',
            'password': 'test123',
            'role': Role.CLIPPER,
            'balance_cents': 89000,  # €890
            'total_earned_cents': 1560000  # €15,600
        },
        {
            'email': 'lucas.mueller@outlook.com',
            'display_name': 'Lucas Mueller',
            'password': 'test123',
            'role': Role.CLIPPER,
            'balance_cents': 45000,  # €450
            'total_earned_cents': 980000  # €9,800
        },
        {
            'email': 'sophia.wagner@gmail.com',
            'display_name': 'Sophia Wagner',
            'password': 'test123',
            'role': Role.CLIPPER,
            'balance_cents': 156000,  # €1,560
            'total_earned_cents': 3450000  # €34,500
        },
        {
            'email': 'admin@clipperhq.com',
            'display_name': 'Admin',
            'password': 'admin123',
            'role': Role.ADMIN,
            'balance_cents': 0,
            'total_earned_cents': 0
        },
        {
            'email': 'manager@clipperhq.com',
            'display_name': 'Project Manager',
            'password': 'manager123',
            'role': Role.MANAGER,
            'balance_cents': 0,
            'total_earned_cents': 0
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            email=user_data['email'],
            display_name=user_data['display_name'],
            role=user_data['role'],
            balance_cents=user_data['balance_cents'],
            total_earned_cents=user_data['total_earned_cents'],
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=random.randint(30, 90))
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    return users

def create_test_projects():
    """Создание тестовых проектов"""
    projects_data = [
        {
            'title': 'Summer Fashion Campaign 2024',
            'description': 'Looking for lifestyle influencers to showcase our new summer collection. High-quality photos and engaging stories required.',
            'earning_conditions': '3 Instagram posts + 5 stories, high-quality photos, brand tags',
            'payment_type': PaymentType.FIX_PER_VIDEO,
            'fixed_reward_cents': 45000,  # €450
            'access_mode': ProjectAccess.OPEN,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=7)
        },
        {
            'title': 'Tech Product Launch Review',
            'description': 'Seeking tech reviewers for our new smartphone launch. Honest reviews preferred, detailed unboxing experience required.',
            'earning_conditions': '10+ minute review video, unboxing footage, honest opinion',
            'payment_type': PaymentType.FIX_PER_VIDEO,
            'fixed_reward_cents': 32000,  # €320
            'access_mode': ProjectAccess.APPROVAL,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=5)
        },
        {
            'title': 'Restaurant Chain Promotion',
            'description': 'Food photographers and reviewers needed for our new menu campaign. Professional food styling experience required.',
            'earning_conditions': 'Professional food photography, honest review, location tags',
            'payment_type': PaymentType.FIX_PER_VIDEO,
            'fixed_reward_cents': 28000,  # €280
            'access_mode': ProjectAccess.OPEN,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=10)
        },
        {
            'title': 'Fitness App Challenge',
            'description': 'Fitness creators needed for 30-day challenge promotion. Workout demonstrations, progress tracking required.',
            'earning_conditions': 'Workout videos, progress updates, challenge participation',
            'payment_type': PaymentType.FIX_PER_VIDEO,
            'fixed_reward_cents': 38000,  # €380
            'access_mode': ProjectAccess.OPEN,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=14)
        },
        {
            'title': 'Travel Destination Campaign',
            'description': 'Travel influencers needed for tourism campaign. Beautiful destination photography, travel vlogs required.',
            'earning_conditions': 'Travel vlog, destination highlights, cultural content',
            'payment_type': PaymentType.FIX_PER_VIDEO,
            'fixed_reward_cents': 52000,  # €520
            'access_mode': ProjectAccess.APPROVAL,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=21)
        },
        {
            'title': 'Beauty Product Tutorial',
            'description': 'Beauty creators needed for makeup tutorial series. Product demonstration, before/after comparisons required.',
            'earning_conditions': 'Makeup tutorials, product reviews, before/after photos',
            'payment_type': PaymentType.FIX_PER_VIDEO,
            'fixed_reward_cents': 29000,  # €290
            'access_mode': ProjectAccess.OPEN,
            'start_date': datetime.utcnow(),
            'end_date': datetime.utcnow() + timedelta(days=8)
        }
    ]
    
    projects = []
    for project_data in projects_data:
        project = Project(
            title=project_data['title'],
            description=project_data['description'],
            earning_conditions=project_data['earning_conditions'],
            payment_type=project_data['payment_type'],
            fixed_reward_cents=project_data['fixed_reward_cents'],
            access_mode=project_data['access_mode'],
            start_date=project_data['start_date'],
            end_date=project_data['end_date'],
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
        )
        db.session.add(project)
        projects.append(project)
    
    db.session.commit()
    return projects

def create_test_submissions(users, projects):
    """Создание тестовых сабмишенов"""
    clipper_users = [u for u in users if u.role == Role.CLIPPER]
    statuses = [SubmissionStatus.PENDING, SubmissionStatus.APPROVED, SubmissionStatus.REJECTED]
    platforms = [PlatformType.INSTAGRAM, PlatformType.TIKTOK]
    
    for i, user in enumerate(clipper_users[:4]):  # Только для 4 клипперов
        for j, project in enumerate(projects[:3]):  # 3 проекта на пользователя
            status = random.choice(statuses)
            platform = random.choice(platforms)
            
            submission = Submission(
                project_id=project.id,
                clipper_id=user.id,
                video_url=f'https://instagram.com/p/test_{user.id}_{project.id}',
                platform=platform,
                views=random.randint(1000, 50000) if status == SubmissionStatus.APPROVED else None,
                status=status,
                reward_cents=project.fixed_reward_cents if status == SubmissionStatus.APPROVED else None,
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
                updated_at=datetime.utcnow() - timedelta(hours=random.randint(0, 24))
            )
            db.session.add(submission)

def create_test_payouts(users):
    """Создание тестовых выплат"""
    clipper_users = [u for u in users if u.role == Role.CLIPPER]
    
    for user in clipper_users:
        for month in range(3):  # 3 месяца выплат
            amount_cents = random.randint(20000, 80000)  # €200-€800
            
            payout = PayoutRequest(
                user_id=user.id,
                amount_cents=amount_cents,
                method='paypal',
                details=f'paypal@{user.email}',
                status=random.choice([PayoutStatus.PAID, PayoutStatus.PENDING]),
                created_at=datetime.utcnow() - timedelta(days=30*month + random.randint(1, 28))
            )
            db.session.add(payout)

def create_test_balance_transactions(users):
    """Создание тестовых транзакций баланса"""
    clipper_users = [u for u in users if u.role == Role.CLIPPER]
    
    for user in clipper_users:
        for i in range(10):  # 10 транзакций на пользователя
            amount_cents = random.randint(1000, 10000)  # €10-€100
            tx_type = random.choice([BalanceType.EARNING, BalanceType.PAYOUT])
            
            transaction = BalanceTransaction(
                user_id=user.id,
                amount_cents=amount_cents if tx_type == BalanceType.EARNING else -amount_cents,
                reason=f'Test transaction {i+1}',
                tx_type=tx_type,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90))
            )
            db.session.add(transaction)

if __name__ == '__main__':
    create_test_data()
