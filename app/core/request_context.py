from contextvars import ContextVar

request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)

def set_request_id(request_id: str):
    print(f"inside set mthod {request_id}")
    request_id_context.set(request_id)

def get_request_id():
    return request_id_context.get()