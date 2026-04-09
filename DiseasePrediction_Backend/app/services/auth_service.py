# from app.database.db import SessionLocal
# from app.database.models import User
# from app.core.security import hash_password, verify_password, create_token
# from app.database.models import LoginLog
# from app.database.db import SessionLocal



from app.database.db import SessionLocal
from app.database.models import User, LoginLog
from app.core.security import hash_password, verify_password, create_token
db = SessionLocal()

def register_user(data):
    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        return {"error": "Email already exists"}

    user = User(
    name=data.name,
    age=data.age,
    phone=data.phone,
    email=data.email,
    password=hash_password(data.password)
)

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}


def login_user(data):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        return {"error": "Invalid credentials"}

    token = create_token({"email": user.email})

    # ✅ ADD THIS PART (LOGIN TRACKING)
    log = LoginLog(user_id=user.id)
    db.add(log)
    db.commit()

    # ✅ MODIFY RETURN (ADD user_id)
    return {
        "access_token": token,
        "user_id": user.id
    }


def forgot_password(email):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "User not found"}

    # In real app → send email
    return {"message": "Reset allowed (simulate email sent)"}


def reset_password(data):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return {"error": "User not found"}

    user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}