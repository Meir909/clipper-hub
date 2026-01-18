from app import create_app
from app.extensions import db
from app.models import PaymentType, Project, Role, User

app = create_app()


def bootstrap():
    with app.app_context():
        if not User.query.filter_by(email="admin@clipper.io").first():
            admin = User(email="admin@clipper.io", role=Role.ADMIN, display_name="Clipper Admin")
            admin.set_password("AdminPass123!")
            db.session.add(admin)
            print("Created admin: admin@clipper.io / AdminPass123!")
        else:
            print("Admin already exists")

        manager = User.query.filter_by(email="manager@clipper.io").first()
        if not manager:
            manager = User(email="manager@clipper.io", role=Role.MANAGER, display_name="DACH Manager")
            manager.set_password("ManagerPass123!")
            db.session.add(manager)
            print("Created manager: manager@clipper.io / ManagerPass123!")

        clipper = User.query.filter_by(email="clipper@clipper.io").first()
        if not clipper:
            clipper = User(email="clipper@clipper.io", role=Role.CLIPPER, display_name="First Clipper")
            clipper.set_password("ClipperPass123!")
            db.session.add(clipper)
            print("Created clipper: clipper@clipper.io / ClipperPass123!")

        if not Project.query.first():
            project = Project(
                title="Swiss Fintech Launch",
                description="Film a 30s TikTok about our Swiss fintech app with focus on security and elegance.",
                earning_conditions="€20 per approved video with >800 views.",
                payment_type=PaymentType.FIX_PER_VIDEO,
                fixed_reward_cents=2000,
                kpi_views=800,
                submission_limit_per_user=3,
                instruction_url="https://notion.so/clipper-brief",
                manager_id=manager.id if manager else None,
            )
            db.session.add(project)
            print("Seeded Swiss Fintech Launch project")

        db.session.commit()


if __name__ == "__main__":
    bootstrap()
