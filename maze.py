from PIL import Image, ImageDraw
import math
import random

width = 1600
height = 800
cell_size = 50
cols = math.floor(width / cell_size)
rows = math.floor(height / cell_size)
grid = []
current = ''
stack = []
#  Helpers + Classes ====================
def index(x, y):
  if (x < 0 or y < 0 or x > cols - 1 or y > rows - 1):
    return -1
  else:
    return x + y * cols

def remove_walls(a, b): # remove wall between two cells
  x = a.x - b.x
  if (x == 1):
    a.walls[3] = False
    b.walls[1] = False
  elif (x == -1):
    a.walls[1] = False
    b.walls[3] = False

  y = a.y - b.y
  if (y == 1):
    a.walls[0] = False
    b.walls[2] = False
  elif (y == -1):
    a.walls[2] = False
    b.walls[0] = False

def get_cell(cells, x, y):
  for i in cells:
    if i.x == x and i.y == y:
      return i

def get_path(a, b): # return a possbile path between points
  stack = []
  current = a
  current.solutionVisited = True
  next_cell = current.check_neighbours(solutionCheck=True)
  solution = [a]

  while (next_cell or len(stack) > 0):
    next_cell = current.check_neighbours(solutionCheck=True)
    if (next_cell):
      next_cell.solutionVisited = True
      stack.append(current)
      current = next_cell
      solution.append(current)
    elif len(stack) > 0:
      current = stack.pop()
      solution.pop()

    if (current.x == b.x and current.y == b.y):
      break
      
  return solution

class Cell:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.walls = [True, True, True, True]
    self.visited = False
    self.solutionVisited = False
    
  def show(self, ctx):
    x = self.x * cell_size
    y = self.y * cell_size
    w = cell_size
    lw = 37
    le = int(lw/2) # dealing with line end lengths
    leOff = le - 1 if (lw % 2 == 0) else le

    if (self.walls[0]):
      ctx.line((x - leOff, y, x + w + le, y), fill='black', width=lw)
    if (self.walls[1]):
      ctx.line((x + w, y - leOff, x + w, y + w + le), fill='black', width=lw)
    if (self.walls[2]):
      ctx.line((x - leOff, y + w, x + w + le, y + w), fill='black', width=lw)
    if (self.walls[3]):
      ctx.line((x, y - leOff, x, y + w + le), fill='black', width=lw)

  def highlight(self, ctx, col2=False, index=None):
    x = self.x * cell_size
    y = self.y * cell_size
    w = cell_size
    margin = 3
    col = 'yellow' if col2 else 'blue'
    ctx.rectangle((x, y, x + w, y + w), outline=None, fill=(105, 200, 255))

    # ctx.ellipse((x + margin, y + margin, x + w - margin, y + w - margin), outline=None, fill=col)

    if (index):
      ctx.text((x,y), str(index),fill=(255,255,255))


  def check_neighbours(self, solutionCheck=False):
    neighbours = []
    indices = {
      "top": index(self.x, self.y - 1),
      "right": index(self.x + 1, self.y),
      "bottom": index(self.x, self.y + 1),
      "left": index(self.x - 1, self.y)
    }

    top = grid[indices['top']] if indices['top'] > -1 else None
    right = grid[indices['right']] if indices['right'] > -1 else None
    bottom = grid[indices['bottom']] if indices['bottom'] > -1 else None
    left = grid[indices['left']] if indices['left'] > -1 else None

    if (not solutionCheck):
      if (top and not top.visited):
        neighbours.append(top)
      if (right and not right.visited):
        neighbours.append(right)
      if (bottom and not bottom.visited):
        neighbours.append(bottom)
      if (left and not left.visited):
        neighbours.append(left)
    else:
      if (top and not top.solutionVisited and not top.walls[2]):
        neighbours.append(top)
      if (right and not right.solutionVisited and not right.walls[3]):
        neighbours.append(right)
      if (bottom and not bottom.solutionVisited and not bottom.walls[0]):
        neighbours.append(bottom)
      if (left and not left.solutionVisited and not left.walls[1]):
        neighbours.append(left)

    if (len(neighbours) > 0):
      z = random.choice(neighbours)
      return z
    else:
      return

# Create image doc
img = Image.new('RGB', (width, height), "white")

# Creating data ============
for j in range(rows):
  for i in range(cols):
    cell = Cell(i, j)
    grid.append(cell)

current = grid[0]
current.visited = True
next_cell = current.check_neighbours()

while (next_cell or len(stack) > 0):
  next_cell = current.check_neighbours()
  if (next_cell):
    next_cell.visited = True
    stack.append(current)
    remove_walls(current, next_cell)
    current = next_cell
  elif len(stack) > 0:
    current = stack.pop()

cellone = get_cell(grid, 0, 0)
celltwo = get_cell(grid, cols-1, 2)
solution = get_path(cellone, celltwo)

# Drawing data =============
ctx = ImageDraw.Draw(img)
for i in range(len(solution)):
  cell = solution[i]
  cell.highlight(ctx)

cellone.highlight(ctx, col2=True)
celltwo.highlight(ctx, col2=True)
for i in grid:
  i.show(ctx)

img.show()
# img.save('./one.png', 'PNG')