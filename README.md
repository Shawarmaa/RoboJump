# 🤖 RoboJump

A delightful platform jumping game built with Python and Tkinter, inspired by the classic DoodleJump. Guide your robot through an endless vertical adventure!

![game](https://github.com/user-attachments/assets/c48665a4-51bd-489d-8c18-ef6859d5b686)

## 🎮 Game Features

- **Endless Platforming**: Jump from platform to platform and see how high you can climb!
- **Power-ups**: Grab the jetpack to soar through the sky
- **Increasing Difficulty**: The game becomes more challenging as you progress
- **High Score System**: Compete with other players and save your best scores
- **Customizable Controls**: Configure your preferred control scheme in the options menu

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually comes with Python)

### Installation

1. Clone the repository
```bash
git clone https://github.com/Shawarmaa/RoboJump.git
cd robojump
```

2. Run the game
```bash
python main.py
```

## 🎯 How to Play

- Use **Left Arrow** and **Right Arrow** keys to move horizontally
- Press **J** to activate the jetpack when available
- Press **B** for the boss key (quickly hide the game!)
- Your robot automatically jumps when landing on platforms
- Fall below the screen and it's game over!

## 🎨 Game Controls

| Key           | Action        |
|---------------|---------------|
| Left Arrow    | Move Left     |
| Right Arrow   | Move Right    |
| J             | Jetpack       |
| B             | Boss Key      |

## 🛠️ Technical Features

- **Smooth Physics**: Realistic gravity and movement mechanics
- **Save System**: Save your progress and continue later
- **Leaderboard**: Track top scores across gaming sessions
- **Pause Functionality**: Take a break anytime during gameplay
- **Custom Assets**: Unique visual elements and animations

## 📁 File Structure

```
robojump/
│
├── main.py           # Main game file
├── files/           # Game assets directory
│   ├── background.png
│   ├── bird_left.png
│   ├── bird_right.png
│   └── ...
├── scores.txt       # Leaderboard data
└── game_save.json   # Save game data
```

## 💾 Save System

The game automatically saves your high scores to `scores.txt`. You can also manually save your game progress, which will be stored in `game_save.json`.

## 🔧 Configuration

You can customize various game settings through the options menu:
- Control bindings
- Player name

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the classic DoodleJump game
