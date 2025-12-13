import random

class BattleshipGame:
    def __init__(self, size=5, num_ships=4):
        self.battle_field_size = size
        self.battle_field = [[0 for i in range(size)] for j in range(size)]
        self.battle_field_player = [['❔' for i in range(size)] for j in range(size)]
        self.number_of_ships = num_ships
        self.ships = {}
        self._place_ships()
        self.game_over = False

    def _place_ships(self):
        # COPY-PASTE of original logic (adapted to use self.)
        for num_ship in range(self.number_of_ships):
            are_coord_free= False
            while not are_coord_free:
                are_coord_free = True 
                ##Ship size
                ship_size=random.randint(1,2)
                ##Intitial position 
                ship_head={'x': random.randint(0,self.battle_field_size - 1), 'y': random.randint(0,self.battle_field_size - 1)}
                ##Ship orientation: vertical=0; horizontal=1
                ship_orientation= random.randint(0,1) 
                
                # Original logic: directly accessing array, no boundary checks (might crash if lucky/unlucky)
                # To prevent crash within this wrapper during __init__ for the user, 
                # we technically need the try/except or just let it be. 
                # But since the original code didn't check boundaries, it relied on luck (or 5x5 is big enough for 1-2 size ships often).
                # However, original code had:
                # if battle_field[ship_head['x']][ship_head['y']] == 0:
                
                try: # Added try-except only to prevent 'IndexError' crashing the class init, mirroring how script would crash
                    if self.battle_field[ship_head['x']][ship_head['y']] == 0:
                        if ship_orientation == 0:
                            for ship_body in range(1,ship_size): 
                                if self.battle_field[ship_head['x']][ship_head['y']+ship_body] != 0:
                                    are_coords_free= False # Keeping the original typo (coords vs coord)
                                    break
                        else:
                            for ship_body in range(1,ship_size): 
                                if self.battle_field[ship_head['x']+ship_body][ship_head['y']] != 0:
                                    are_coords_free= False # Keeping the original typo
                                    break
                    else: are_coords_free= False # Keeping the original typo
                except IndexError:
                    # Original code would crash here. 
                    # For faithful reproduction, we proceed, but ship placement logic with the typo 
                    # actually means 'are_coord_free' stays True, so it places it anyway?
                    # wait, if are_coord_free stays True (because only are_coords_free was set to False), loop ends.
                    pass

                # Note: Because of the typo in original (are_coords_free vs are_coord_free), 
                # the loop 'while not are_coord_free' always sees True after first pass and breaks.
                # So collision checks were ignored in the original code. I will include this behavior.
            
            # Place ship
            # Original code didn't have boundary checks here either, risking IndexError on assignment
            try:
                for space in range(ship_size):
                    if ship_orientation == 0:
                        self.battle_field[ship_head['x']][ship_head['y']+space] = num_ship+1
                    else:
                        self.battle_field[ship_head['x']+space][ship_head['y']] = num_ship+1
            except IndexError:
                pass # Just ignore if it goes out of bounds, like a broken script might behave (or crash)

            self.ships[f'ship{num_ship+1}']= {
                'num': num_ship+1,
                'size': ship_size, 
                'head_pos': ship_head, 
                'orientation': ship_orientation}

    def process_guess(self, x_coordinate, y_coordinate):
        # Pure logic from the original while loop, extracted
        msg = ""
        ship_ID=[]
        
        # Original logic access
        if self.battle_field[x_coordinate][y_coordinate] > 0:
            msg = 'Ship hit!'
            ship_ID.append(self.battle_field[x_coordinate][y_coordinate])
            self.battle_field[x_coordinate][y_coordinate] = self.battle_field[x_coordinate][y_coordinate] - len(self.ships) -1
            self.battle_field_player[x_coordinate][y_coordinate] = '💥'
            # Original prints board here, we don't.

        elif self.battle_field[x_coordinate][y_coordinate] < 0:
            msg = 'Dont be greedy, ship site already hit! Try again...'
            # Original prints board here, we don't.
            return msg # The original uses 'continue', so we return early to simulate skipping the rest
        else: 
            self.battle_field_player[x_coordinate][y_coordinate] = '🌊'
            msg = 'Splash! Try again...'    
            # Original prints board here, we don't.
            return msg # Original uses 'continue'

        # Sinking Logic
        for ship in self.ships:  
            # Original: if len(ship_ID)>0 and ships[ship]['num'] == ship_ID[0]:
            if len(ship_ID)>0 and self.ships[ship]['num'] == ship_ID[0]:
                ship_hits= []  
                is_ship_sunk = 0
                if self.ships[ship]['orientation'] == 0:  
                    for i in range(self.ships[ship]['size']):
                        try:
                            # Original line 92
                            if self.battle_field[self.ships[ship]['head_pos']['x']][self.ships[ship]['head_pos']['y']+i] == self.battle_field[x_coordinate][y_coordinate]:
                                ship_hits.append(self.battle_field[self.ships[ship]['head_pos']['x']][self.ships[ship]['head_pos']['y']+i] )
                        except IndexError: pass
                if self.ships[ship]['orientation'] == 1:
                    for i in range(self.ships[ship]['size']):
                        try:
                            # Original line 96
                            if self.battle_field[self.ships[ship]['head_pos']['x']+i][self.ships[ship]['head_pos']['y']] == self.battle_field[x_coordinate][y_coordinate]:
                                ship_hits.append(self.battle_field[self.ships[ship]['head_pos']['x']+i][self.ships[ship]['head_pos']['y']] )
                        except IndexError: pass

                for i in ship_hits:
                    is_ship_sunk = is_ship_sunk + i
                
                # Original line 100
                if is_ship_sunk == self.battle_field[x_coordinate][y_coordinate] * self.ships[ship]['size']:
                    msg = 'Ship sunk!'  # It prints 'Ship sunk!', we assume this overrides 'Ship hit!'
                    for space in range(self.ships[ship]['size']):
                        if self.ships[ship]['orientation'] == 0:
                            self.battle_field_player[self.ships[ship]['head_pos']['x']][self.ships[ship]['head_pos']['y']+space] = '☠️'
                        else:
                            self.battle_field_player[self.ships[ship]['head_pos']['x']+space][self.ships[ship]['head_pos']['y']]= '☠️'
            else: continue
            
        return msg

    def is_game_over(self):
        all_ships_sunk = True
        for row in self.battle_field:
            for cell in row:
                if cell >0: 
                    all_ships_sunk = False
                    break       
        return all_ships_sunk
