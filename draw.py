from pynput import keyboard
from pynput.mouse import Button, Controller

mouse = Controller()

seven_seg={
"a":[1,1,1,0,1,1,1],
"b":[1,1,1,1,1,1,1],
"c":[1,0,0,1,1,1,0],
"d":[0,1,1,1,1,0,1],
"e":[1,0,0,1,1,1,1],
"f":[1,0,0,0,1,1,1],
"g":[1,0,1,1,1,1,0],
"h":[0,1,1,0,1,1,1],
"i":[0,0,0,0,1,1,0],
"j":[0,1,1,1,1,0,0],
"k":[1,0,1,0,1,1,0],
"l":[0,0,0,1,1,1,0],
"m":[1,1,0,1,0,1,0],
"n":[0,0,1,0,1,0,1],
"o":[1,1,1,1,1,1,0],
"p":[1,1,0,0,1,1,1],
"q":[1,1,1,0,0,1,1],
"r":[0,0,0,0,1,0,1],
"s":[1,0,1,1,0,1,1],
"t":[0,0,0,1,1,1,1],
"u":[0,1,1,1,1,1,0],
"v":[0,1,1,1,0,1,0],
"w":[1,0,1,1,1,0,0],
"x":[1,0,0,1,0,0,1],
"y":[0,1,1,1,0,1,1],
"z":[1,1,0,1,1,0,1],
" ":[0,0,0,0,0,0,0]
}

font=2                  # font size, scales everything up or down
length=10               # lenght in px of one segment of the 7 segment display
length=length*font
is_script_active=False  # don't draw if script is not active, activity can be toggled by pressing '+'


def moveRel(x,y):       # move relative to the current position
    mouse.move(x,y)

def dragRel(x,y):       # drag relative to the current position
    mouse.press(Button.left)
    mouse.move(x,y)
    mouse.release(Button.left)

def draw_segments(seg_val):
    seven_seg_points=[(0,0),(length,0),(0,length),(0,length),(-length,0),(0,-length),(0,-length),(0,0)] # coordinate of all the segments relative to the last segment in the list.
    for i in range(6):
        x=seven_seg_points[i+1][0]
        y=seven_seg_points[i+1][1]
        if seg_val[i]==1:
            dragRel(x,y)
        else:
            moveRel(x,y)

    if seg_val[6]==1:
        moveRel(0,length)
        dragRel(length,0)
        moveRel(-length,-length) # end in top right

def draw_questionmark(inp_):
    print("cannot draw",inp_)
    straight=5*font
    slant=7*font
    moveRel(0,straight)
    dragRel(slant,-straight)
    dragRel(slant,straight)
    dragRel(-slant,straight)
    dragRel(0,straight)
    moveRel(0,int(0.6*straight))
    dragRel(0,int(0.4*straight))
    moveRel(-straight,-4*straight) #end in top right

def draw_chars(inp_txt):
    i=int(1.4*length) # this makes sure there is a gap of .4*length between two different characters

    for x in inp_txt:
        if x in seven_seg: # draw the char can be drawn, else draw a question mark
            to_disp=seven_seg[x]
            draw_segments(to_disp)
        else:
            draw_questionmark(x)

        moveRel(i,0) #move aside and get ready for next char

def on_press(key):
    global is_script_active
    try:
        inp=key.char
    except:
        inp=str(key)
    if inp=="-":
        exit()
    elif inp=="+":
        is_script_active = not is_script_active     # toggle activity
        if is_script_active:
            print("script turned on")
        else:
            print("script turned off")
    elif is_script_active:
        if inp=="Key.space":
            inp=" "
        if inp:                  # if inp is not none
            draw_chars(inp[0])   # draw the first char

print("ready to go!")
print("press '+' when you are ready to start drawing")
print("press '-' to exit")

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()
keyboard_listener.join()
