from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    shop_website = Column(String(200))
    company_name = Column(String(100))
    items = relationship("Item", back_populates="series")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    series_id = Column(Integer, ForeignKey("series.id"))
    quantity = Column(Integer, default=0)
    image = Column(LargeBinary)
    image_name = Column(String(200))

    series = relationship("Series", back_populates="items")


# Create database and tables
engine = create_engine("sqlite:///storage.db")
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)
