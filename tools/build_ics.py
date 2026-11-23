import json,sys
from datetime import datetime,timedelta,date,timezone
root=sys.argv[1]
d=json.load(open(root+'/events.json'))
L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Exam Calendar//EN","CALSCALE:GREGORIAN","X-WR-CALNAME:Exams 2026/27","X-WR-TIMEZONE:Europe/London",
"BEGIN:VTIMEZONE","TZID:Europe/London","BEGIN:DAYLIGHT","TZOFFSETFROM:+0000","TZOFFSETTO:+0100","TZNAME:BST","DTSTART:19700329T010000","RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU","END:DAYLIGHT",
"BEGIN:STANDARD","TZOFFSETFROM:+0100","TZOFFSETTO:+0000","TZNAME:GMT","DTSTART:19701025T020000","RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU","END:STANDARD","END:VTIMEZONE"]
esc=lambda s:s.replace("\\","\\\\").replace(",",r"\,").replace(";",r"\;")
code={"SAS":"EN2721","DESIGN":"EN2710","GEN":""}
for e in d['events']:
    if 'date' not in e or date.fromisoformat(e['date'])<date(2026,11,8): continue
    dt=date.fromisoformat(e['date']); lab=code.get(e['mod'],e['mod'])
    summ=(f"{lab} {d['modules'][e['mod']]}: " if lab else "")+e['title']+(f" ({e['weight']})" if e.get('weight') else "")
    L+=["BEGIN:VEVENT",f"UID:examcal-{e['mod']}-{''.join(c for c in e['title'] if c.isalnum())[:16]}-{e['date']}@exam-calendar",f"DTSTAMP:{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}",f"SUMMARY:{esc(summ)}"]
    if e.get('start'):
        s=datetime.fromisoformat(e['date']+"T"+e['start']); en=datetime.fromisoformat(e['date']+"T"+e['end']) if e.get('end') else s+timedelta(minutes=50)
        L+=[f"DTSTART;TZID=Europe/London:{s:%Y%m%dT%H%M%S}",f"DTEND;TZID=Europe/London:{en:%Y%m%dT%H%M%S}"]
    else: L+=[f"DTSTART;VALUE=DATE:{dt:%Y%m%d}",f"DTEND;VALUE=DATE:{dt+timedelta(days=1):%Y%m%d}"]
    if e.get('room'): L.append(f"LOCATION:{esc(e['room'])}")
    if e.get('note'): L.append("DESCRIPTION:"+esc(e['note']))
    for t in ("-P7D","-P2D"): L+=["BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:"+esc(summ),"TRIGGER:"+t,"END:VALARM"]
    L.append("END:VEVENT")
L.append("END:VCALENDAR")
open(root+'/exams-2026-27.ics','w').write("\r\n".join(L)+"\r\n")
print(sum(1 for l in L if l=="BEGIN:VEVENT"),"events")
