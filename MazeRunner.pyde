import os, random

add_library('minim')
# for navigating to files like images and sounds in the game.
path = os.getcwd()
# resolution for game.
DISPLAY_WIDTH = 1400
DISPLAY_HEIGHT = 800
# instantiate minim, which handles sounds.
player = Minim(this)


# superclass for all other creatures and pickups
class Entity:
    def __init__(self, x, y, r, img, w, h):
        self.x = x  # x and y variables determine position of sprites
        self.y = y
        self.r = r  # r is radius, which helps with sprite collision
        self.w = w  # w and h are image width and height, which are used to scale down sprite images.
        self.h = h
        self.vx = 0  # vx and vy is velocity, which allows sprites to move if need be.
        self.vy = 0
        self.img = loadImage(path + "/images/" + img)  # loads images
        self.dir = RIGHT

    # primitive update and display functions for the superclass, more fleshed out in other classes if need be.
    def update(self):
        self.x += self.vx
        self.y += self.vy

    def display(self):
        self.update()
        image(self.img, self.x, self.y, self.w, self.h)


# the good sprites are any pickupables, such as the campus cat, apple, and energy. Picking these up will give you
# points, and if you pick all of them up and reach the torch, you win the game.
class GoodSprite(Entity):
    def __init__(self, x, y, r, img, w, h):
        Entity.__init__(self, x, y, r, img, w, h)
        
# the torch indicates the end of the maze. Will only win the game if all good sprites are gone.
class Torch(Entity):
    def __init__(self, x, y, r, img, w, h):
        Entity.__init__(self, x, y, r, img, w, h)

