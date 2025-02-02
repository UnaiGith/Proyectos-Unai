from abc import ABC, abstractmethod
from enum import StrEnum
# Remove inspections when this ticket is resolved:
# https://youtrack.jetbrains.com/issue/PY-64422/Erroneous-Cannot-find-reference-override-in-typing.pyi-in-Python-3.12
# noinspection PyUnresolvedReferences,PyProtectedMember
from typing import override


# region ------------ Weapon classes ------------


class Weapon(ABC):
    """Abstract class for weapons."""

    def __init__(self, name: str, short_range: bool, damage: int, num_uses: int = 3):
        self.name = name
        self.short_range = short_range
        self.damage = damage
        self.num_uses = num_uses

    def attack(self, target: 'Character') -> None:
        if self.num_uses > 0:
            self.attack_sound()
            target.reduce_health(self.damage)
            self.num_uses -= 1
            if self.num_uses == 0:
                print(f"{self.name} broke! It has no more uses.")
        else:
            print(f"{self.name} is broken! Cannot attack.")

    def range_str(self) -> str:
        return "short" if self.short_range else "long"
    @abstractmethod
    def attack_sound(self) -> None:
        pass

    def __str__(self):
        return f"{self.name}(range={self.range_str()}, damage={self.damage}, num_uses={self.num_uses})"

class Sword(Weapon):
    SHORT_RANGE = True
    DAMAGE = 25
    NUM_USES = 5

    def __init__(self):
        super().__init__(self.__class__.__name__, self.SHORT_RANGE, self.DAMAGE, self.NUM_USES)

    @override
    def attack_sound(self) -> None:
        print("Swish!")
        print("Slash!")

    def __repr__(self):
        return "Sword()"

    def __str__(self):
        return f"{self.name}(range=short, damage=25, num_uses=5)"

class Axe(Weapon):
    SHORT_RANGE = True
    DAMAGE = 40
    NUM_USES = 3

    def __init__(self):
        super().__init__(self.__class__.__name__, self.SHORT_RANGE, self.DAMAGE, self.NUM_USES)

    @override
    def attack_sound(self) -> None:
        print("Chop!")

    def __repr__(self):
        return "Axe()"


class Bow(Weapon):
    SHORT_RANGE = False
    DAMAGE = 15
    NUM_USES = 10

    def __init__(self):
        super().__init__(self.__class__.__name__, self.SHORT_RANGE, self.DAMAGE, self.NUM_USES)

    @override
    def attack_sound(self) -> None:
        print("Creak...")
        print("Twang!")
        print("Thud!")

    def __repr__(self):
        return f"Bow()"


# endregion

# region ------------ Character classes ------------

class Race(StrEnum):
    """Enumeration of races."""
    ELF = "elf"
    DWARF = "dwarf"
    ORC = "orc"
    TROLL = "troll"

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


class Character(ABC):
    """Abstract class for characters."""

    INITIAL_HP = 100
    """Initial health points."""

    def __init__(self, name: str, weapon: Weapon):
        self.hp = self.INITIAL_HP
        self.name = name
        self.weapon = weapon

    def __repr__(self):
        return f"Character(name=\"{self.name}\", hp={self.hp}, weapon={self.weapon})"

    def attack(self, target: 'Character') -> None:
        if self.is_alive():
            print(f"{self.name} attacks {target.name} with {self.weapon.name}")
            self.weapon.attack(target)
        else:
            print(f"{self.name} cannot attack because they are not alive.")

    def reduce_health(self, damage: int) -> None:
        self.hp = self.hp- damage
        if self.hp < 0:
            self.hp=0
        print(f"{self.name} received {damage} points of damage -> {self.name} HP={self.hp}")
        if self.hp == 0:
            print(f"{self.name} has died!")

    def is_alive(self) -> bool:
        return self.hp > 0


    def __str__(self):
        return f"Character(name={self.name}, hp={self.hp}, weapon={self.weapon})"


class Enemy(Character):
    def __init__(self, name: str, weapon: Weapon, race: Race):
        super().__init__(name, weapon)
        self.race = race

    def __repr__(self):
        return f'Enemy(name="{self.name}", weapon={self.weapon.__repr__()}, race=Race.{self.race.name})'

    def __str__(self):
        return f"[{self.race}] {self.name}(HP={self.hp}, alive={self.is_alive()}, weapon={self.weapon.__str__()})"


class Player(Character):
    def __init__(self, name: str, weapon: Weapon):
        super().__init__(name, weapon)

    def __repr__(self):
        return f'Player(name="Dovahkiin", weapon=Sword())'

    def __str__(self):
        return f"[player] Dovahkiin(HP=100, alive=True, weapon=Sword(range=short, damage=25, num_uses=5))"


# endregion

# region ------------ Main ------------

def execute_battle(interactive=True) -> None:
    # Create characters
    player = Player('Dovahkiin', Sword())
    dwarf = Enemy('Gimli', Axe(), Race.DWARF)
    elf = Enemy('Legolas', Bow(), Race.ELF)
    orc = Enemy('Garrosh', Sword(), Race.ORC)
    troll = Enemy('Thokk', Axe(), Race.TROLL)

    # Print characters
    print(repr(player), repr(dwarf), repr(elf), repr(orc), repr(troll), '', sep='\n')
    print(player, dwarf, elf, orc, troll, '', sep='\n')

    ask_for_user_input(interactive)

    # Player attacks enemies
    print('–––––––––– Player attacks enemies ––––––––––\n')
    player.attack(dwarf)
    player.attack(elf)
    player.attack(orc)
    player.attack(troll)

    ask_for_user_input(interactive)

    # Some enemies attack player
    print('–––––––––– Some enemies attack player ––––––––––\n')
    dwarf.attack(player)
    elf.attack(player)

    ask_for_user_input(interactive)

    # Enemies attack each other
    print('–––––––––– Enemies attack each other ––––––––––\n')
    elf.attack(dwarf)
    elf.attack(dwarf)
    dwarf.attack(elf)
    orc.attack(troll)
    troll.attack(orc)

    ask_for_user_input(interactive)

    # The dwarf dies
    print('–––––––––– The dwarf dies ––––––––––\n')
    print(f'Is the dwarf {dwarf.name} still alive? {dwarf.is_alive()}\n')
    player.attack(dwarf)
    player.attack(dwarf)
    orc.attack(dwarf)
    print(f'Is the dwarf {dwarf.name} still alive? {dwarf.is_alive()}\n')
    dwarf.attack(player)

    ask_for_user_input(interactive)

    # Elf and orc trigger a mine and die
    print('–––––––––– Elf and orc trigger a mine and die ––––––––––\n')
    print('The orc and elf encountered a mine, triggering a powerful explosion!\n')
    elf.reduce_health(50)
    orc.reduce_health(50)
    print('\nCharacters status:\n')
    print(player, dwarf, elf, orc, troll, '', sep='\n')

    ask_for_user_input(interactive)

    # Final battle
    print('–––––––––– Final battle ––––––––––\n')
    print(f'{player.name} and {troll.name} engage in a fierce battle!\n')
    player.attack(troll)
    troll.attack(player)
    print(f'{player.name} surrenders and {troll.name} finishes him off!\n')
    troll.attack(player)
    print('Game over! Player lost the battle... :(')


def ask_for_user_input(interactive: bool) -> None:
    """Ask for user input to continue if interactive mode is enabled."""
    if interactive:
        input('Press Enter to continue...\n')


if __name__ == '__main__':
    execute_battle()

# endregion
