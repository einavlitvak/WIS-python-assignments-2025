import random

##Ship size
Ship1_size=3
Ship2_size=2
Ship3_size=2
Ship4_size=4
##Intitial position 
Ship1_head={'x': random.randint(0,9), 'y': random.randint(0,9)}
Ship2_head={'x': random.randint(0,9), 'y': random.randint(0,9)}
Ship3_head={'x': random.randint(0,9), 'y': random.randint(0,9)}
Ship4_head={'x': random.randint(0,9), 'y': random.randint(0,9)}
##Ship orientation
#vertical=0
#horizontal=1
ship1_orientation= random.randint(0,1)
ship2_orientation= random.randint(0,1)
ship3_orientation= random.randint(0,1)
ship4_orientation= random.randint(0,1)

#ships
ships = {
    'ship1': {'num':1, 'head_pos':Ship1_head, 'orientation':ship1_orientation, 'size': Ship1_size},
    'ship2': {'num':2, 'head_pos':Ship2_head, 'orientation':ship2_orientation, 'size': Ship2_size},
    'ship3': {'num':3, 'head_pos':Ship3_head, 'orientation':ship3_orientation, 'size': Ship3_size},
    'ship4': {'num':4, 'head_pos':Ship4_head, 'orientation':ship4_orientation, 'size': Ship4_size}}

##field array of ceros 10x10
battle_field = [[0 for i in range(15)] for j in range(15)]

for ship in ships:      
    if ships[ship]['orientation'] == 0:
        for i in range(ships[ship]['size']):
            battle_field[ships[ship]['head_pos']['x']][ships[ship]['head_pos']['y']+i] = ships[ship]['num'] 
    elif ships[ship]['orientation'] == 1:
        for i in range(ships[ship]['size']):
            battle_field[ships[ship]['head_pos']['x']+i][ships[ship]['head_pos']['y']] = ships[ship]['num'] 

print(battle_field)

game_over= False

while not game_over
    
    if all_ship_sunk:
        print('Battle over!')
        game_over = True
