import time

def play_again():
    # Asks if user wants to play again
    print('\nDo you want to play again? (yes or no)')
    return input('>').lower().startswith('y')

def secret():
    # Displays scene for pushing secret button
    print('You push the button...')
    time.sleep(1)
    print('...')
    time.sleep(2)
    print('You can hear mechanical clicking sounds emanating from somewhere behind the walls of the room...')
    time.sleep(2)
    print('...')
    time.sleep(2)
    print('A section of the east wall of the library pulls forward and moves to the side, revealing an opening to another room!')
    time.sleep(3)

def game():
    global current_room
    global inventory
    global directions
    global game_playing
    global rm_open
    # display current location
    print()
    print('You are in {}.'.format(current_room['name']))
    print(current_room['text'])
    # get user input
    command = input('\n> ').strip()
    # movement
    if command in directions:
        if command in current_room:
            current_room = rooms[current_room[command]]
        else:
            print("You can't go that way.")
    # quit game
    elif command.lower() in ('q', 'quit'):
        game_playing = False
    # take objects
    elif command.lower().split()[0] == 'take':
        item = command.lower().split()[1]
        if item in current_room['contents']:
            print('You take the ' + item)
            current_room['contents'].remove(item)
            inventory.append(item)
        else:
            print("I don't see that here.")
    # look at objects
    elif command.lower().split()[0] == 'inspect':
        thing = command.lower().split()[1]
        if thing in current_room['things']:
            print('You inspect the ' + thing)
            print(current_room['thing_text'])
            if current_room == rooms['library']:
                if 'note' in inventory:
                    print('remembering what you read in the note, you inspect the back panel of the bookshelf behind the dust free book,\nyou find a small black button sticking out of it.')
            if current_room == rooms['prison']:
                if 'note' not in inventory:
                    print("You can see a rolled up note in the skeleton's clenched hand")
        else:
            print("I don't see that here.")
    elif "look behind book" in command:
        if current_room == rooms['library']:
            if 'note' in inventory:
                print('You inspect the back panel of the bookshelf behind the dust free book,\nyou find a small black button sticking out of it.')
    # press secret button
    elif 'push button' in command.lower():
        if current_room == rooms['library']:
            if not rm_open:
                    secret()
                    rm_open = True
                    current_room['text'] += ' There is an opening to the east'
            else:
                print('You already did that.')
        else:
            print("You can't push that")
    # read things
    elif command.lower().split()[0] == 'read':
        if command.lower().split()[1] == 'note':
            if 'note' in inventory:
                print('The note reads:\nThe knowledge you can find in books is a valuable treasure,'
                  '\nbut to look behind the books can provide riches beyond measure.')
            else:
                print("You don't have a note to read")
        elif command.lower().split()[1] == 'book':
            if 'book' in inventory:
                print("You find that every page in the book is blank")
            else:
                print("You don't have a book")
        elif command.lower().split()[1] == 'sign':
            if current_room == rooms['starting']:
                print('Welcome to Text Game 2.2!\nPossible commands are:\nnorth    south\neast     west'
                      '\ntake     open\npush     read\ninspect  quit')
            else:
                print('What sign?')
        else:
            print("You can't read that")
    # open treasure chest or secret box
    elif command.lower().split()[0] == 'open':
        if command.lower().split()[1] == 'chest':
            if current_room == rooms['treasure room']:
                if 'key' in inventory:
                    print('You open the chest with the key and claim all of the loot for yourself!')
                    print('Congratulations you have won the game!')
                    game_playing = False
                else:
                    print('You attempt to open the chest but it is locked.')
        elif command.lower().split()[1] == 'box':
            if current_room == rooms['secret room']:
                if 'key' in inventory:
                    print('The box is empty')
                else:
                    print('You open the box and see a key inside of it.')
            else:
                print("what box?")
        else:
            print("There's nothing here for you to open")
    else:
        print("I don't understand that command.")

while True:
    rooms = {'starting': {'name': 'a small room', 'east': 'library', 'north': 'statue room',
                        'text': "The room is mostly empty, apart from a sign nailed to a post in the middle of the room. \nYou can see a door to the east, and a door to the north.",
                        'things': ['sign'],
                        'thing_text': "It's a sign, maybe you should read it?",
                        'contents': []},
             'statue room': {'name': 'a great hall filled with statues', 'east': 'prison', 'south': 'starting',
                             'north': 'treasure room',
                             'text': 'There are two lines of marble statues leading up either side of a walkway that streches through the middle of the room. '
                                     '\nThere are doors to other rooms on the east, north, and the south sides of the hall.',
                             'things': ['statues', 'statue'],
                             'thing_text': "You notice that all of the statues depict the same faceless figure. There's something .... eerie about them.",
                             'contents': []},
             'prison': {'name': 'a dungeon room', 'west': 'statue room', 'south': 'library',
                        'text': 'The room holds a prison cell. The rusted, iron-barred cell door is open ajar, with a human skeleton lying on the straw covered floor inside.'
                                '\nThere is a door to the west, and a door to the south.',
                        'things': ['skeleton'],
                        'thing_text': "Ewwww, it's all dead and stuff",
                        'contents': ['note']},
             'library': {'name': 'a library', 'north': 'prison', 'west': 'starting', 'east': 'secret room',
                         'text': 'The walls are lined with bookshelves reaching to the ceiling of the room.'
                                 '\nThere is a door to the north, and a door to the west.',
                         'things': ['bookshelf', 'bookshelves', 'books', 'book'],
                         'thing_text': "all of the books except for one are covered in a visible layer of dust.",
                         'contents': ['book']},
             'secret room': {'name': 'a small room with stone walls', 'west': 'library',
                             'text': 'In the center of the room sits a pedestal with a small wooden box placed on top of it.'
                                     '\nThe opening to the library is on the west side of the room',
                             'things': ['box', 'small wooden box', 'wooden box'],
                             'thing_text': 'It is a box ... maybe you should open it?',
                             'contents': ['key']},
             'treasure room': {'name': 'a small torchlit room', 'south': 'statue room',
                               'text': 'There is a large chest sitting in the middle of the room.\nThere is a door to the south of the room.',
                               'things': ['chest', 'treasure chest'],
                               'thing_text': "The chest is made of wood with ornate golden trim. It's quite large. It would be too heavy to carry out of here yourself, you'll have to find a way to open it.",
                               'contents': []}}

    directions = ['north', 'south', 'east', 'west']
    inventory = []
    current_room = rooms['starting']
    game_playing = True
    rm_open = False

    while game_playing:
        game()
    if not play_again():
        break


