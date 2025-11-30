"""Data models for the clothing store application"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """Product model for clothing store items"""
    id: int
    name: str
    category: str
    price: float
    size: str
    color: str
    image_url: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert product to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "size": self.size,
            "color": self.color,
            "image_url": self.image_url
        }

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', category='{self.category}', price={self.price}, size='{self.size}', color='{self.color}')"