# the the class for Faiza the Falcon, our intrepid hero of the game and of NYUAD!
class Faiza(Entity):
    def __init__(self, x, y, r, img, w, h):
        Entity.__init__(self, x, y, r, img, w, h)
        self.inputHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}

    # input handler for movement, each arrow key moves faiza in a certain direction.      
    def update(self):
        # each if statement ensures Faiza will not go out of bounds or clip through the maze. it is explained further
        # below, but the maze is made up on 1s and 0s, 1 being a solid block, 0 being a space.
        # These will check to make sure Faiza will not go outside the 0s of the maze.
        if (80 <= self.x - 40 <= 1080) and (self.inputHandler[LEFT]) and game.grid[(self.y // 30) - 2][(self.x // 40) - 3] == 0:
            # Faiza also changes direction if moving left/right.
            self.dir = LEFT
            self.x -= 40
        elif (80 <= self.x + 40 <= 1080) and (self.inputHandler[RIGHT]) and game.grid[(self.y // 30) - 2][(self.x // 40) - 1] == 0:
            self.dir = RIGHT
            self.x += 40
        # up/down is separate from left/right, so that there are no issues with input/xy positions.
        if (60 <= self.y + 30 <= 750) and (self.inputHandler[DOWN]) and game.grid[(self.y // 30) - 1][(self.x // 40) - 2] == 0:
            self.y += 30
        elif (60 <= self.y - 30 <= 750) and (self.inputHandler[UP]) and game.grid[(self.y // 30) - 3][(self.x // 40) - 2] == 0:
            self.y -= 30

    # method to check the distance between two creatures.        
    def checkCollision(self, target):
        # just uses the distance formula to do so.
        return ((self.x - target.x) ** 2 + (self.y - target.y) ** 2) ** 0.5
    
    # method to check the distance between two creatures.        
    def checkCollisionGood(self, target):
        # just uses the distance formula to do so.
        return ((self.x - (target.x-10)) ** 2 + (self.y - (target.y-5)) ** 2) ** 0.5

    def display(self):
        self.update()
        if self.dir == RIGHT:
            image(self.img, self.x, self.y, self.w, self.h)
        elif self.dir == LEFT:
            # reflects Faiza's image over y axis when moving left.
            pushMatrix()
            scale(-1, 1)
            image(self.img, -self.x - self.w, self.y, self.w, self.h)
            popMatrix()


# the class for the evil sprites, such as covid-19, zoom, and phones.
class EvilSprite(Entity):
    def __init__(self, x, y, r, img, w, h):
        Entity.__init__(self, x, y, r, img, w, h)
        self.vx = 5
        self.vy = 5

    def update(self):
        # the evil sprite will move in a random direction around the maze.
        self.vx, self.vy = self.random_position()
        self.x = self.x + (self.vx * 40)
        self.y = self.y + (self.vy * 30)

    # the evil sprite will choose a random direction adjacent to it (as long as there is empty space),
    # move 1 tile over, and then repeats this algorithm.
    def random_position(self):
        neighbor_x = 0
        neighbor_y = 0
        run = True
        while run:
            rand_pos = random.choice([1, 2, 3, 4])
            if rand_pos == 1:
                neighbor_x, neighbor_y = 0, 1
            elif rand_pos == 2:
                neighbor_x, neighbor_y = 1, 0
            elif rand_pos == 3:
                neighbor_x, neighbor_y = 0, -1
            elif rand_pos == 4:
                neighbor_x, neighbor_y = -1, 0
            # will keep running the loop and choosing random directions until it chooses a space with no wall.
            if 0 <= (((self.y // 30) - 2) + neighbor_y) < len(game.grid) and 0 <= (((self.x // 40) - 2) + neighbor_x) < len(game.grid[0]) and \ game.grid[((self.y // 30) - 2) + neighbor_y][((self.x // 40) - 2) + neighbor_x] != 1:
                run = False
        return neighbor_x, neighbor_y


# The heart class simply displays the life of Faiza.
class Heart(Entity):
    def __init__(self, x, y, r, img, w, h):
        Entity.__init__(self, x, y, r, img, w, h)


# main function for most of the game.
class Game:
    def __init__(self, windowWidth, windowHeight):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        # load all sounds and music.
        self.start_game = player.loadFile(path + "/sounds/pacman_beginning.wav")
        self.eat_sprite = player.loadFile(path + "/sounds/pacman_eatfruit.wav")
        self.over = player.loadFile(path + "/sounds/pacman_death.wav")
        self.bg_music = player.loadFile(path + "/sounds/bg_sound.mp3")
        self.pacman_win = player.loadFile(path + "/sounds/pacman_win.mp3")
        self.game_over_img = loadImage(path + "/images/game_over.jpg")
        self.bg_music.loop()
        self.alive = True
        self.win = False
        # below is the instantiating of all objects.
        self.player = Faiza(520, 60, 30, "Faiza.png", 40, 30)
        self.torch = Torch(520, 720, 10, "torch.png", 40, 90)
        self.score = 0
        self.numevil = 3
        self.leaderboard = []
        # the primitive grid before the rectangles are added.
        # 1 represents a rectangle, 0 is empty space, and 2 is the torch.
        self.grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        # placing the good sprites:
        # the good sprites are placed in every free space.
        goodsprites_cords = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[c][r] == 0:
                    x_g = 80 + (r * 40)
                    y_g = 60 + (c * 30)
                    goodsprites_cords.append([x_g, y_g])
        self.goodsprite_list = []
        for cords in goodsprites_cords:
            self.goodsprite_list.append(
                GoodSprite(cords[0]+10, cords[1]+5, 10, "good" + str(random.randint(1, 3)) + ".png", 25, 20))
        
        # 10 evil sprites are placed in random parts of the map, as long as its an empty space.
        self.evil = []
        
        evil_pos_x = [(1 + 2) * 40, (4 + 2) * 40, (6 + 2) * 40, (11 + 2) * 40, (23 + 2) * 40, (1 + 2) * 40]
        evil_pos_y = [(5 + 2) * 30, (22 + 2) * 30, (21 + 2) * 30, (5 + 2) * 30, (22 + 2) * 30]
        for i in range(self.numevil):
            self.evil.append(EvilSprite(random.choice(evil_pos_x), random.choice(evil_pos_y), 30, "evil" + str(random.randint(1, 3)) + ".png", 40, 30))
            
        # placing the hearts:
        # Faiza has 5 life.
        self.lifesupply = []
        for i in range(5):
            self.lifesupply.append(Heart(1100 + (i * 50), 50, 0, "heart.png", 50, 50))
            
    def display(self):
        self.show_grid()
        # if the game is ongoing:
        if self.alive:
            self.show_score()
        # if you win the game:
        elif self.win:
            self.bg_music.pause()
            img = loadImage(path + '/images/' + 'background1.png')
            image(img, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            textFont(crackmanFont)
            textSize(50)
            textAlign(CENTER)
            fill(255)
            text("Congrats! You won the game!" + "\n" + "Click anywhere to restart!", 700, 300)
            self.pacman_win.play()
            textSize(30)
            text("SCORE: " + str(self.score * 10), 700, 500)
            return
        # if you lose the game
        else:
            img = loadImage(path + '/images/' + 'background1.png')
            image(img, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            textFont(crackmanFont)
            textSize(50)
            textAlign(CENTER)
            fill(255)
            text("GAME OVER!" + "\n" + "Click anywhere to restart!", 700, 300)
            self.over.play()
            textSize(30)
            text("SCORE: " + str(self.score * 10), 700, 500)
            self.bg_music.pause()
            return
        # display sprites
        self.torch.display()
        for heart in self.lifesupply:
            heart.display()
            
        for s in self.goodsprite_list:
            s.display()
        
        for e in self.evil:
            e.display()
        self.player.display()
        # if good sprite is touched by Faiza, remove it from the list. If the list is empty and you touch the torch, you win.
        for s in self.goodsprite_list:
            if self.player.checkCollisionGood(s) == 0:
                self.score += 1
                self.eat_sprite.rewind()
                self.eat_sprite.play()
                self.goodsprite_list.remove(s)
        # if Faiza touches an evil sprite, remove one heart. If all are gone, you lose the game.
        for e in self.evil:
            if self.player.checkCollision(e) <= 5:
                if len(self.lifesupply) == 0:
                    self.alive = False
                    return
                self.lifesupply.pop()
                self.eat_sprite.rewind()
                self.eat_sprite.play()
        # if no good sprites exist and torch is touched, you win.
        if self.goodsprite_list == [] and self.player.checkCollision(self.torch) <= self.player.r + self.torch.r:
            self.win = True
            self.alive = False
            
    def addsprites(self, n):
        evil_pos_x = [(1 + 2) * 40, (4 + 2) * 40, (6 + 2) * 40, (11 + 2) * 40, (23 + 2) * 40, (1 + 2) * 40]
        evil_pos_y = [(5 + 2) * 30, (22 + 2) * 30, (21 + 2) * 30, (5 + 2) * 30, (22 + 2) * 30]
        for i in range(n):
            self.evil.append(EvilSprite(random.choice(evil_pos_x), random.choice(evil_pos_y), 30, "evil" + str(random.randint(1, 3)) + ".png", 40, 30))
        
        
    # shows the game score.
    def show_score(self):
        if self.alive:
            textSize(20)
            textAlign(LEFT)
            fill(255)
            # score is calculated by number of good sprites taken, times 10.
            text("Score: " + str(self.score * 10) + " Falcon Dirhams", 1100, 200)

    # shows the grid with rectangles.
    # adds rectangle to each part of the grid with a 1.
    def show_grid(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[c][r] == 1:
                    fill(153, 0, 153)
                    rect(((r + 2) * 40), ((c + 2) * 30), 40, 30)

    # shows the leaderboard.                
    def leader_board_show(self):
        background(182, 40, 233)
        fill(255)
        textFont(crackmanFont)
        textSize(100)
        fill(255, 255, 255)
        # makes sure all scores in text file are formatted properly.
        with open("leaderboard.txt", "r") as reader:
            for l in reader:
                if not l.isspace():
                    if int(l.strip()) not in self.leaderboard:
                        self.leaderboard.append(int(l.strip()))
        cnt = 0
        self.leaderboard.sort(reverse=True)
        # ##-----LEADERBOARD-------##
        image(img, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        # TOP 5
        fill(255)
        textFont(crackmanFont)
        textSize(60)
        textAlign(CENTER)
        text("Top 5", 700, 150)
        textFont(crackmanFont)
        fill(255)
        textSize(40)
        # displays the leaderboard.
        for i in range(1, 6):
            n = "th"
            if i == 1:
                n = "st"
            elif i == 2:
                n = "nd"
            elif i == 3:
                n = "rd"
            else:
                n = "th"
            text(str(i) + n + " place: " + str(self.leaderboard[i - 1]) + " points", 700, 200 + (i * 100))
        # back button
        fill(255)
        textFont(crackmanFont)
        textAlign(CENTER)
        textSize(20)
        text("Game Menu", 70, 40)
        noFill()
        if (10 <= mouseX <= 140) and (10 <= mouseY <= 45):
            stroke(255)
            rect(10, 20, 120, 25)


# instantiate the game
game = Game(DISPLAY_WIDTH, DISPLAY_HEIGHT)

level = True
paused = False
soundOn = True

def setup():
    frameRate(10)
    global img, img2, crackmanFont, stage, pause_img, paused, soundOn
    # saves the scores to a file, and then displays the top 5 scores.
    with open("leaderboard.txt", "a") as writer:
        writer.write('')
    size(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    img = loadImage(path + '/images/' + 'background1.png')  # background for all parts of the game.
    img2 = loadImage(path + '/images/' + 'bigfaiza.png')  # larger Faiza that appears on the main menu.
    pause_img = loadImage(path + '/images/' + 'pause.png') # pause image
    crackmanFont = loadFont("Phosphate-Inline-48.vlw")  # our custom font
    stage = 1

def draw():
    global game, level, paused, soundOn
    # stage 1 is main menu.
    if stage == 1:
        background(0)
        fill(255)
        textFont(crackmanFont)
        textAlign(CENTER)
        image(img, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        image(img2, 100, 350, 300, 500)
        # game title
        textSize(60)
        text("Welcome To Maze-Runner: Falcon Edition", 700, 100)
        textSize(40)
        # menu buttons
        text("Start!", 700, 500)
        text("Leaderboard", 700, 560)
        text("Instructions", 700, 620)
        text("Exit", 700, 680)
        textSize(40)
        noFill()
        if (500 <= mouseX <= 900) and (460 <= mouseY <= 510):
            stroke(255)
            rect(500, 460, 400, 50)
        elif (500 <= mouseX <= 900) and (520 <= mouseY <= 570):
            stroke(255)
            rect(500, 520, 400, 50)
        elif (500 <= mouseX <= 900) and (580 <= mouseY <= 630):
            stroke(255)
            rect(500, 580, 400, 50)
        elif (500 <= mouseX <= 900) and (640 <= mouseY <= 690):
            stroke(255)
            rect(500, 640, 400, 50)
    
    # stage 2 starts the game itself.
    if stage == 2:
        image(img, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        image(pause_img, 1200, 650, 200, 150)
            
        game.display()
        if game.alive == True:
            fill(255)
            textFont(crackmanFont)
            textAlign(CENTER)
            textSize(20)
            text("Game Menu", 70, 40)
            noFill()
            if (10 <= mouseX <= 140) and (10 <= mouseY <= 45):
                stroke(255)
                rect(10, 20, 120, 25)
                
            text("Easy", 500,40)
            text("Medium", 580, 40)
            text("Hard", 670, 40)
            noFill()
            
            if (470 <= mouseX <= 530) and (15 <= mouseY <= 45) and level == True:
                stroke(255)
                rect(470, 15, 60, 30)
            
            if (540 <= mouseX <= 620) and (15 <= mouseY <= 45) and level == True:
                stroke(255)
                rect(540, 15, 80, 30)
            
            if (640 <= mouseX <= 700) and (15 <= mouseY <= 45) and level == True:
                stroke(255)
                rect(640, 15, 60, 30)
                
                
    # stage 3 shows the leaderboard.
    if stage == 3:
        game.leader_board_show()
    # stage 4 is the instructions on how to play the game.
    if stage == 4:
        image(img, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        fill(255)
        textFont(crackmanFont)
        textAlign(CENTER)
        textSize(40)
        text("Instructions: " + "\n\n", 700, 300)
        textSize(25)
        text("1. Go around the maze using the arrow keys and collect energy boosts" + "\n" + " or cuddle a campus cat to gain campus dirhams" + "\n\n" + "2. Avoid the Evil sprites" + "\n\n" + "3. Reach the torch at the end of the maze after collecting all the goodies to win the game" + "\n\n" + "4. You cannot change the level you chose in the begining of the game!" + "\n\n" + "5. You can Pause and Play the game at anytime with the button in the bottom right corner"+ "\n\n" + "6. At anytime, press m to mute or unmute the audio"+ "\n\n" + "IT'S HARDER THAN YOU THINK!!", 700, 350)
        fill(255)
        textFont(crackmanFont)
        textAlign(CENTER)
        textSize(20)
        text("Game Menu", 70, 40)
        noFill()
        if (10 <= mouseX <= 140) and (10 <= mouseY <= 45):
            stroke(255)
            rect(10, 20, 120, 25)
    # stage 5 closes the game.
    if stage == 5:
        exit()

def keyPressed():
    if keyCode == LEFT:
        game.player.inputHandler[LEFT] = True
    elif keyCode == RIGHT:
        game.player.inputHandler[RIGHT] = True
    elif keyCode == DOWN:
        game.player.inputHandler[DOWN] = True
    elif keyCode == UP:
        game.player.inputHandler[UP] = True

def keyReleased():
    if keyCode == LEFT:
        game.player.inputHandler[LEFT] = False
    elif keyCode == RIGHT:
        game.player.inputHandler[RIGHT] = False
    elif keyCode == DOWN:
        game.player.inputHandler[DOWN] = False
    elif keyCode == UP:
        game.player.inputHandler[UP] = False

def mouseClicked():
    global game, stage, level, paused
    # writing to the file after game over
    if not game.alive or game.win:
        with open("leaderboard.txt", "a") as writer:
            scr = str(game.score * 10) + "\n"
            writer.write(scr)
    # instantiating a new game
    if not game.alive or game.win:
        game = Game(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        level = True
        stage = 1
    # click detection for the main menu buttons.
    if (500 <= mouseX <= 900) and (460 <= mouseY <= 510):
        stage = 2
    if (500 <= mouseX <= 900) and (520 <= mouseY <= 570):
        stage = 3
    if (500 <= mouseX <= 900) and (580 <= mouseY <= 630):
        stage = 4
    if (500 <= mouseX <= 900) and (640 <= mouseY <= 690):
        stage = 5
    if (10 <= mouseX <= 140) and (10 <= mouseY <= 50):
        stage = 1
    # click detection for the pause/play
    if (1200 <= mouseX <= 1400) and (650 <= mouseY <= 800) and paused == False:
        noLoop()
        paused = True
    elif (1200 <= mouseX <= 1400) and (650 <= mouseY <= 800) and paused == True:
        loop()
        paused = False
     
    # controlling and selecting: Easy, Medium and Hard levels    
    if (470 <= mouseX <= 530) and (15 <= mouseY <= 45) and level == True:
        game.numevil = 3
        level = False
        
    if  (540 <= mouseX <= 620) and (15 <= mouseY <= 45) and level == True:
        game.addsprites(3)
        level = False
        
    if (640 <= mouseX <= 700) and (15 <= mouseY <= 45) and level == True:
        game.addsprites(6)
        level = False

def keyTyped():
    # controlling audio
    global soundOn
    if (key == 'm' or key=='M') and soundOn==True:
        game.start_game.mute()
        game.eat_sprite.mute()
        game.bg_music.mute()
        game.pacman_win.mute()
        soundOn = False
    elif (key == 'm' or key=='M') and soundOn==False:
        game.start_game.unmute()
        game.eat_sprite.unmute()
        game.bg_music.unmute()
        game.pacman_win.unmute()
        soundOn = True
        
