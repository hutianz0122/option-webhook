from fastapi import FastAPI, Request
from logger_utils import (
    append_raw_signal_log,
    append_normalized_signal_log,
    append_rejected_signal_log,
    append_routed_signal_log
)
from normalizer import normalize_raw_signal
from validator import validate_signal
from router import route_signal


app = FastAPI()


@app.get("/")
def root():
    return {"message": "server running"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    append_raw_signal_log(payload=data, status="received")

    normalized_signal = normalize_raw_signal(data)
    is_valid, errors = validate_signal(normalized_signal)

    if not is_valid:
        append_rejected_signal_log(payload=data, errors=errors, status="rejected")
        return {
            "status": "rejected",
            "errors": errors,
            "normalized_signal": normalized_signal,
        }

    append_normalized_signal_log(signal=normalized_signal, status="normalized")

    routed_signal = route_signal(normalized_signal)
    append_routed_signal_log(routed_signal=routed_signal, status="routed")

    print("Webhook received payload:", data)
    print("Normalized signal:", normalized_signal)
    print("Routed signal:", routed_signal)

    return {
        "status": "accepted",
        "normalized_signal": normalized_signal,
        "routed_signal": routed_signal,
    }