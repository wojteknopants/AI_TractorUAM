#from queue import PriorityQueue
import heapq

class Wrap: #needed for heapq to compare only priority and not Tile objects. Annoying
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item
    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        else: 
            return False

class PriorityQ:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, Wrap(priority, item))
    
    def get(self):
        wrapbuff = heapq.heappop(self.elements)
        return wrapbuff.item

def heuristic(a, b): #Manhattan
    (x1, y1) = a.xy
    (x2, y2) = b.xy
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(start, goal):
    frontier            = PriorityQ()
    frontier.put(start, 0)
    came_from           = {} #tracks parents of each node (tile) during pathfinding
    cost_so_far         = {} #keeps total g cost from start for each node (tile) considered
    came_from[start]    = None
    cost_so_far[start]  = 0
    
    while not frontier.empty(): #if there is node (tile) still to consider, take one with lowest f 
        current = frontier.get()
        
        
        if current.xy == goal.xy:
            break
        
        for next in current.neighbors():
            new_cost = cost_so_far[current] + next.g #calculating total g cost for new node 
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost 
                priority          = new_cost + heuristic(next, goal) #calculating f = g+h
                frontier.put(next, priority)
                came_from[next]   = current
    
    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):

    current = goal
    path = []
    while current != start: # note: this will fail if no path found
        path.append(current.xy)
        current = came_from[current]
    path.append(start.xy) # optional
    path.reverse() # optional
    return path