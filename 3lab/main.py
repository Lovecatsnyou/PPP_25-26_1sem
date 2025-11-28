def find_shortest_path(graph, start, end):
    
    def dfs(current, target, visited, path, distance):
        # достигли конца
        if current == target:
            return (path, distance)
        
        best_result = None
        
        # проходим соседей
        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dfs(neighbor, target, visited, path + [neighbor], distance + weight)
                visited.remove(neighbor)
                
                # Запоминаем лучший путь (с минимальным расстоянием)
                if result:
                    if best_result is None or result[1] < best_result[1]:
                        best_result = result
        
        return best_result
    
    visited = {start}
    return dfs(start, end, visited, [start], 0)

if __name__ == "__main__":
    # Граф из таблицы смежности, можно менять
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('D', 5)],
        'C': [('A', 2), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)]
    }
    
    # Поиск пути, тоже можно менять, в данном случае от A до E.
    result = find_shortest_path(graph, 'A', 'E')
    
    if result:
        path, distance = result
        print(f"Путь: {' => '.join(path)}")
        print(f"Расстояние: {distance}")
    else:
        print("Пути не найдено")
