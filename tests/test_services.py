import pytest
from app.services import TradeProcessor
from app.models import TradeEvent

def make_event(**overrides):
    base = dict(
        trade_id="T123",
        symbol="AAPL",
        side="BUY",
        price=100.0,
        quantity=5,
        timestamp="2025-07-31T12:00:00Z",
    )
    base.update(overrides)
    return TradeEvent(**base)

def test_process_computes_notional_and_signed_notional():
    proc = TradeProcessor()
    ev = make_event(side="SELL", price=200.25, quantity=4)
    result = proc.process(ev)
    assert result["notional"] == 801.0
    assert result["signed_notional"] == -801.0
    assert result["symbol"] == "AAPL"

@pytest.mark.parametrize("field, value, msg", [
    ("trade_id", "", "trade_id is required"),
    ("quantity", 0, "quantity must be > 0"),
    ("price", -1, "price must be > 0"),
    ("side", "LONG", "side must be BUY or SELL"),
])
def test_validate_raises_for_bad_inputs(field, value, msg):
    proc = TradeProcessor()
    ev = make_event(**{field: value})
    with pytest.raises(ValueError) as e:
        proc.process(ev)
    assert msg in str(e.value)