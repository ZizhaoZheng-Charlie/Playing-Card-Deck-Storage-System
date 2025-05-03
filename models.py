from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    LargeBinary,
    ForeignKey,
    Boolean,
    Float,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    shop_website = Column(String(255))
    company_name = Column(String(100))
    items = relationship("Item", back_populates="series")
    wish_items = relationship("WishItem", back_populates="series")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    series_id = Column(Integer, ForeignKey("series.id"))
    quantity = Column(Integer, default=1)
    image = Column(LargeBinary, nullable=True)
    image_name = Column(String(255), nullable=True)

    # Status fields
    is_signature = Column(Boolean, default=False)
    is_gilded = Column(Boolean, default=False)
    is_sealed = Column(Boolean, default=False)

    series = relationship("Series", back_populates="items")


class WishItem(Base):
    __tablename__ = "wish_items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    series_id = Column(Integer, ForeignKey("series.id"))
    expected_price = Column(String(100), nullable=True)
    shop_url = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    priority = Column(String(20), default="Medium")

    # Status fields
    is_signature = Column(Boolean, default=False)
    is_gilded = Column(Boolean, default=False)
    is_sealed = Column(Boolean, default=False)

    series = relationship("Series", back_populates="wish_items")


# Create database and tables
engine = create_engine("sqlite:///storage.db")
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)
