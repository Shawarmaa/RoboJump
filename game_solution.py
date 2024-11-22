import json
import random
import tkinter as tk
from tkinter import font

WIDTH = 480
HEIGHT = 640
GRAVITY = 0.5
JUMP_STRENGTH = -17
HORIZONTAL_STRENGTH = 7
JETPACK_STRENGTH = 5
START_X, START_Y = 240, 480

TILE_WIDTH = 102
TILE_HEIGHT = 24
PLAYER_HEIGHT = 49
PLAYER_WIDTH = 47  # also enemy width

LEADERBOARD_FILE = "scores.txt"
SAVE_FILE = "game_save.json"
FPS = 3


class RoboJump:
    """
    DoodleJump class represents the game logic for the Doodle Jump game.

    It initializes the game window, sets up key bindings,
    and loads assets such as images for the game.
    It handles the game loop, player movements, score tracking,
    and interactions with game elements like tiles, enemies, and power-ups.
    """

    def __init__(self):
        """
        Initializes the game window and sets up the initial state of the game.

        Args:
            window: The tkinter window object used for creating
            the game interface.
        """
        self.window = tk.Tk()
        self.window.title("Robo Jump")
        self.window.resizable(False, False)
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.main_menu = True
        self.playing = False
        self.paused = False

        self.player_x_pos = START_X
        self.player_y_pos = START_Y
        self.player_y_velocity = -JUMP_STRENGTH
        self.player_x_velocity = 0

        self.score = 0
        self.name = "Bruh"

        self.tiles = []
        self.player_heights = []
        self.buttons = []

        self.tile_y_pos = 70
        self.enemy_chance = 0.1
        self.space_between = 50
        self.difficulty_level = 1000

        self.boss = None
        self.is_jetpack_on = False
        self.is_power_up_on = False
        self.open_from_save = False
        self.boss_key_pressed = False

        self.left_bind = "Left"
        self.right_bind = "Right"
        self.boss_bind = "b"
        self.jetpack_bind = "j"

        self.window.bind(f"<{self.left_bind}>", self.move_left)
        self.window.bind(f"<{self.right_bind}>", self.move_right)
        self.window.bind(f"<KeyRelease-{self.left_bind}>", self.stop_move)
        self.window.bind(f"<KeyRelease-{self.right_bind}>", self.stop_move)
        self.window.bind("<b>", self.display_work_screen)
        self.window.bind("<j>", self.deploy_jet_pack)

        # assets
        self.background_image = tk.PhotoImage(file="files/background.png")
        self.boss_image = tk.PhotoImage(file="files/boss_image.png")
        self.leaderboard_bg_image = tk.PhotoImage(
            file="files/leaderboard_bg.png"
        )
        self.gameover_bg_image = tk.PhotoImage(file="files/game_over_bg.png")
        self.player_right_image = tk.PhotoImage(file="files/bird_right.png")
        self.player_left_image = tk.PhotoImage(file="files/bird_left.png")
        self.main_menu_image = tk.PhotoImage(file="files/main_menu.png")
        self.tile_image = tk.PhotoImage(file="files/regular_tile.png")
        self.enemy_image = tk.PhotoImage(file="files/enemy.png")
        self.save_game_btn_image = tk.PhotoImage(
            file="files/save_game_btn_image.png"
        )
        self.leaderboard_btn_image = tk.PhotoImage(
            file="files/leaderboard_btn_image.png"
        )
        self.menu_btn_image = tk.PhotoImage(file="files/menu_btn_image.png")
        self.options_btn_image = tk.PhotoImage(
            file="files/options_btn_image.png"
        )
        self.play_btn_image = tk.PhotoImage(file="files/play_btn_image.png")
        self.saves_btn_image = tk.PhotoImage(file="files/saves_btn_image.png")
        self.submit_name_btn_image = tk.PhotoImage(
            file="files/submit_name_btn_image.png"
        )
        self.options_screen_image = tk.PhotoImage(file="files/options_bg.png")
        self.top_image = tk.PhotoImage(file="files/top.png")
        self.pause_btn_image = tk.PhotoImage(file="files/pause_btn.png")
        self.play_icon_image = tk.PhotoImage(file="files/play_btn.png")
        self.pause_screen_image = tk.PhotoImage(file="files/paused_bg.png")

        self.window.tk.call(
            "font",
            "create",
            "DoodleJumpFont",
            "-family",
            "imgs/DoodleJump.ttf",
        )
        self.custom_font = font.Font(family="DoodleJumpFont", size=25)

        self.init_main_menu()

        self.game_loop()

        self.window.mainloop()

    def init_main_menu(self):
        """
        Initializes the main menu by resetting the canvas, setting the state
        to the main menu, and adding buttons, images, and tiles.
        This method also places the player character and initializes
        the name input field with a submit button.

        This method sets up:
        - The background image for the main menu.
        - Buttons for navigating to different menu screens.
        - The player character's initial position and appearance.
        - An input field for the player name and a button to submit the name.
        """
        # Reset the canvas and set the state for the main menu
        self.reset_canvas()
        self.main_menu = True
        self.playing = False

        # Set the background image for the main menu
        self.canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.main_menu_image)

        # Create and place the Play button
        play_btn = tk.Button(
            self.window,
            image=self.play_btn_image,
            command=self.switch_to_play,
            bd=0,
        )
        play_btn.place(x=240, y=178)

        # Create and place the Options button
        options_btn = tk.Button(
            self.window,
            image=self.options_btn_image,
            command=self.switch_to_options,
            bd=0,
        )
        options_btn.place(x=240, y=265)

        # Create and place the Leaderboard button
        leaderboard_btn = tk.Button(
            self.window,
            image=self.leaderboard_btn_image,
            command=self.switch_to_leaderboard,
            bd=0,
        )
        leaderboard_btn.place(x=240, y=348)

        # Create and place the Saves button
        saves_btn = tk.Button(
            self.window,
            image=self.saves_btn_image,
            command=self.switch_to_saves,
            bd=0,
        )
        saves_btn.place(x=50, y=572)

        # Initialize menu player position and velocity for the main menu
        self.menu_player_x_pos = 96
        self.menu_player_y_pos = 431
        self.menu_player_y_velocity = JUMP_STRENGTH
        self.menu_player_x_velocity = 0

        # Create the player image on the canvas
        self.menu_player = self.canvas.create_image(
            96, 431, anchor="nw", image=self.player_right_image
        )

        # Create a tile on the canvas
        tile = self.canvas.create_image(
            WIDTH // 4 - 50,
            START_Y + TILE_HEIGHT,
            anchor="nw",
            image=self.tile_image,
        )
        self.tiles.append(tile)

        # Initialize the variable for the player name input
        name_var = tk.StringVar()

        # Create and place the name entry field
        name_entry = tk.Entry(
            self.window, width=6, font=self.custom_font, textvariable=name_var
        )
        name_entry.place(x=228, y=430)
        self.buttons.append(name_entry)

        # Create and place the submit name button
        submit_name_btn = tk.Button(
            self.window,
            image=self.submit_name_btn_image,
            command=lambda: self.submit_name(name_var.get()),
            bd=0,
        )
        submit_name_btn.place(x=230, y=474)

        # Add all buttons to the list for potential management
        self.buttons.append(play_btn)
        self.buttons.append(options_btn)
        self.buttons.append(leaderboard_btn)
        self.buttons.append(saves_btn)
        self.buttons.append(submit_name_btn)

    def game_loop(self):
        """
        Main game loop that updates the game state based on whether the player
        is in the main menu or playing the game. It handles player movement,
        gravity, collision detection, and updates the canvas accordingly.

        Updates the menu player's position based on gravity.
        If in the game, it updates the player's position handles
        jetpack mechanics,checks collisions, and updates object positions.
        """
        if self.main_menu:
            # Update player's vertical velocity and position based on gravity
            self.menu_player_y_velocity += GRAVITY
            self.menu_player_y_pos += self.menu_player_y_velocity

            # Check for collision with tiles in the menu
            for tile in self.tiles:
                tile_x, tile_y = self.canvas.coords(tile)

                # menu player is colliding with a tile
                if (
                    self.menu_player_x_pos + PLAYER_WIDTH > tile_x
                    and self.menu_player_x_pos < tile_x + TILE_WIDTH
                    and self.menu_player_y_pos + PLAYER_HEIGHT <= tile_y
                    and self.menu_player_y_pos
                    + PLAYER_HEIGHT
                    + self.menu_player_y_velocity
                    >= tile_y
                ):
                    # Reset vertical velocity to simulate a jump
                    self.menu_player_y_velocity = JUMP_STRENGTH

            # Update the position of the menu player on the canvas
            self.canvas.coords(
                self.menu_player,
                self.menu_player_x_pos,
                self.menu_player_y_pos,
            )

        elif self.playing:
            # Apply gravity to the player's vertical velocity
            self.player_y_velocity += GRAVITY

            # Handle jetpack activation
            if self.is_jetpack_on:
                self.player_y_pos -= JETPACK_STRENGTH + 10  # Jetpack movement
                self.player_y_velocity = (
                    -15
                )  # Override vertical velocity when jetpack is on
            else:
                # Apply gravity if the jetpack is not on
                self.player_y_pos += self.player_y_velocity

            # Check and handle player's horizontal and vertical bounds
            self.check_horizontal_bound()
            self.check_vertical_bound()

            # Move objects and enemies
            self.move_objects()
            self.move_enemy()

            # Check for collisions
            self.check_collision()

            # Update the player's horizontal position
            self.player_x_pos += self.player_x_velocity

            # Update the player's position on the canvas
            self.canvas.coords("player", self.player_x_pos, self.player_y_pos)

            # Raise the "top" tag to ensure tiles don't cover the score
            self.canvas.tag_raise("top")

        # Call the game loop again after a set frame rate
        self.window.after(FPS, self.game_loop)

    def reset_canvas(self):
        """
        Reset the game canvas and initialize necessary game variables.
        Clears the canvas, destroys buttons, and resets player and game state.
        """
        # Clear all items from the canvas
        self.canvas.delete("all")

        # Destroy any buttons that were added to the window
        for btn in self.buttons:
            btn.destroy()

        # Reset values if starting from a new game (not from save)
        if not self.open_from_save:
            self.player_x_pos = START_X
            self.player_y_pos = START_Y
            self.player_y_velocity = -JUMP_STRENGTH
            self.player_x_velocity = 0

        # Reset game state flags
        self.is_jetpack_on = False  # Jetpack is off initially
        self.is_power_up_on = False  # Power-ups are not active

        # Reinitialize game variables
        self.buttons = []
        self.tiles = []
        self.player_heights = []
        self.open_from_save = False
        self.tile_y_pos = 70
        self.enemy_chance = 0.1
        self.space_between = 50
        self.difficulty_level = 1000

    def switch_to_play(self):
        """
        Switch to the gameplay screen: reset canvas, set up player,
        background, and UI.Initializes the game environment for active play,
        including the score display,pause button, and initial tiles.
        """
        self.reset_canvas()

        # Set the game state to playing and hide the main menu
        self.playing = True
        self.main_menu = False

        # Set up background and top UI layer
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.background_image
        )
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.top_image, tags="top"
        )

        # Display the score at the top-left of the screen
        self.canvas.create_text(
            10,
            10,
            anchor="nw",
            font=self.custom_font,
            tags=("score", "top"),
            text=f"{self.score}",
            fill="white",
        )

        # Add a pause button to the top-right corner
        self.pause_btn = tk.Button(
            self.window,
            image=self.pause_btn_image,
            command=self.pause_game,
            bd=0,
        )
        self.pause_btn.place(x=WIDTH - 36 - 13, y=4)
        self.buttons.append(self.pause_btn)

        # Place the player image at the starting position
        self.canvas.create_image(
            self.player_x_pos,
            self.player_y_pos,
            anchor="nw",
            image=self.player_right_image,
            tags="player",
        )

        # Add initial tiles to the canvas
        self.add_initial_tiles()

    def check_horizontal_bound(self):
        """
        checks if the player goes beyond the screen horizontally
        Moves the position of the player to create a teleportation effect
        """
        if self.player_x_pos >= WIDTH:
            self.player_x_pos = 1
        elif self.player_x_pos <= 0:
            self.player_x_pos = WIDTH - 1

    def check_vertical_bound(self):
        """
        checks if the player has fallen of the bottom
        to end the game
        """
        if self.player_y_pos >= HEIGHT:  # if player falls of the bottom
            self.ending_screen()

    def ending_screen(self):
        """
        Displays the game over screen with the player's score, high score,
        and options to go back to the main menu or view the leaderboard.
        """
        score = self.score
        self.playing = False
        self.reset_canvas()
        self.main_menu = False

        self.canvas.create_image(
            0, 0, anchor="nw", image=self.gameover_bg_image
        )
        menu_btn = tk.Button(
            self.window,
            image=self.menu_btn_image,
            command=self.init_main_menu,
            bd=0,
        )
        menu_btn.place(x=144, y=394)
        self.buttons.append(menu_btn)

        leaderboard_btn = tk.Button(
            self.window,
            image=self.leaderboard_btn_image,
            command=self.switch_to_leaderboard,
            bd=0,
        )
        leaderboard_btn.place(x=144, y=474)
        self.buttons.append(leaderboard_btn)

        self.update_score()
        high_score = self.read_scores()[0].split()[1]

        self.canvas.create_text(
            244,
            170,
            font=self.custom_font,
            text=f"Your score: {score}",
            fill="white",
        )
        self.canvas.create_text(
            244,
            210,
            font=self.custom_font,
            text=f"High score: {high_score}",
            fill="white",
        )
        self.canvas.create_text(
            244,
            250,
            font=self.custom_font,
            text=f"Your Name: {self.name}",
            fill="white",
        )

        self.score = 0

    def check_collision(self):
        """
        Checks for collisions between the player and tiles.
        If the jetpack is off,the player will collide with enemies or tiles.
        Removes tiles that fall off the screen.
        """
        for tile in self.tiles:
            tile_x, tile_y = self.canvas.coords(tile)
            tag = self.canvas.gettags(tile)[0]

            if not self.is_jetpack_on:
                if tag == "enemy":
                    tile_width = PLAYER_WIDTH
                    is_colliding = (
                        # player's right side is beyond the tile's left
                        self.player_x_pos + PLAYER_WIDTH > tile_x
                        # player's left side is within the tile's width
                        and self.player_x_pos < tile_x + tile_width
                        # player's bottom is above the tile's top
                        and self.player_y_pos + PLAYER_HEIGHT > tile_y
                        # player's top is below the tile's bottom
                        and self.player_y_pos < tile_y + TILE_HEIGHT
                    )

                    if is_colliding:
                        self.ending_screen()
                        break

                else:
                    tile_width = TILE_WIDTH
                    is_colliding = (
                        # player's right side is beyond the tile's left
                        self.player_x_pos + PLAYER_WIDTH > tile_x
                        # player's left side is within the tile's width
                        and self.player_x_pos < tile_x + tile_width
                        # player's bottom is at or above the tile's top
                        and self.player_y_pos + PLAYER_HEIGHT <= tile_y
                        # player will land on the tile
                        and self.player_y_pos
                        + PLAYER_HEIGHT
                        + self.player_y_velocity
                        >= tile_y
                    )

                    if is_colliding:
                        self.player_y_velocity = JUMP_STRENGTH

            # Remove tiles that fall beyond the height limit
            if tile_y >= HEIGHT:
                self.canvas.delete(tile)
                self.tiles.remove(tile)

    def move_objects(self):
        """
        Moves objects (tiles, player, etc.) based on the player's movement.
        Adjusts tiles and adds score when the player moves above certain
        height all objects will move down to
        replicate a scrolling effect
        """
        self.player_heights.append(self.player_y_pos)
        value = 244  # Player height limit

        # player is visually above the threshold and falling or using jetpack
        if self.player_y_pos <= value and (
            self.player_y_velocity <= 0 or self.is_power_up_on
        ):
            # Calculate the distance moved to replicate player falling
            higher_height = self.player_heights[-1]
            lower_height = self.player_heights[-2]
            distance = -higher_height + lower_height

            # Add the distance to the score and add new tiles
            self.add_score(distance)
            self.add_tiles()

            # Move all objects (tiles) by the calculated distance
            for object in self.tiles:
                self.canvas.move(object, 0, distance * 1.6)

            # Adjust the player's vertical position by the distance moved
            self.player_y_pos += distance * 2

        # Keep track of only the last 5 player heights to avoid memory bloat
        self.player_heights = self.player_heights[-5:]

    def add_tiles(self):
        """
        Adds new tiles or enemies to the game based on the current
        score and difficulty.The space between tiles increases as
        the player's score rises. The function spawns either an enemy
        or a regular tile, and ensures no collisions with existing tiles.
        """
        # Increase space between tiles and raise difficulty based on score
        if self.score > self.difficulty_level:
            self.space_between += 50
            self.difficulty_level += 1000

        x = random.randint(
            0, 380
        )  # Random horizontal position within the canvas width
        y = (
            self.tile_y_pos - self.space_between
        )  # Vertical position adjusted for space

        # Randomly choose between spawning an enemy or a regular tile
        spawn_choice = random.random()
        if spawn_choice < self.enemy_chance:
            # Spawn an enemy
            spawned_object = self.canvas.create_image(
                x, y, anchor="nw", image=self.enemy_image, tags=("enemy")
            )
        else:
            # Spawn a regular tile
            spawned_object = self.canvas.create_image(
                x, y, anchor="nw", image=self.tile_image, tags=("tile")
            )

        # Add the newly spawned object to the tiles list
        self.tiles.append(spawned_object)

        # Update the vertical position for the next tile spawn
        self.tile_y_pos = y

    def add_score(self, additional_score):
        """
        Adds to the player's score based on their movement or height change.

        Args:
            additional_score (int or float): Amount to increase the score by.
        """
        self.score += additional_score
        self.canvas.itemconfig("score", text=self.score)

    def move_enemy(self):
        """
        Moves the enemy objects across the screen. If an enemy goes off the
        screen (right side), it is reset to the left side.
        """
        for object in self.tiles:
            x, y = self.canvas.coords(object)
            tag = self.canvas.gettags(object)[0]

            if tag == "enemy":
                if x > WIDTH:
                    self.canvas.moveto(object, -PLAYER_WIDTH, y)
                else:
                    self.canvas.move(object, 1, 0)

    def add_initial_tiles(self):
        """
        Adds the initial set of tiles to the canvas in specific positions.
        The tiles are placed in a grid-like pattern around the player's
        initial position.
        """
        start = self.canvas.create_image(
            self.player_x_pos,
            self.player_y_pos + PLAYER_HEIGHT + TILE_HEIGHT,
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        quadrant_width = WIDTH // 2
        quadrant_height = HEIGHT // 2

        tile1 = self.canvas.create_image(
            quadrant_width // 3,  # x = 240 // 3 = 80
            quadrant_height // 3,  # y = 320 // 3 = 106
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile2 = self.canvas.create_image(
            quadrant_width // 3 * 2,  # x = 240 // 3 * 2 = 160
            quadrant_height // 3 * 2,  # y = 320 // 3 * 2 = 213
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile3 = self.canvas.create_image(
            quadrant_width + quadrant_width // 3,  # x = 360 + 240 // 3 = 400
            quadrant_height // 3,  # y = 106
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile4 = self.canvas.create_image(
            quadrant_width
            + quadrant_width // 3 * 2,  # x = 360 + 240 // 3 * 2 = 480
            quadrant_height // 3 * 2,  # y = 213
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile5 = self.canvas.create_image(
            quadrant_width // 3,  # x = 80
            quadrant_height + quadrant_height // 3,  # y = 480 + 106 = 586
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile6 = self.canvas.create_image(
            quadrant_width // 3 * 2,  # x = 160
            quadrant_height + quadrant_height // 3 * 2,  # y = 480 + 213 = 693
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile7 = self.canvas.create_image(
            quadrant_width + quadrant_width // 3,  # x = 400
            quadrant_height + quadrant_height // 3,  # y = 586
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        tile8 = self.canvas.create_image(
            quadrant_width + quadrant_width // 3 * 2,  # x = 480
            quadrant_height + quadrant_height // 3 * 2,  # y = 693
            anchor="nw",
            image=self.tile_image,
            tags=("tile"),
        )

        self.tiles.append(start)
        self.tiles.append(tile1)
        self.tiles.append(tile2)
        self.tiles.append(tile3)
        self.tiles.append(tile4)
        self.tiles.append(tile5)
        self.tiles.append(tile6)
        self.tiles.append(tile7)
        self.tiles.append(tile8)

    def pause_game(self):
        """
        Toggles the game's pause state and updates the UI accordingly.

        If the game is paused, it displays the pause screen, changes the
        pause button to a play button, and adds a save game button.
        If the game is resumed, it removes the pause screen, restores
        the pause button, and removes the save game button.

        Args:
            None
        """
        # Stops the game from playing
        self.playing = not self.playing

        if not self.playing:
            # Show the pause screen and change buttons
            self.canvas.create_image(
                0, 0, anchor="nw", image=self.pause_screen_image, tags="pause"
            )
            self.pause_btn.config(image=self.play_icon_image)

            # Add the save game button
            self.save_game_btn = tk.Button(
                self.window,
                image=self.save_game_btn_image,
                command=self.save_game,
                bd=0,
            )
            self.buttons.append(self.save_game_btn)
            self.save_game_btn.place(x=144, y=320)

        else:
            # Remove the save game button and revert to the pause button
            self.save_game_btn.destroy()
            self.pause_btn.config(image=self.pause_btn_image)

            # Remove the pause screen
            self.canvas.delete("pause")

    def switch_to_options(self):
        """
        Switches to the options screen, displaying the options background
        and buttons for changing key bindings for player controls.
        """
        # Reset the canvas and update the main menu state
        self.reset_canvas()
        self.main_menu = False

        # Display the options screen background
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.options_screen_image
        )

        # Create and place the menu button to return to the main menu
        menu_btn = tk.Button(
            self.window,
            image=self.menu_btn_image,
            command=self.init_main_menu,
            bd=0,
        )
        menu_btn.place(x=144, y=523)
        self.buttons.append(menu_btn)

        # Create and place buttons for changing key bindings
        keybind_left = tk.Button(
            self.window,
            text=f"Change Move Left: {self.left_bind}",
            font=self.custom_font,
            compound="center",
            command=lambda: self.set_left_keybind(keybind_left),
        )
        keybind_left.place(x=144, y=182)

        keybind_right = tk.Button(
            self.window,
            text=f"Change Move Right: {self.right_bind}",
            font=self.custom_font,
            compound="center",
            command=lambda: self.set_right_keybind(keybind_right),
        )
        keybind_right.place(x=144, y=268)

        keybind_boss_key = tk.Button(
            self.window,
            text=f"Change Boss Key: {self.boss_bind}",
            font=self.custom_font,
            compound="center",
            command=lambda: self.set_boss_keybind(keybind_boss_key),
        )
        keybind_boss_key.place(x=144, y=353)

        keybind_jetpack_key = tk.Button(
            self.window,
            text=f"Change Jetpack Key: {self.jetpack_bind}",
            font=self.custom_font,
            compound="center",
            command=lambda: self.set_jetpack_keybind(keybind_jetpack_key),
        )
        keybind_jetpack_key.place(x=144, y=438)

        # Append the buttons to the list for management
        self.buttons.append(keybind_right)
        self.buttons.append(keybind_left)
        self.buttons.append(keybind_boss_key)
        self.buttons.append(keybind_jetpack_key)

    def key_press(self, event, direction, button):
        """
        Handle key press events to update the keybinding.

        Args:
            event (tk.Event): The key press event.
            direction (str): The type of keybinding being set
            ("left", "right", "boss", "jetpack").
            button (tk.Button): The button to update the display
            with the new keybinding.
        """
        if direction == "left":
            self.left_bind = event.keysym
            self.window.bind(f"<{self.left_bind}>", self.move_left)
            self.window.bind(f"<KeyRelease-{self.left_bind}>", self.stop_move)
            button.configure(text=f"Move Left: {self.left_bind}")

        elif direction == "right":
            self.right_bind = event.keysym
            self.window.bind(f"<{self.right_bind}>", self.move_right)
            self.window.bind(f"<KeyRelease-{self.right_bind}>", self.stop_move)
            button.configure(text=f"Move Right: {self.right_bind}")

        elif direction == "boss":
            self.boss_bind = event.keysym
            self.window.bind(f"<{self.boss_bind}>", self.display_work_screen)
            button.configure(text=f"Boss Key: {self.boss_bind}")

        elif direction == "jetpack":
            self.jetpack_bind = event.keysym
            self.window.bind(f"<{self.jetpack_bind}>", self.deploy_jet_pack)
            button.configure(text=f"Jetpack Key: {self.jetpack_bind}")

        # Unbind the keypress event after a key has been set
        self.window.unbind("<KeyPress>")

    def set_boss_keybind(self, button):
        """
        Set the keybinding for the boss key.

        Args:
            button (tk.Button): The button that is used to display
            the keybinding.
        """
        button.configure(text="Press the key")
        self.window.unbind(f"<{self.boss_bind}>")
        self.window.bind(
            "<KeyPress>", lambda event: self.key_press(event, "boss", button)
        )

    def set_jetpack_keybind(self, button):
        """
        Set the keybinding for the jetpack.

        Args:
            button (tk.Button): The button that is used to display
            the keybinding.
        """
        button.configure(text="Press the key")
        self.window.unbind(f"<{self.jetpack_bind}>")
        self.window.bind(
            "<KeyPress>",
            lambda event: self.key_press(event, "jetpack", button),
        )

    def set_left_keybind(self, button):
        """
        Set the keybinding for moving left.

        Args:
            button (tk.Button): The button that is used to display
            the keybinding.
        """
        button.configure(text="Press the key")
        self.window.unbind(f"<{self.left_bind}>")
        self.window.unbind(f"<KeyRelease-{self.left_bind}>")
        self.window.bind(
            "<KeyPress>", lambda event: self.key_press(event, "left", button)
        )

    def set_right_keybind(self, button):
        """
        Set the keybinding for moving right.

        Args:
            button (tk.Button): The button that is used to display
            the keybinding.
        """
        button.configure(text="Press the key")
        self.window.unbind(f"<{self.right_bind}>")
        self.window.unbind(f"<KeyRelease-{self.right_bind}>")
        self.window.bind(
            "<KeyPress>", lambda event: self.key_press(event, "right", button)
        )

    def move_left(self, event):
        """
        Moves the player left and updates the player's image.

        Args:
            event: The event triggered by the left key press.
        """
        self.player_x_velocity = -HORIZONTAL_STRENGTH
        self.canvas.itemconfig("player", image=self.player_left_image)

    def move_right(self, event):
        """
        Moves the player right and updates the player's image.

        Args:
            event: The event triggered by the right key press.
        """
        self.player_x_velocity = HORIZONTAL_STRENGTH
        self.canvas.itemconfig("player", image=self.player_right_image)

    def stop_move(self, event):
        """
        Stops the player's horizontal movement.

        Args:
            event: The event triggered when the player releases
            the left or right key.
        """
        self.player_x_velocity = 0

    def deploy_jet_pack(self, event):
        """Toggles the jetpack and power-up states."""
        self.is_jetpack_on = not self.is_jetpack_on
        self.is_power_up_on = not self.is_power_up_on

    def display_work_screen(self, event):
        """
        Toggles between showing a work-related image and the original screen
        when the boss key is pressed.

        Args:
            event (tk.Event): The event that triggered the method.
        """
        self.window.title("File Manager")

        self.boss_key_pressed = not self.boss_key_pressed

        if self.boss_key_pressed:
            # Create and display the work-related image
            self.boss = tk.Canvas(self.window, height=HEIGHT, width=WIDTH)
            self.boss.place(x=0, y=0, anchor="nw")
            self.boss.create_image(
                0, 0, anchor="nw", image=self.boss_image, tags=("boss")
            )
        else:
            self.boss.destroy()
            self.window.title("Doodle Jump")

    def switch_to_leaderboard(self):
        """
        Switches the screen to the leaderboard view, displaying the
        leaderboard background and the menu button. Also calls
        `display_scores` to show the top scores.
        """
        # Reset the canvas and set the main menu state to False
        self.reset_canvas()
        self.main_menu = False

        # Display the leaderboard background image
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.leaderboard_bg_image
        )

        menu_btn = tk.Button(
            self.window,
            image=self.menu_btn_image,
            command=self.init_main_menu,
            bd=0,
        )
        menu_btn.place(x=144, y=523)
        self.buttons.append(menu_btn)

        # Display the leaderboard scores
        self.display_scores()

    def read_scores(self):
        """
        Reads the scores from the leaderboard file
        The function splits the data into lines then loops
        through each line and removes line spacing then assigns it to an array
        """
        with open(LEADERBOARD_FILE, "r") as f:
            return [x.strip() for x in f.readlines()]

    def update_score(self):
        """
        Updates the leaderboard with the current player's score.

        The player's name and score are appended to the leaderboard, and the
        list is sorted in descending order based on the score. The top 5
        scores are then written back to the leaderboard file.
        """
        # Retrieve all current scores from the leaderboard file
        all_scores = self.read_scores()

        all_scores.append(f"{self.name}: {self.score}")

        # Sort the scores in descending order based on the key (score value)
        all_scores.sort(
            reverse=True, key=lambda event: float(event.split(":")[1])
        )

        # Keep only the top 5 scores
        all_scores = all_scores[:5]

        # Write the updated leaderboard back to the file
        with open(LEADERBOARD_FILE, "w") as f:
            for entry in all_scores:
                f.write(entry + "\n")

    def display_scores(self):
        """
        Displays the top scores on the canvas.

        The method retrieves the scores from the leaderboard
        file and displays them on the canvas, one score at a time.
        """
        scores = self.read_scores()

        # Initial vertical position for the first score
        y_pos = 200

        # Loop through each score and display it on the canvas
        for i, score in enumerate(scores):
            self.canvas.create_text(
                244,
                y_pos,
                font=self.custom_font,
                text=f"{i+1}. {score}",
                fill="white",
            )
            # Move the vertical position down by 40 pixels for the next score
            y_pos += 40

    def switch_to_saves(self):
        """
        Load the saved game state from a file and restore
        the game to the saved state. If no saved file exists
        or the file is corrupted, it handles the error gracefully.
        """
        try:
            # Try to load the saved game state from a JSON file
            with open(SAVE_FILE, "r") as file:
                game_state = json.load(file)

            # Restore game state from the saved data
            self.main_menu = game_state["main_menu"]
            self.playing = game_state["playing"]
            self.paused = game_state["paused"]
            self.player_x_pos = game_state["player_x_pos"]
            self.player_y_pos = game_state["player_y_pos"]
            self.player_y_velocity = game_state["player_y_velocity"]
            self.player_x_velocity = game_state["player_x_velocity"]
            self.score = game_state["score"]

            # Restore control key bindings
            self.left_bind = game_state["left_bind"]
            self.right_bind = game_state["right_bind"]
            self.boss_bind = game_state["boss_bind"]
            self.jetpack_bind = game_state["jetpack_bind"]

            # Restore other game settings
            self.name = game_state["name"]
            self.boss_key_pressed = game_state["boss_key_pressed"]
            self.player_heights = game_state["player_heights"]
            self.is_jetpack_on = game_state["is_jetpack_on"]
            self.is_power_up_on = game_state["is_power_up_on"]

            # Restore level and tile data
            self.tile_y_pos = game_state["tile_y_pos"]
            self.space_between = game_state["space_between"]
            self.difficulty_level = game_state["difficulty_level"]

            # Bind the controls to the loaded key bindings
            self.window.bind(f"<{self.left_bind}>", self.move_left)
            self.window.bind(f"<{self.right_bind}>", self.move_right)
            self.window.bind(
                f"<KeyRelease-{self.left_bind}>",
                self.stop_move)
            self.window.bind(
                f"<KeyRelease-{self.right_bind}>",
                self.stop_move)
            self.window.bind("<b>", self.display_work_screen)
            self.window.bind("<j>", self.deploy_jet_pack)

        except FileNotFoundError:
            print(
                "No games have been saved"
            )  # Handle case where no saved file is found
        except json.JSONDecodeError:
            print("The saved file has been corrupted")
            # Handle corrupted file

        # Mark as opened from a save and start the game
        self.open_from_save = True
        self.switch_to_play()
        print("Going to saved games")

    def save_game(self):
        """
        Save the current game state to a file in JSON format.
        """
        print("Saving game...")

        # Collect current game state into a dictionary
        game_state = {
            "main_menu": self.main_menu,
            "playing": self.playing,
            "paused": self.paused,
            "player_x_pos": self.player_x_pos,
            "player_y_pos": self.player_y_pos,
            "player_y_velocity": self.player_y_velocity,
            "player_x_velocity": self.player_x_velocity,
            "score": self.score,
            "left_bind": self.left_bind,
            "right_bind": self.right_bind,
            "boss_bind": self.boss_bind,
            "jetpack_bind": self.jetpack_bind,
            "name": self.name,
            "boss_key_pressed": self.boss_key_pressed,
            "player_heights": self.player_heights,
            "is_jetpack_on": self.is_jetpack_on,
            "is_power_up_on": self.is_power_up_on,
            "tile_y_pos": self.tile_y_pos,
            "space_between": self.space_between,
            "difficulty_level": self.difficulty_level,
        }

        # Write the game state to the saved file
        with open(SAVE_FILE, "w") as f:
            json.dump(game_state, f)

        # Return to the main menu after saving
        self.init_main_menu()

    def submit_name(self, name):
        """Sets the player's name."""
        self.name = name


if __name__ == "__main__":
    game = RoboJump()
