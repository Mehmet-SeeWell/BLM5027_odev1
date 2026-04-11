import random as rnd

class Taximap():

    map = []
    destinations = {}

    def generate_map(map_x_size, map_y_size, number_of_destinations):
        Taximap.map = []
        Taximap.destinations = {}

        ### Blank Map
        for _ in range(map_y_size):
            Taximap.map.append([])
            for _ in range(map_x_size):
                Taximap.map[-1].append(": ")

        ### Destinations
        total_spaces = ((map_y_size-2) + map_x_size)*2 ### Only the border tiles
        destinations = rnd.sample(range(0,total_spaces), number_of_destinations)
        for dest_num, location in enumerate(destinations):
            if location < map_x_size: ### Top Row
                locy = 0
                locx = location
            elif total_spaces - map_x_size < location: ### Bottom Row
                locy = map_y_size-1
                locx = location - (total_spaces-map_x_size)
            else:   # The Rest
                locy = ((location - map_x_size)//2) + 1
                locx = (location - map_x_size)%2 * (map_x_size-1)

            Taximap.map[locy][locx] = str(dest_num+1) + " "
            Taximap.destinations[(locx, locy)] = dest_num
        
        # total_spaces = map_y_size*map_x_size
        # destinations = rnd.sample(range(0,total_spaces), self.destination_amount)
        # for dest_num, location in enumerate(destinations):
        #     locx, locy = location//6, location%6 ### X and Y coordinates of the destination
        #     self.map[locy][locx] = str(dest_num+1) + " "

    def render_blank_map():
        # [print(x) for x in Taximap.map]
        print("x"+("-"*((len(Taximap.map[0])*2)+1))+"x") ### Top Wall
        for row in Taximap.map:
            print("| " + ''.join(row) + "|")
        print("x"+("-"*((len(Taximap.map[0])*2)+1))+"x") ### Bottom Wall