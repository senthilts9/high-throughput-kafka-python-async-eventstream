from dataclasses import dataclass, asdict
from datetime import datetime
import json

@dataclass
class TradeEvent:
    trade_id: str
    symbol: str
    side: str
    price: float
    quantity: int
    timestamp: str

    def to_json(self):
        return json.dumps(asdict(self))