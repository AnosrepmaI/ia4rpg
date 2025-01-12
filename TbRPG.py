import random
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.health = 100
        self.attack = 21
        self.inventory = []

    def alive(self):
        return self.health > 0

    def tdamage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {damage} damage! {self.health} health remaining.")

    def mattack(self, monster):
        damage = random.randint(self.attack - 1, self.attack + 5)
        print(f"{self.name} attacks {monster.name} and deals {damage} damage!")
        monster.tdamage(damage)

    def uitem(self):
        if self.inventory:
            item = self.inventory.pop()
            if item == "Potion":
                self.health = min(self.health + 30, 100)
                print(f"{self.name} uses a Potion that restores health! {self.health} current health.")
        else:
            print("You have no items to use!")

    def pinventory(self):
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")

    def gexp(self, amount):
        self.experience += amount
        print(f"{self.name} gains {amount} experience!")
        if self.experience >= self.level * 30:
            self.lvl()

    def lvl(self):
        self.level += 1
        self.attack += 5
        self.health = min(self.health + 30, 100)
        print(
            f"You leveled up! {self.name} is now level {self.level}. Attack increased and some health restored!({self.health}hp)")


class Monster:
    def __init__(self, name, health, attack, special_ability=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.special_ability = special_ability

    def alive(self):
        return self.health > 0

    def tdamage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {damage} damage! {self.health} health remaining.")

    def pattack(self, player):
        damage = random.randint(self.attack - 2, self.attack + 2)
        print(f"{self.name} attacks {player.name} and deals {damage} damage!")
        player.tdamage(damage)

    def use_special_ability(self, player):
        if self.special_ability == "Heal":
            heal_amount = random.randint(5, 10)
            self.health = min(self.health + heal_amount, 50)
            print(f"{self.name} heals for {heal_amount} health! {self.name}'s health is now {self.health}.")
        elif self.special_ability == "Poison":
            poison_damage = random.randint(5, 10)
            print(f"{self.name} inflicted {player.name} with {poison_damage} poison damage!")
            player.tdamage(poison_damage)


class FinalBoss(Monster):
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack, special_ability="Tactical Nuke")

    def pattack(self, player):
        damage = random.randint(self.attack - 1, self.attack + 7)
        print(f"{self.name} unleashes a powerful attack on {player.name} and deals {damage} damage!")
        player.tdamage(damage)

    def use_special_ability(self, player):
        fire_breath_damage = random.randint(15, 30)
        print(f"{self.name} uses Tactical Nuke and deals {fire_breath_damage} damage to {player.name}!")
        player.tdamage(fire_breath_damage)


# Combat with a monster
def combat(player, monster):
    while player.alive() and monster.alive():
        print("\nWhat do you want to do?")
        action = input("[A]ttack  [U]se item  [Q]uit: ").lower()
        print("\n")
        while action not in ['a', 'u', 'q']:
            print("Invalid action. Please choose again.")
            action = input("[A]ttack  [U]use item  [Q]uit: ").lower()

        if action == "a":
            player.mattack(monster)
            if monster.alive():
                monster.pattack(player)
                monster.use_special_ability(player)
        elif action == "u":
            player.uitem()
            if monster.alive():
                monster.pattack(player)
                monster.use_special_ability(player)
        elif action == "q":
            print(f"{player.name} decides to quit.")
            quit()


def enter_room(player, room_number):
    print(f"\nEntering Room {room_number}...")

    monsters = [
        Monster("Goblin", 30, 5),
        Monster("Orc", 60, 10),
        Monster("Salamander", 50, 12, special_ability="Heal"),
        Monster("Black Mamba", 60, 11, special_ability="Poison"),
    ]
    monster = random.choice(monsters)
    print(f"{monster.name} has appeared with {monster.health} health!")

    # Combat with the monster
    combat(player, monster)

    if player.alive():
        loot = random.choice(["Potion", "Nothing"])
        if loot == "Potion":
            player.inventory.append("Potion")
            print(f"\n{player.name} finds a Potion and adds it to the inventory!")

        player.gexp(20)


def print_slow(text, delay=1):
    """Prints the text line by line with a delay."""
    for line in text.split("\n"):
        print(line)
        time.sleep(delay)


def main():
    intro = """
    A heavy, unnatural fog hangs in the air as you approach the dilapidated gates of the Dungeon of Shadows. 
    The cold, damp stone walls rise like a tomb around you, their cracked surface whispering of forgotten souls trapped within. 
    The wind howls through the broken openings, carrying with it faint, unsettling sounds — whispers, scratching, 
    distant cries that seem to echo from the very depths of the earth.
    Legends speak of this forsaken place: a dungeon once home to the most twisted of creatures, now abandoned, yet still hungry for the living. 
    The ground beneath your feet feels wrong, as though the very earth wishes you to turn back. But curiosity — or perhaps something darker — pulls you forward.
    You feel the weight of unseen eyes watching you as the gates creak open, as though they’ve been waiting for you. 
    The air grows colder, and you know in your bones that once you step inside, there may be no escape.
    A shiver crawls up your spine. The dungeon is alive, and it knows you're here.
    """
    print_slow(intro)

    player_name = input("Enter your character's name: ")
    player = Player(player_name)

    print(f"\nWelcome, {player.name}, to the Dungeon!")
    print("You must fight through the dungeon rooms to face the Final Boss.")`

    for room_number in range(1, 4):
        if player.alive():
            enter_room(player, room_number)
        else:
            print(f"{player.name} has been defeated!")
            break

    # If the player is still alive, face the Final Boss
    if player.alive():
        print("\nYou've reached the Final Boss room!")
        final_boss = FinalBoss("Demon Lord", 100, 20)
        print(f"A mighty {final_boss.name} with {final_boss.health} health stands before you!")
        combat(player, final_boss)

    if player.alive():
        print(f"\n{player.name} has defeated the Final Boss and conquered the dungeon!")
    else:
        print("Game Over!")


# Run the game
if __name__ == "__main__":
    main()