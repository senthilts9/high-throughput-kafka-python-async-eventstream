from app.models import TradeEvent

class TradeProcessor:
    def __init__(self):
        pass

    def validate(self, event: TradeEvent):
        if not event.trade_id:
            raise ValueError("trade_id is required")
        if event.quantity <= 0:
            raise ValueError("quantity must be > 0")
        if event.price <= 0:
            raise ValueError("price must be > 0")
        if event.side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")

    def process(self, event: TradeEvent) -> dict:
        self.validate(event)
        notional = round(event.price * event.quantity, 6)
        side_sign = 1 if event.side == "BUY" else -1
        return {
            "trade_id": event.trade_id,
            "symbol": event.symbol,
            "side": event.side,
            "quantity": event.quantity,
            "price": event.price,
            "notional": notional,
            "signed_notional": side_sign * notional,
            "timestamp": event.timestamp,
        }