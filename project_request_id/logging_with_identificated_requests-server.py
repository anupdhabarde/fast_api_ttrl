import uuid
import contextvars
import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
request_id_contextvar = contextvars.ContextVar("request_id", default=None)


def debug(message):
    request_id = request_id_contextvar.get()
    print(f"({request_id}) {message}")


def divide(a, b):
    debug(f"Dividing {a} / {b} ...")
    result = a / b
    debug(f"Result is {result}")


@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request_id_contextvar.set(request_id)
    debug("Request started")

    try:
        return await call_next(request)

    except Exception as ex:
        debug(f"Request failed: {ex}")
        return JSONResponse(content={"success": False}, status_code=500)

    finally:
        assert request_id_contextvar.get() == request_id
        debug("Request ended")


@app.get("/")
async def read_root():
    a = 100
    b = random.randint(0, 1)
    return {"success": True, "result": divide(a, b)}


if __name__ == "__main__":
    uvicorn.run(app)
