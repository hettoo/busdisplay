from tkinter import *
import urllib.request
import json
import time

INTERVAL = 60
SLEEP_TIME = 0.05
HEAD_SIZE = 44
TIME_SIZE = 34
XMARGIN = 50
YMARGIN = 110
HEAD_GAP = 5
ITEM_GAP = 180
CLOCK_MARGIN = 50
CLOCK_SIZE = 44
FONT = 'Droid Sans'

def req(query):
    try:
        page = urllib.request.urlopen('https://api.tfl.gov.uk/%s?app_id=%s&app_key=%s' % (query, app_id, app_key))
        j = page.read()
        return json.loads(j)
    except:
        return []

def countdown(l, t):
    for i in range(0, len(l)):
        if l[i] > t:
            l[i] -= t
        else:
            l[i] = 0

def getTimes(id, line = ''):
    items = req('StopPoint/%s/arrivals' % id)
    if (line != ''):
        items = list(filter(lambda i : i['lineName'] == line, items))
    return sorted(list(map(lambda i : i['timeToStation'], items)))

def formatTimes(l):
    s = ''
    for time in l:
        if s != '':
            s += ', '
        s += str(time // 60)
    return s

def key(event):
    if event.char == 'q':
        root.destroy()

root = Tk()
root.bind_all('<Key>', key)
root.attributes('-fullscreen', True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
canvas = Canvas(root, width=width, height=height, bg='black')
canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

x = XMARGIN
y = YMARGIN

head1 = canvas.create_text(x, y, font=(FONT, HEAD_SIZE), anchor='sw', fill='#ff9944')
canvas.itemconfig(head1, text='91 & N91 --- 2 / 1')

y += HEAD_GAP

time1 = canvas.create_text(x, y, font=(FONT, TIME_SIZE), anchor='nw', fill='#ff9944')

y += ITEM_GAP

head2 = canvas.create_text(x, y, font=(FONT, HEAD_SIZE), anchor='sw', fill='#ff9944')
canvas.itemconfig(head2, text='210 --- 3 / 3')

y += HEAD_GAP

time2 = canvas.create_text(x, y, font=(FONT, TIME_SIZE), anchor='nw', fill='#ff9944')

y += ITEM_GAP

head3 = canvas.create_text(x, y, font=(FONT, HEAD_SIZE), anchor='sw', fill='#ff9944')
canvas.itemconfig(head3, text='41 --- 9 / 8')

y += HEAD_GAP

time3 = canvas.create_text(x, y, font=(FONT, TIME_SIZE), anchor='nw', fill='#ff9944')

clock = canvas.create_text(width - CLOCK_MARGIN, height - CLOCK_MARGIN, font=(FONT, CLOCK_SIZE), anchor='se', fill='red')

times91s = []
times91n = []
times210w = []
times210e = []
times41w = []
times41e = []

def drawTimes():
    canvas.itemconfig(time1, text='South: ' + formatTimes(times91s) + ' / North: ' + formatTimes(times91n))
    canvas.itemconfig(time2, text='West: ' + formatTimes(times210w) + ' / East: ' + formatTimes(times210e))
    canvas.itemconfig(time3, text='West: ' + formatTimes(times41w) + ' / East: ' + formatTimes(times41e))
    canvas.itemconfig(clock, text=time.strftime('%a %d %b, %H:%M', time.localtime()))

app_id = ''
app_key = ''

with open('key') as fp:
    app_id = fp.readline().strip()
    app_key = fp.readline().strip()

last = time.time()
extra = 0.0
update = last

while True:
    current = time.time()
    if current >= update:
        times91s = getTimes('490013692S')
        times91n = getTimes('490003695N')
        times210w = getTimes('490008366W')
        times210e = getTimes('490007751S', '210')
        times41w = getTimes('490007971W', '41')
        times41e = getTimes('490007971E', '41')
        last = time.time()
        extra = 0.0
        update = last + INTERVAL
    else:
        realdiff = current - last + extra
        diff = int(realdiff)
        extra = realdiff - diff
        countdown(times91s, diff)
        countdown(times91n, diff)
        countdown(times210w, diff)
        countdown(times210e, diff)
        countdown(times41w, diff)
        countdown(times41e, diff)
        last = current
    drawTimes()
    root.update()
    time.sleep(SLEEP_TIME)
