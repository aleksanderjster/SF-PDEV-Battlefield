## ======================================================================
## 1. Playing on  battlefield with size 6x6 cells
## 2. Player vs PC. PC do random guess. Field which
##    had been used are not accepted
## 3. Ship on the field represented by class Ship(position on the field)
## 4. Field class describes position of the ships.
## 5. Cells of the field represented by follow legend:
##    ■ - ship fiels on players side 
##    О - Untouched cell 
##    X - Hit cell of the ship
##    T - Miss cell of the field
## 6. Each participant of the game has:
##    1 of 3x ■ ship
##    2 of 2x ■ ship
##    4 of 1x ■ ship
##    - It should be 1 empty field in between neighbour ships.
## 7. Player can't hit the same cell twice. It should appear an exclusion.
## 8. It should appear exclution in case of unexpected reactions.
## =======================================================================
##   A B
##  ┌─┬─┐
## 1│■│X│
##  ├─┼─┤
## 2│О│T│
##  └─┴─┘
## =======================================================================
## Class Cell() - keep state of cell on Battlefield
## =======================================================================

import random

class Cell():

    def __init__(self, address):
        self._address = address     # Keep cell address in form 'A3' 
        self._hit = False           # State. Was cell hit?
        self._locked = False        # State. Is it available for ship placement?
        self._isShip = False        # State. Is cell under the ship
        self._sign = 'О'            # Printing sign by default

    @property                       
    def address(self):
        return self._address
    
    @property
    def hit(self):
        return self._hit
    
    @hit.setter
    def hit(self, value):
        self._hit = value
        if self._hit and self._isShip:
            self._sign = 'X'
        else:
            self._sign = 'T'
    
    @property
    def locked(self):
        return self._locked
    @locked.setter
    def locked(self, value):
        self._locked = value

    @property
    def sign(self):
        return self._sign
    @sign.setter
    def sign(self, sign):
        self._sign = sign

    @property
    def isShip(self):
        return self._isShip
    @isShip.setter
    def isShip(self, value):
        self._isShip = value

    @property
    def row(self):
        return int(self._address[1:]) - 1

    @property
    def column(self):
        ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ALFABET.find(self._address[0])

    def reset(self):
        self._locked = False        # State. Is it available for ship placement?
        self._isShip = False        # State. Is cell under the ship
        self._sign = 'О'            # Printing sign by default
        

## =======================================================================
## Class Ship() - Represent ship state on the Battlefield
## =======================================================================

class Ship(Cell):
    
    def __init__(self, *, address='A1', size=1, field):
        self._origin = field.getCell(address)
        self._field = field
        self._size = size

    @property
    def origin(self):
        return self._origin.address

    @origin.setter
    def origin(self, address):
        self._origin = field.getCell(address)

    def isValid(self):

        # checking if ship does not exceed the field.
        isEnoughSpace = False
        isAvailable = False
        if self._origin.column + self._size - 1 < self._field.SIZE:
            isEnoughSpace = True
        else:
            return False

        # checking that cells under ship are not locked for ship
        for col in range(self._size):
            ship_cell = self._field.getField[self._origin.row][self._origin.column + col]
            if ship_cell._locked:                
                isAvailable = False
                break
            else:
                isAvailable = True
        return isEnoughSpace and isAvailable

    @property
    def locked_area(self):
        #defining locked area
        locked_start_row = self._origin.row - 1
        locked_start_column = self._origin.column - 1
        locked_end_row = locked_start_row + 2
        locked_end_column = locked_start_column + self._size + 1

        #triming locked area
        if locked_start_row < 0: locked_start_row = 0
        if locked_start_column < 0: locked_start_column = 0
        if locked_end_row >= self._field.size: locked_end_row = self._field.size - 1
        if locked_end_column >= self._field.size: locked_end_column = self._field.size - 1
        return [
            [locked_start_row, locked_start_column],
            [locked_end_row, locked_end_column]
            ]
    
    def lock_area(self, area):
        for row  in range(area[0][0], area[1][0]+1):
            for column in range(area[0][1], area[1][1]+1):
                locked_cell = self._field.getField[row][column]
                locked_cell.locked = True

    # all ships arranged in horizontal position only    
    def launch(self):
        for col in range(self._size):            
            ship_cell = self._field.getField[self._origin.row][self._origin.column + col]
            ship_cell._isShip = True                # Mark cell as ship
            # ship_cell.locked = True                 # Mark cell is not vacant for otherships
            if self._field.visible:
                ship_cell._sign = '■'               # Represent cell for player side
            else:
                ship_cell._sign = 'О'         # Represent cell for PC side
                
        self.lock_area(self.locked_area)

            

