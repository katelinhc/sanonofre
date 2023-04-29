from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class DailyReadinessContributors(BaseModel): 
    activity_balance: Optional[int] = None 
    body_temperature: Optional[int] = None 
    hrv_balance: Optional[int] = None 
    previous_day_activity: Optional[int] = None 
    previous_night: Optional[int] = None 
    recovery_index: Optional[int] = None 
    resting_heart_rate: Optional[int] = None 
    sleep_balance: Optional[int] = None

class DailyReadiness(BaseModel): 
    id: str 
    day: date 
    score: Optional[int] = None 
    temperature_deviation: Optional[float] = None 
    temperature_trend_deviation: Optional[float] = None 
    timestamp: datetime 
    contributors: DailyReadinessContributors

class DailySleepContributors(BaseModel): 
    deep_sleep: Optional[int] = None 
    efficiency: Optional[int] = None 
    latency: Optional[int] = None 
    rem_sleep: Optional[int] = None 
    restfulness: Optional[int] = None 
    timing: Optional[int] = None 
    total_sleep: Optional[int] = None

class DailySleep(BaseModel): 
    id: str
    day: date 
    score: int 
    timestamp: datetime 
    contributors: DailySleepContributors

class Heartrate(BaseModel): 
    bpm: Optional[int] 
    source: Optional[str] 
    timestamp: Optional[datetime]

class Tag(BaseModel): 
    test: str

class SleepHeartRate(BaseModel): 
    interval: Optional[float] = 0 
    items: Optional[List[Optional[int]]] = []

class SleepHRV(BaseModel): 
    interval: Optional[float] = 0 
    items: Optional[List[Optional[float]]] = []

class SleepReadiness(BaseModel): 
    contributors: DailyReadinessContributors 
    score: Optional[int] = None
    temperature_deviation: Optional[float] = None 
    temperature_trend_deviation: Optional[float] = None

class Sleep(BaseModel): 
    id: str 
    average_breath: float 
    average_heart_rate: float 
    average_hrv: Optional[float]  
    awake_time: int 
    bedtime_end: datetime 
    bedtime_start: datetime 
    day: date 
    deep_sleep_duration: int 
    efficiency: int 
    heart_rate: Optional[SleepHeartRate] 
    timestamp: Optional[datetime] = None 
    hrv: Optional[SleepHRV] 
    latency: int 
    light_sleep_duration: int 
    low_battery_alert: bool 
    lowest_heart_rate: Optional[int] 
    movement_30_sec: str 
    period: int 
    readiness: Optional[SleepReadiness]
    readiness_score_delta: Optional[float] = 0 
    rem_sleep_duration: int 
    restless_periods: int 
    sleep_phase_5_min: str 
    sleep_score_delta: Optional[float] 
    time_in_bed: int 
    total_sleep_duration: int 
    type: str

class Tag(BaseModel): 
    id: str 
    day: date 
    text: Optional[str] 
    timestamp: datetime 
    tags: List[str]
