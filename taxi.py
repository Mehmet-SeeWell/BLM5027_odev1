import numpy as np
import random as rnd
from map_generator import Taximap

class Taxi:

    posx, posy = -1, -1 ### 36
    action = -1 ### 0: Go left, 1: Go right, 2: Go up, 3: Go down + 4: Pick up + 5: Drop off
    passenger_state = -1 ### 0-4: Destinations + 5: Inside the Taxi
    destination_position = -1 ### 5
    reward = 0

    # Hyperparameters
    learning_rate = 0.1
    discount_factor = 0.95
    epsilon = 0.95

    num_of_states = 0
    num_of_actions = 6
    q_table = np.zeros([num_of_states, num_of_actions])
    
    def initialize_environment(map_size_x, map_size_y, destination_amount, reset_q_table = False):
        Taximap.generate_map(map_size_x, map_size_y, destination_amount)

        if reset_q_table:
            Taxi.num_of_states = map_size_x*map_size_y*(destination_amount+1)*destination_amount ### Taxi positions * passenger states * destination positions
            Taxi.q_table = np.zeros([Taxi.num_of_states, Taxi.num_of_actions])

    def random_start():
        Taxi.posx, Taxi.posy = rnd.randrange(len(Taximap.map[0])), rnd.randrange(len(Taximap.map))
        Taxi.passenger_state, Taxi.destination_position = rnd.sample(range(0, len(Taximap.destinations)), 2)
        Taxi.reward = 0

    def get_current_state():
        state = ((Taxi.posy * len(Taximap.map[0]) + Taxi.posx) * (len(Taximap.destinations) + 1) + Taxi.passenger_state) * len(Taximap.destinations) + Taxi.destination_position

        return state
    
    def update_q_table(old_state, old_value, next_value, reward):
        Taxi.q_table[old_state, Taxi.action] = (1 - Taxi.learning_rate) * old_value + Taxi.learning_rate * (reward + Taxi.discount_factor * next_value)

    def step():
        old_state = Taxi.get_current_state()

        if rnd.uniform(0, 1) < Taxi.epsilon:
            Taxi.action = rnd.randrange(6)
        else:
            Taxi.action = np.argmax(Taxi.q_table[old_state])

        reward = Taxi.act()
        Taxi.reward += reward

        terminated = (reward == 20)

        if terminated:
            next_value = 0
        else:
            next_value = np.max(Taxi.q_table[Taxi.get_current_state()])

        Taxi.update_q_table(
            old_state=old_state,
            old_value=Taxi.q_table[old_state, Taxi.action],
            next_value=next_value,
            reward=reward
        )

        return terminated
    

    def step():
        old_state = Taxi.get_current_state()
        if rnd.uniform(0, 1) < Taxi.epsilon:
            Taxi.action = rnd.randrange(6) # Explore
        else:
            Taxi.action = np.argmax(Taxi.q_table[old_state]) # Exploit

        reward = Taxi.act()

        Taxi.reward += reward

        terminated = (reward == 20)

        if terminated:
            next_value =  0
        else:
            next_value = np.max(Taxi.q_table[Taxi.get_current_state()])
        
        Taxi.update_q_table(
                            old_state = old_state,
                            old_value = Taxi.q_table[old_state, Taxi.action], 
                            next_value = next_value,
                            reward = reward
                            )
        
        return terminated
        

    def act():
        actions = [Taxi.move_left, Taxi.move_right, Taxi.move_up, Taxi.move_down, Taxi.pick_up, Taxi.drop_off]
        return actions[Taxi.action]()

    def move_left():
        if Taxi.posx > 0:
            Taxi.posx -= 1

        return -1

    def move_right():
        if Taxi.posx < len(Taximap.map[0])-1:
            Taxi.posx += 1

        return -1

    def move_up():
        if Taxi.posy > 0:
            Taxi.posy -= 1

        return -1

    def move_down():
        if Taxi.posy < len(Taximap.map)-1:
            Taxi.posy += 1

        return -1
        
    def pick_up():
        if Taxi.passenger_state < len(Taximap.destinations) and (Taxi.posx, Taxi.posy) in Taximap.destinations and Taximap.destinations[(Taxi.posx, Taxi.posy)] == Taxi.passenger_state:
            # Taximap.map[Taxi.posy][Taxi.posx] = f"{Taximap.destinations[(Taxi.posx, Taxi.posy)]+1} " ### Remove the passenger from the map
            Taxi.passenger_state = len(Taximap.destinations) ### Place the passenger inside of the taxi
            return -1 ### Passenger picked up
        else:
            return -10 ### Illegal "pick up"

    def drop_off():
        if Taxi.passenger_state == len(Taximap.destinations) and (Taxi.posx, Taxi.posy) in Taximap.destinations:
            # Taximap.map[Taxi.posy][Taxi.posx] = f"{Taximap.map[Taxi.posy][Taxi.posx][0]}P" ### Add the passenger to the map     
            Taxi.passenger_state = Taximap.destinations[(Taxi.posx, Taxi.posy)] ### Place the passenger to the current position       
            if Taxi.passenger_state == Taxi.destination_position:
                return 20 ### Correct destination
            else:
                return -1 ### Incorrect destination
        else:
            return -10 ### Illegal "drop off"

    def render_map():
        # [print(x) for x in Taximap.map]
        print("x"+("-"*((len(Taximap.map[0])*2)+1))+"x") ### Top Wall
        
        for rn, row in enumerate(Taximap.map):
            render = []
            for cn, col in enumerate(row):
                plot = ""
                current_pos = (cn, rn)

                if current_pos == (Taxi.posx, Taxi.posy):
                    plot += "T"
                elif current_pos in Taximap.destinations:
                    plot += str(Taximap.destinations[current_pos])
                else:
                    plot = ":"

                if (
                    Taxi.passenger_state < len(Taximap.destinations)
                    and current_pos in Taximap.destinations
                    and Taximap.destinations[current_pos] == Taxi.passenger_state
                ):
                    plot += "p"
                elif (
                    current_pos in Taximap.destinations
                    and Taximap.destinations[current_pos] == Taxi.destination_position
                ):
                    plot += "d"
                else:
                    plot += " "
                    
                render.append(plot)

            print("| " + ''.join(render) + "|")

        print("x"+("-"*((len(Taximap.map[0])*2)+1))+"x") ### Bottom Wall