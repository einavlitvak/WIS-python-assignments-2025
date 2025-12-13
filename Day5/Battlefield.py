import random

##field array of ceros 10x10
battle_field_size=5
battle_field = [[0 for i in range(battle_field_size)] for j in range(battle_field_size)]
battle_field_player = [['❔' for i in range(battle_field_size)] for j in range(battle_field_size)]


##number of ships
number_of_ships= 4
ships = {}
for num_ship in range(number_of_ships):
    are_coord_free= False
    while not are_coord_free:
        are_coord_free = True 
        ##Ship size
        ship_size=random.randint(1,2)
        ##Intitial position 
        ship_head={'x': random.randint(0,battle_field_size - 1), 'y': random.randint(0,battle_field_size - 1)}
        ##Ship orientation: vertical=0; horizontal=1
        ship_orientation= random.randint(0,1) 
        if battle_field[ship_head['x']][ship_head['y']] == 0:
            if ship_orientation == 0:
                for ship_body in range(1,ship_size): 
                    if battle_field[ship_head['x']][ship_head['y']+ship_body] != 0:
                        are_coords_free= False
                        break
            else:
                for ship_body in range(1,ship_size): 
                    if battle_field[ship_head['x']+ship_body][ship_head['y']] != 0:
                        are_coords_free= False
                        break
        else: are_coords_free= False
    for space in range(ship_size):
        if ship_orientation == 0:
            battle_field[ship_head['x']][ship_head['y']+space] = num_ship+1
        else:
            battle_field[ship_head['x']+space][ship_head['y']] = num_ship+1
    ships[f'ship{num_ship+1}']= {
        'num': num_ship+1,
        'size': ship_size, 
        'head_pos': ship_head, 
        'orientation': ship_orientation}
        
game_over= False

for row in battle_field_player:
    print(row)

print('Good luck sinking my ships...')
while not game_over:
    # for row in battle_field:
    #     print(row)
    print('choose coordinates between 0 and 4')
    x_coordinate_str= input('Enter a field position for X:')
    y_coordinate_str= input('Enter a field position for Y:')
    x_coordinate=int(x_coordinate_str)
    if x_coordinate<0 or x_coordinate>4:
        print('wrong input! It must be a number between 0 and 4')
        continue
    y_coordinate=int(y_coordinate_str)
    if y_coordinate<0 or y_coordinate>4:
        print('wrong input! It must be a number between 0 and 4')
        continue

    ship_ID=[]
    if battle_field[x_coordinate][y_coordinate] > 0:
        print('Ship hit!')
        ship_ID.append(battle_field[x_coordinate][y_coordinate])
        battle_field[x_coordinate][y_coordinate] = battle_field[x_coordinate][y_coordinate] - len(ships) -1
        battle_field_player[x_coordinate][y_coordinate] = '💥'
        for row in battle_field_player:
            print(row)
    elif battle_field[x_coordinate][y_coordinate] < 0:
        print('Dont be greedy, ship site already hit! Try again...')
        for row in battle_field_player:
            print(row)
        continue
    else: 
        battle_field_player[x_coordinate][y_coordinate] = '🌊'
        print('Splash! Try again...')    
        for row in battle_field_player:
            print(row)
        continue 

    for ship in ships:  
        if len(ship_ID)>0 and ships[ship]['num'] == ship_ID[0]:
            ship_hits= []  
            is_ship_sunk = 0
            if ships[ship]['orientation'] == 0:  
                for i in range(ships[ship]['size']):
                    if battle_field[ships[ship]['head_pos']['x']][ships[ship]['head_pos']['y']+i] == battle_field[x_coordinate][y_coordinate]:
                        ship_hits.append(battle_field[ships[ship]['head_pos']['x']][ships[ship]['head_pos']['y']+i] )
            if ships[ship]['orientation'] == 1:
                for i in range(ships[ship]['size']):
                    if battle_field[ships[ship]['head_pos']['x']+i][ships[ship]['head_pos']['y']] == battle_field[x_coordinate][y_coordinate]:
                        ship_hits.append(battle_field[ships[ship]['head_pos']['x']+i][ships[ship]['head_pos']['y']] )
            for i in ship_hits:
                is_ship_sunk = is_ship_sunk + i
            if is_ship_sunk == battle_field[x_coordinate][y_coordinate] * ships[ship]['size']:
                print('Ship sunk!')
                for space in range(ships[ship]['size']):
                    if ships[ship]['orientation'] == 0:
                        battle_field_player[ships[ship]['head_pos']['x']][ships[ship]['head_pos']['y']+space] = '☠️'
                    else:
                        battle_field_player[ships[ship]['head_pos']['x']+space][ships[ship]['head_pos']['y']]= '☠️'
                for row in battle_field_player:
                    print(row)       
        else: continue

    all_ships_sunk = True
    for row in battle_field:
        for cell in row:
            if cell >0: 
                all_ships_sunk = False
                break       
 
    if all_ships_sunk:
        print('Battle over!')
        game_over = True

