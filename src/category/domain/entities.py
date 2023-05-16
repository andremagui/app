from collections import namedtuple
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, NamedTuple


@dataclass
class Category:
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )  # a way to make sure different values will be generated for every instance created






















# other ways to use it
# class Product(NamedTuple):
#    id: str
#    name: str#

# Product()
# Product = namedtuple("Product", ["id", "name"])

# Product()
