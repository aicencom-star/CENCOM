from app.src.database import engine
from app.src.models.base import Base
from app.src.models.user import User


print("Dang tao bang database...")

Base.metadata.create_all(bind=engine)

print("Tao bang thanh cong.")