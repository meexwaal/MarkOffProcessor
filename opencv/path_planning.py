import queue

neighborLists = {}

def initGraph(x, y):
  return [[True for i in range(y)] for j in range(x)]

def neighbors(node, graph):
  if node in neighborLists:
    return neighborLists[node]
  dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
  result = []
  for dir in dirs:
    nx = node[0] + dir[0]
    ny = node[1] + dir[1]
    if 0 <= nx < len(graph) and 0 <= ny < len(graph[0]) and graph[nx][ny]:
      result.append((nx, ny))
  neighborLists[node] = result
  return result

def dist(a, b):
  (x1, y1) = a
  (x2, y2) = b
  return abs(x1 - x2) + abs(y1 - y2)

def aStarSearch(graph, start, goal, cameFrom):
  pq = queue.PriorityQueue()
  pq.put((0, start))
  costSoFar = {}
  costSoFar[start] = 0

  while not pq.empty():
    (ret, current) = pq.get()

    if current == goal:
      break

    for next in neighbors(current, graph):
      newCost = costSoFar[current] + 1
      if next not in costSoFar or newCost < costSoFar[next]:
        costSoFar[next] = newCost
        priority = newCost + dist(goal, next)
        pq.put((priority, next))
        cameFrom[next] = current

  return cameFrom

def removeNodes(nodesList, graph):
  for n in nodesList:
    (x, y) = n
    graph[x][y] = False
  return graph

def planPathRecurse(start, nodesList, graph, path):
  if not nodesList:
    return path
  cameFrom = {}
  cameFrom[start] = None
  mindist = None
  for node in nodesList:
    if mindist == None or dist(start, node) < mindist:
      mindist = dist(start,node)
      minnode = node
  cameFrom = aStarSearch(graph, start, minnode, cameFrom)
  nodesList.remove(minnode)
  pathNew = reconstructPath(cameFrom, minnode)
  pathNew.pop()
  pathNew.reverse()
  path.extend(pathNew)
  return planPathRecurse(minnode, nodesList, graph, path)

def reconstructPath(cameFrom, end):
  path = []
  while not end == None:
    path.append(end)
    end = cameFrom[end]
  return path

def planPath(start, goodNodes, badNodes, x, y):
  graph = initGraph(x, y)
  graph = removeNodes(badNodes, graph)
  return planPathRecurse(start, goodNodes, graph, [start])
