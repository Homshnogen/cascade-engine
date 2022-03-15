import tkinter as tk
#import random
#import threading
import time
#import numpy as np
#from PIL import ImageTk,Image

# todo: runtime test try block with hasattr

class mytime:
  def __enter__(self):
    self.t = time.time()
  
  def __exit__(self, e1, e2, e3):
    t = time.time() - self.t
    print("finished in time", t)

def auto(f): # can be used for local scoping variables
  return f()

def preset(f):
  def ret(*args):
    def ret():
      return f(*args)
    return ret
  return ret

def precomp(f):
  def ret(*args):
    x = f(*args)
    def ret():
      return x
    return ret
  return ret

def register(reg):
  try:
    reg.append
  except AttributeError:
    print("register unavailable")
    def iden(x):
      return x
    return iden
  def deco(f):
    reg.append(f)
    return f
  return deco

def registerargs(reg):
  try:
    reg.append
  except AttributeError:
    print("register unavailable")
    def iden(x):
      return x
    return iden
  def deco(f):
    def ret(*args):
      reg.append(args)
      return f(*args)
    return ret
  return deco

def registercall(reg):
  try:
    reg.append
  except AttributeError:
    print("register unavailable")
    def iden(x):
      return x
    return iden
  def deco(f):
    def ret(*args):
      reg.append((f,args))
      return f(*args)
    return ret
  return deco


class BranchingDialogue:
  @classmethod
  def from_list(C, path = [""]):
    ret = C(text = path[-1])
    for i in reversed(path[:-1]):
      ret = C(text = i, choices = [ret])
    return ret
  
  @classmethod
  def from_file(C, filepath):
    with open(filepath) as file:
      return file.readlines()
      for line in file.readlines():
        print(line)

  def __init__(self, *, text = "", choices = []):
    self.text = text
    self.choices = choices

  def choose(self, x):
    try:
      return self.choices[x]
    except IndexError:
      return None

class ETControls: # button controls
  # States: Off=0 Press=1, Hold=2, Release=3
  
  def __init__(self, keypairs, *, actions = 0):
    self.registry = {} # make this part of init
    for (key, action) in keypairs:
      if action >= actions:
        actions = action + 1
      self.registry[key] = action
    if self.registry == {}: # set default values
      pass #find a way to handle , probably throw an error
      #self.registry = {"Up": Up, "Down": Down, "Left": Left, "Right": Right}
    self.actions = actions
    self.action_range = range(actions)
    self.active = [False]*actions
    self.state = [0]*actions
  
  def add_action(self, key, action):
    if action >= self.actions:
      return # unhandled action
    self.registry.update(key, action)
  
  def remove_action(self, key, *, action = -1):
    self.registry.pop(key)
  
  def key_down(self, event):
    key_action = self.registry.get(event.keysym, -1)
    # Check if the pressed key is a valid key
    if key_action != -1:
      self.active[key_action] = True
  
  def key_up(self, event):
    key_action = self.registry.get(event.keysym, -1)
    # Check if the pressed key is a valid key
    if key_action != -1:
      self.active[key_action] = False
  
  def state_update(self): # please refactor this when complete
    for i in self.action_range:
      if (self.active[i]): # button is pressed
        if self.state[i] == 0:
          self.state[i] = 1
        elif self.state[i] == 1:
          self.state[i] = 2
        # elif self.state[i] is Hold:
        elif self.state[i] == 3:
          self.state[i] = 1
      else:
        #if self.state[i] is Off:
        if self.state[i] == 1:
          self.state[i] = 3
        elif self.state[i] == 2:
          self.state[i] = 3
        elif self.state[i] == 3:
          self.state[i] = 0
  
  def refresh(self):
    for i in self.action_range:
      self.state[i] = 0 # dead state
      self.active[i] = False # end activity
# end of ETControls class
  
class ETGame: # wrapper for Tk window object
  def destroy(self): 
    self.alive = False
    
  def focus_in(self, event):
    print('focus in')
    self.focus = True
    
  def focus_out(self, event):
    print('focus out')
    self.focus = False
    self.controls.refresh()
  
  def __init__(self, *, Controller = ETControls):
    # define globals with self and set initial values
    try: # type checking for Ctrl
      Controller.__init__
      Controller.refresh
      Controller.state_update
      Controller.key_up
      Controller.key_down
    except AttributeError:
      print ("Ctrl missing attributes")
      # handle wrong Ctrl
      Controller = ETControls
    self.controls = Controller([("Up", 0), ("Down", 1), ("Left", 2), ("Right", 3)]) # check type
    self.window = tk.Tk()
    self.window.title("Gameee")
    self.framerate = 30
    self.frame_length = 1/self.framerate
    self.alive = True
    self.focus = False
    self.canvas = tk.Canvas(
      self.window, # canvas parent object
      width=600, 
      height=300
    )
    self.canvas.pack() # formats the window to the elements
    self.window.bind("<FocusIn>", self.focus_in) # key press
    self.window.bind("<FocusOut>", self.focus_out) # key press
    self.window.bind("<KeyPress>", self.controls.key_down) # key press
    self.window.bind("<KeyRelease>", self.controls.key_up) # key press
    #self.window.bind("<Button-1>", self.controls.key_input) #mouse-1
    self.window.protocol("WM_DELETE_WINDOW", self.destroy)
  
  def game(self):
    for action in self.controls.action_range:
      if self.controls.state[action] != 0:
        print(f"state{self.controls.state[action]}, action{action}")
  
  def loop(self):
    next_frame = time.time() + 0.05 # framerate 20
    while self.alive: # change to object exist
      if self.focus: # only update if game is focused
        self.controls.state_update()
        self.game()
      self.window.update()
      while self.alive and (time.time() < next_frame):
        pass
      while next_frame < time.time():
        next_frame = next_frame + 0.05 # framerate 20
  
  def preload():
    pass
    # is this necessary or can it be moved to __init__ ?
  
  def start(self):
    self.preload()
    self.loop()
    # end the object components
    self.window.destroy()
# end class definition: ETGame

#game_instance = ETGame()
#game_instance.start()