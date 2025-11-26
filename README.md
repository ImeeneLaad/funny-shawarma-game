# funny-shawarma-game

**Description:**
funny-shawarma-game is a 2D Pygame adventure where Imene tries to reclaim her stolen Shawarma from her mischievous friends! Navigate through three challenging levels, dodge enemy attacks, and collect snacks to succeed.


## **Story**

Imene went out to eat, but her friends **Rieb, Nour, and Kamel** stole her Shawarma! To get it back:

1. Face **Rieb** in Level 1 (he throws cats).
2. Confront **Nour** in Level 2 (he throws knives).
3. Defeat **Kamel** in Level 3, who guards the Shawarma.

Collect at least **25 snacks** along the way to win the final battle.


## **Gameplay**

* **Player (Imene)**

  * Lives: 3 hearts.
  * Controls: Arrow keys or WASD.
  * Goal: Collect snacks and reach the Shawarma.

* **Enemies**

  * Level 1: Rieb → throws cats.
  * Level 2: Nour → throws knives.
  * Level 3: Kamel → blocks and attacks.

* **Collectibles**

  * Snacks: Increase your count. Minimum 25 required to get the Shawarma.

* **Game Over**

  * Lose all 3 hearts → Game Over.
  * Reach final level with <25 snacks → cannot reclaim Shawarma.



## **Installation**

1. Install Python 3.8+
2. Install Pygame:

   ```bash
   pip install pygame
   ```
3. Clone or download the repository:

   ```bash
   git clone <your-repo-url>
   ```
4. Run the game:

   ```bash
   python main.py
   ```

---

## **Project Structure**

```
ShawarmaQuest/
│
├── main.py          # Launches the game and handles level transitions
├── level1.py        # Level 1: Rieb
├── level2.py        # Level 2: Nour
├── level3.py        # Level 3: Kamel
├── assets/
│   ├── images/      # Player, enemies, snacks, backgrounds
│   └── sounds/      # Effects and music
└── README.md        # This file
```

---

## **Controls**

* Move: `Arrow Keys` or `WASD`
* Quit: `ESC`

---

## **Credits**

* Game Concept: Imene Laadheri
* Developed with: [Pygame](https://www.pygame.org/)



## **License**

This project is open-source. Feel free to modify or share!



## **Future Features**

* Animated attacks and collectibles.
* More levels and enemies.
* Power-ups for Imene.
* Highscore tracking.



**Have fun getting your Shawarma back! 🍔😄**
