from datetime import datetime, timezone
def gettime(time: str) -> datetime:
	year = int(time[0:4])
	month = int(time[5:7])
	day = int(time[8:10])
	return datetime(year, month, day)