## =======================================================================
## Class Battlefield() - keeping and operate with Cells collection.
## =======================================================================

class Battlefield():
    ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    SIZE = 6                        # max size 26    
    SHIP_TYPES = [3,
                 2, 2,
                 1, 1, 1, 1,]                 # Ship types in the game



    def __init__(self, *, visible=True):
        self.field = []
        self.visible = visible
        
        for row in range(self.SIZE):
            field_row = []
            for col in range(self.SIZE):
                cell_address = f'{self.ALFABET[col]}{row+1}'    # creates cell address in form 'A2'
                field_row.append(Cell(cell_address))            # construct row of cells
            self.field.append(field_row)                        # construct field from rows

    def getCell(self, address):
        row = int(address[1:]) - 1
        col = self.ALFABET.find(address[0])
        return self.field[row][col]

    @property
    def getField(self):
        return self.field

    @property
    def size(self):
        return self.SIZE

    @property
    def ship_type_list(self):
        return self.SHIP_TYPES

    def addressIsValid(self, *, address):
        try:
            if self.ALFABET[:self.SIZE].find(address[0].upper()) < 0: return False      # first symbol is not valid letter
            if (address[1:]).isnumeric():
                if int(address[1:]) - 1 < self.SIZE:
                    return True
        except:
            return False
        else:
            return False
        
    def reset(self):
        for row in self.field:
            for cell in row:
                cell.reset()
                

## =======================================================================
## Class Game() - keeping and operate with game actions.
## =======================================================================
class Game():
    
    def __init__(self):
        self._player = Battlefield(visible=True)
        self._pc = Battlefield(visible=False)

    @property
    def player(self):
        return self._player

    @property
    def pc(self):
        return self._pc

    @property
    def size(self):
        return self._player.size

        
    def print(self):
        player = self._player.getField
        pc = self._pc.getField

        ## constructing immutable parts of the printed table
        
        ## most left part of the table
        table_title = '   '
        table_upper_line = '  ┌'
        table_separator = '  ├'
        table_lower_line = '  └'

        ## constructig parts in between the ends
        for col in range(self.size - 1):
            table_title += f'{self.player.ALFABET[col]} '
            table_upper_line += '─┬'
            table_separator += '─┼'
            table_lower_line += '─┴'

        ##most right part of the table
        table_title += f'{self.player.ALFABET[self.size-1]} '
        table_upper_line += '─┐'
        table_separator += '─┤'
        table_lower_line += '─┘'

        ## printing tables of player and PC
        print(f'{table_title}    {table_title}')
        print(f'{table_upper_line}    {table_upper_line}')

        for row in range(self.size):
            table_row_1 = f'{row+1:2d}│'
            table_row_2 = table_row_1
            
            for col in range(self.size):

                # there to be checked state of the cell of the field
                # to decide what kind of sign to print in the row

                table_row_1 += f'{player[row][col].sign}│'
                table_row_2 += f'{pc[row][col].sign}│'

            print(f'{table_row_1}    {table_row_2}')

            if row < self.size - 1:
                print(f'{table_separator}    {table_separator}')

        print(f'{table_lower_line}    {table_lower_line}')


##
##
##



## =======================================================================
## game engine functions - act with game actions.
## =======================================================================

def get_vacant_cells(field, criteria):
    vacant_cells = []
    for field_row in field.getField:
        for cell in field_row:
            if criteria == 'hit':
                if cell.hit == False: vacant_cells.append(cell.address)
            if criteria == 'locked':
                if cell.locked == False: vacant_cells.append(cell.address)
    return vacant_cells

    
