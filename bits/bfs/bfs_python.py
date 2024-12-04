graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

def bfs_python(initial, target, graph):
    visited = []
    queued = []

    queued.append(initial)
    visited.append(initial)

    while (queued):
        m = queued.pop(0)
        print(m, end= " ")

        for neighbhor in graph[m]:
            if neighbhor not in visited:
                
                visited.append(neighbhor)
                queued.append(neighbhor)

bfs_python('5', 'jon snow', graph)
        

        
