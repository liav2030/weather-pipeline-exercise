import os, time, json, requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import pika

load_dotenv()

OWM_KEY = os.getenv("OWM_API_KEY")
CITY = os.getenv("CITY", "London")
INTERVAL = int(os.getenv("SAMPLE_INTERVAL_SEC", "3600"))
RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@localhost:5672/%2f")
QUEUE = os.getenv("QUEUE", "weather")

def sample_weather(city: str) -> dict:
    if not OWM_KEY:
        raise RuntimeError("Missing OWM_API_KEY")
    r = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": OWM_KEY, "units": "metric"},
        timeout=10,
    )
    r.raise_for_status()
    d = r.json()
    time_iso = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    return {"city": city, "temp_c": d["main"]["temp"], "time_iso": time_iso}

def publish(msg: dict):
    params = pika.URLParameters(RABBIT_URL)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE, durable=True)
    ch.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body=json.dumps(msg).encode("utf-8"),
        properties=pika.BasicProperties(content_type="application/json", delivery_mode=2)
    )
    conn.close()

def main():
    while True:
        try:
            data = sample_weather(CITY)
            print(json.dumps(data, ensure_ascii=False), flush=True)  
            publish(data)
        except Exception as e:
            err = {"error": str(e), "city": CITY, "time_iso": datetime.now(timezone.utc).isoformat(timespec="milliseconds")}
            print(json.dumps(err, ensure_ascii=False), flush=True)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