## =======================================================================
def pc_ships_arrangement(pc):

    ship_types = pc.ship_type_list
    
    try:        # Attempting to auto arrange pc's ships

        # filling ships on pc side in random manner
        for ship_type in ship_types:       
            
            vacant_cells = get_vacant_cells(pc, 'locked')       # getting not locked cells 
            
            i = 0  # trigger for exit with unable ship placement            
            while True:
                i += 1
                
                try:
                    candidate_cell = vacant_cells[random.randint(0, len(vacant_cells)-1)]
                except:
                    print(f'ERROR: Arrangement failed! Trying again')
                    pc.reset()
                    return False

                if pc.addressIsValid(address=candidate_cell):
                    if Ship(address=candidate_cell, size=ship_type, field=pc).isValid():
                        Ship(address=candidate_cell, size=ship_type, field=pc).launch()
                        break

                if i > 100:
                    print(f'ERROR: Auto-arrangement failed! Trying again')
                    return False
    except:
        print(f'ERROR: Auto ship arrangement failed! Start game again')
        return False

    return True


## =======================================================================
def player_ships_arrangement(player, game):
    
    # filling players field with ships
    game.print()
    for ship_type in player.ship_type_list:
        
        while True: # input address for ship until it is correct and ship can be placed
            
            candidate_cell = input(f'Give start point for {ship_type}-deck/s ship: ').upper()
            try:
                if player.addressIsValid(address=candidate_cell):
                    if Ship(address=candidate_cell, size=ship_type, field=player).isValid():
                        Ship(address=candidate_cell, size=ship_type, field=player).launch()
                        game.print()
                        break
                    else:
                        print(f'Ship can not be places at {candidate_cell}! Give another address.')
                else:
                    print(f'Address is not valid! Check address and try again.')
            except:
                return False
    return True


## =======================================================================
def player_hit(field):
    address_to_hit = input(f'Enter cell address to hit: ').upper()
    if not field.addressIsValid(address=address_to_hit): return # validate address is correct
    if field.getCell(address_to_hit).hit: return                # validate address not hit before
    return address_to_hit


## =======================================================================
def pc_hit(field):
    vacant_cells = get_vacant_cells(field, 'hit') # getting not hit cells
    address_to_hit = vacant_cells[random.randint(0, len(vacant_cells)-1)]
    return address_to_hit
    

## =======================================================================    
def main():
    game = Game()
    
    player = game.player
    pc = game.pc
    
    i = 0
    while True:
        i += 1
        result = pc_ships_arrangement(pc)
        if result: break
        if i > 10:
            print(f'Game start failed!')
            return

    while True:            
        result = player_ships_arrangement(player, game)
        if result: break
        player = game.player
            

                    
    print(f'\nShips are arranged successfully! Game started!\n')

    game.print()
    
    ship_types = player.ship_type_list
    player_ships = sum(ship_types)
    pc_ships = player_ships

    my_turn = True                                           # player's switch

    while player_ships > 0 and pc_ships > 0:                # game continious until someone's ships are over

        if my_turn:
            while True:                                     # request input until it is valid
                address_to_hit = player_hit(pc)
                
                if address_to_hit:                    
                    pc.getCell(address_to_hit).hit = True   # mark cell as 'X'                                             

                    if  pc.getCell(address_to_hit).isShip:
                        pc_ships -= 1                           # countdown ships number
                        game.print()
                        print(f'\n=================================')
                        print(f'>>> You hit opponent ship at {address_to_hit}')
                        print(f'=================================\n')
                        if pc_ships == 0: break
                    else:
                        print(f'\n=================================')
                        print(f'You miss at {address_to_hit}')
                        print(f'=================================\n')
                        my_turn = False                          # give control to pc
                        break
                else:
                    print('Address is not correct or had been hit!')
                    
                    
        else:
            while True:
                address_to_hit = pc_hit(player)
                if address_to_hit:
                    player.getCell(address_to_hit).hit = True
                    if player.getCell(address_to_hit).isShip:
                        player_ships -= 1
                        game.print()
                        print(f'\n=================================')
                        print(f'>>> PC hit your ship at {address_to_hit}')
                        print(f'=================================\n')
                    else:
                        print(f'\n=================================')
                        print(f'PC miss at {address_to_hit}')
                        print(f'=================================\n')
                        my_turn = True
                        break
        
        game.print()

    if pc_ships == 0: print(f'Congratulations! You win!')
    if player_ships == 0: print(f'You loose! Take a revenge!')


## =======================================================================            
if __name__ == '__main__':
    main()














