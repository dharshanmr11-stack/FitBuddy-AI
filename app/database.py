from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

from .config import DATABASE_URL


# SQLite configuration
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


# Database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


# Database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class
Base = declarative_base()


# -----------------------------
# USER TABLE
# -----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(100),
        nullable=False
    )

    user_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String(200),
        nullable=False
    )

    intensity = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # One user can have many plans
    plans = relationship(
        "Plan",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# -----------------------------
# PLAN TABLE
# -----------------------------
class Plan(Base):
    __tablename__ = "plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Proper foreign key added here
    user_id = Column(
        String(100),
        ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        nullable=True
    )

    # Relationship back to User
    user = relationship(
        "User",
        back_populates="plans"
    )


# -----------------------------
# CREATE DATABASE TABLES
# -----------------------------
def init_db():
    Base.metadata.create_all(
        bind=engine
    )


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# -----------------------------
# SAVE / UPDATE USER
# -----------------------------
def save_user(
    db,
    username,
    user_id,
    age,
    weight,
    goal,
    intensity
):
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user:
        user.username = username
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity

    else:
        user = User(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    return user


# -----------------------------
# SAVE PLAN
# -----------------------------
def save_plan(
    db,
    user_id,
    original_plan,
    nutrition_tip
):
    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


# -----------------------------
# GET USER
# -----------------------------
def get_user(db, user_id):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


# -----------------------------
# GET LATEST PLAN
# -----------------------------
def get_latest_plan(db, user_id):
    return (
        db.query(Plan)
        .filter(Plan.user_id == user_id)
        .order_by(Plan.id.desc())
        .first()
    )


# -----------------------------
# UPDATE PLAN
# -----------------------------
def update_plan(
    db,
    plan,
    updated_plan,
    feedback
):
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    plan.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(plan)

    return plan


# -----------------------------
# GET ALL USERS
# -----------------------------
def get_all_users(db):
    return (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )