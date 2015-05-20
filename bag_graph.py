import bag_engine

'''Generate .dot graph file. Format

digraph G {
  1 [label = "room name #1"];
  2 [label = "room name #2"];
  1 -> 2 [label = "door going from room 1 to room 2"];
}
'''

def create_graph(graph):

    room_num = 1
    room_name_to_number = {}
    for room in graph.keys():
        room_name_to_number[room] = room_num
        room_num += 1

    result = []
    for room in graph.keys():
        # output the room node
        room_number = room_name_to_number[room]
        result.append("  " + str(room_number) + ' [label = "' + room + '"];')

    for room in graph.keys():
        room_number = room_name_to_number[room]

        doors = graph[room]["doors"]
        for door in doors.keys():
            next_room = doors[door]
            next_room_number = room_name_to_number[next_room]
            result.append("  " + str(room_number) + " -> " + str(next_room_number) + ' [label = "' + door + '"];')

    return result


graph = create_graph(bag_engine.g_rooms)

output = open("bag_graph.dot", "w")
output.write("digraph G {" + "\n")
output.writelines("\n".join(graph))
output.writelines("\n}\n")
output.close()
