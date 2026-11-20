from datetime import date, timedelta
def week_bounds(day):
    start=day-timedelta(days=day.weekday()); return start,start+timedelta(days=6)
def month_bounds(day):
    import calendar
    return date(day.year,day.month,1),date(day.year,day.month,calendar.monthrange(day.year,day.month)[1])
def test_sunday_week():
    assert week_bounds(date(2026,11,22))==(date(2026,11,16),date(2026,11,22))
def test_month_end():
    assert month_bounds(date(2026,10,31))==(date(2026,10,1),date(2026,10,31))
def test_leap_year():
    assert month_bounds(date(2028,2,1))[1]==date(2028,2,29)
def test_year_rollover():
    assert week_bounds(date(2027,1,1))==(date(2026,12,28),date(2027,1,3))
