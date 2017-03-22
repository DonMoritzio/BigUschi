import pyinotify as pyno

wm = pyno.WatchManager()

mask = pyno.IN_CREATE

class EventHandler(pyno.ProcessEvent):
    def process_IN_CREATE(self, event):
        print(event.pathname)

handler = EventHandler()
notifier = pyno.Notifier(wm, handler)
wdd = wm.add_watch('/root/webcam/test', mask)
notifier.loop()
