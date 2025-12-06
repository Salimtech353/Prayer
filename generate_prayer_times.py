import json
from datetime import datetime
from hijri_converter import Gregorian
from praytimes import PrayTimes  # pip install praytimes

# ---------- আপনার লোকেশন ----------
LAT = 23.8103
LON = 90.4125
METHOD = 'ISNA'  # Islam Society of North America
TIMEZONE = 6.0   # Bangladesh

# ---------- তারিখ ----------
today = datetime.now()
gregorian_date = today.strftime("%d-%m-%Y")
weekday = today.strftime("%A")
month_name = today.strftime("%B")
year = today.year

# হিজরি তারিখ
hijri_date = Gregorian(today.year, today.month, today.day).to_hijri()
hijri_date_str = f"{hijri_date.day:02d}-{hijri_date.month:02d}-{hijri_date.year}"
hijri_weekday = hijri_date.weekday_name()
hijri_month = hijri_date.month_name()
hijri_year = hijri_date.year

# ---------- নামাজের সময় ----------
pt = PrayTimes(METHOD)
times = pt.get_times(
    date=(today.year, today.month, today.day),
    coords=(LAT, LON),
    timezone=TIMEZONE
)

timings = {
    "Fajr": times['fajr'],
    "Sunrise": times['sunrise'],
    "Dhuhr": times['dhuhr'],
    "Asr": times['asr'],
    "Sunset": times['sunset'],
    "Maghrib": times['maghrib'],
    "Isha": times['isha'],
    "Imsak": times['imsak'],
    "Midnight": times['midnight']
}

# ---------- JSON বানানো ----------
data = {
    "code": 200,
    "status": "OK",
    "data": {
        "timings": timings,
        "date": {
            "readable": today.strftime("%d %b %Y"),
            "timestamp": str(int(today.timestamp())),
            "gregorian": {
                "date": gregorian_date,
                "format": "DD-MM-YYYY",
                "weekday": {"en": weekday},
                "month": {"number": today.month, "en": month_name},
                "year": str(year)
            },
            "hijri": {
                "date": hijri_date_str,
                "format": "DD-MM-YYYY",
                "weekday": {"en": hijri_weekday},
                "month": {"number": hijri_date.month, "en": hijri_month},
                "year": str(hijri_year)
            }
        },
        "location": {
            "latitude": LAT,
            "longitude": LON,
            "method": {"id": 2, "name": METHOD},
            "school": "Standard"
        }
    }
}

# ---------- JSON ফাইলে লেখা ----------
with open('prayer-timings.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Prayer timings JSON তৈরি হয়েছে।")