import io
import sys
import unittest
from unittest.mock import patch, Mock, call, MagicMock

from python_uax.classes import Sword, Axe, Bow, Character, Player, Enemy, Race, execute_battle


class WeaponsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # Create weapons
        self.sword = Sword()
        self.axe = Axe()
        self.bow = Bow()

    def test_str(self):
        self.assertEqual('Sword(range=short, damage=25, num_uses=5)', str(self.sword))
        self.assertEqual('Axe(range=short, damage=40, num_uses=3)', str(self.axe))
        self.assertEqual('Bow(range=long, damage=15, num_uses=10)', str(self.bow))

    def test_repr(self):
        self.assertEqual('Sword()', repr(self.sword))
        self.assertEqual('Axe()', repr(self.axe))
        self.assertEqual('Bow()', repr(self.bow))

    @patch('builtins.print')  # mock the print function
    def test_attack_sound(self, mock_print: Mock):
        self.sword.attack_sound()
        mock_print.assert_has_calls([call('Swish!'), call('Slash!')])
        self.axe.attack_sound()
        mock_print.assert_has_calls([call('Chop!')])
        self.bow.attack_sound()
        mock_print.assert_has_calls([call('Creak...'), call('Twang!'), call('Thud!')])

    @patch('builtins.print')  # mock the print function
    def test_attack(self, mock_print: Mock):
        # Create a mock character
        mock_character: Character = MagicMock(spec=Character)
        # Instead of actually reducing the health, the damage is printed
        mock_character.reduce_health = lambda damage: print(f'Damage: {damage}')

        broken_uses = 2

        # Sword
        sword_uses = 5
        sword_damage = 25
        for i in range(sword_uses + broken_uses):
            self.sword.attack(mock_character)
        mock_print.assert_has_calls([call('Swish!'), call('Slash!'), call(f'Damage: {sword_damage}')] * sword_uses
                                    + [call('Sword broke! It has no more uses.')]
                                    + [call('Sword is broken! Cannot attack.')] * broken_uses)

        # Axe
        axe_uses = 3
        axe_damage = 40
        for i in range(axe_uses + broken_uses):
            self.axe.attack(mock_character)
        mock_print.assert_has_calls([call('Chop!'), call(f'Damage: {axe_damage}')] * axe_uses
                                    + [call('Axe broke! It has no more uses.')]
                                    + [call('Axe is broken! Cannot attack.')] * broken_uses)

        # Bow
        bow_uses = 10
        bow_damage = 15
        for i in range(bow_uses + broken_uses):
            self.bow.attack(mock_character)
        mock_print.assert_has_calls([call('Creak...'), call('Twang!'), call('Thud!'), call(f'Damage: {bow_damage}')] * bow_uses
                                    + [call('Bow broke! It has no more uses.')]
                                    + [call('Bow is broken! Cannot attack.')] * broken_uses)


class CharactersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # Create characters
        self.player = Player('Dovahkiin', Sword())
        self.dwarf = Enemy('Gimli', Axe(), Race.DWARF)
        self.elf = Enemy('Legolas', Bow(), Race.ELF)
        self.orc = Enemy('Garrosh', Sword(), Race.ORC)
        self.troll = Enemy('Thokk', Axe(), Race.TROLL)

    def test_str(self):
        self.assertEqual('[player] Dovahkiin(HP=100, alive=True, weapon=Sword(range=short, damage=25, num_uses=5))', str(self.player))
        self.assertEqual('[dwarf] Gimli(HP=100, alive=True, weapon=Axe(range=short, damage=40, num_uses=3))', str(self.dwarf))
        self.assertEqual('[elf] Legolas(HP=100, alive=True, weapon=Bow(range=long, damage=15, num_uses=10))', str(self.elf))
        self.assertEqual('[orc] Garrosh(HP=100, alive=True, weapon=Sword(range=short, damage=25, num_uses=5))', str(self.orc))
        self.assertEqual('[troll] Thokk(HP=100, alive=True, weapon=Axe(range=short, damage=40, num_uses=3))', str(self.troll))

    def test_repr(self):
        self.assertEqual('Player(name="Dovahkiin", weapon=Sword())', repr(self.player))
        self.assertEqual('Enemy(name="Gimli", weapon=Axe(), race=Race.DWARF)', repr(self.dwarf))
        self.assertEqual('Enemy(name="Legolas", weapon=Bow(), race=Race.ELF)', repr(self.elf))
        self.assertEqual('Enemy(name="Garrosh", weapon=Sword(), race=Race.ORC)', repr(self.orc))
        self.assertEqual('Enemy(name="Thokk", weapon=Axe(), race=Race.TROLL)', repr(self.troll))

    def test_is_alive(self):
        self.assertTrue(self.player.is_alive())
        self.assertTrue(self.dwarf.is_alive())

        self.player.hp = 0
        self.assertFalse(self.player.is_alive())
        self.dwarf.hp = 0
        self.assertFalse(self.dwarf.is_alive())

    @patch('builtins.print')  # mock the print function
    def test_reduce_health(self, mock_print: Mock):
        self.player.reduce_health(25)
        self.assertEqual(75, self.player.hp)
        mock_print.assert_called_with('Dovahkiin received 25 points of damage -> Dovahkiin HP=75')
        self.player.reduce_health(50)
        self.assertEqual(25, self.player.hp)
        mock_print.assert_called_with('Dovahkiin received 50 points of damage -> Dovahkiin HP=25')
        self.player.reduce_health(25)
        self.assertEqual(0, self.player.hp)
        mock_print.assert_has_calls([call('Dovahkiin received 25 points of damage -> Dovahkiin HP=0'),
                                     call('Dovahkiin has died!')])

        self.dwarf.reduce_health(75)
        self.assertEqual(25, self.dwarf.hp)
        mock_print.assert_called_with('Gimli received 75 points of damage -> Gimli HP=25')
        self.dwarf.reduce_health(26)
        self.assertEqual(0, self.dwarf.hp)
        mock_print.assert_has_calls([call('Gimli received 26 points of damage -> Gimli HP=0'),
                                     call('Gimli has died!')])

    @patch('builtins.print')  # mock the print function
    def test_attack(self, mock_print: Mock):
        # Player and dwarf attack each other
        self.player.attack(self.dwarf)
        self.assertEqual(75, self.dwarf.hp)
        mock_print.assert_has_calls([call('Dovahkiin attacks Gimli with Sword'),
                                     call('Swish!'), call('Slash!'),
                                     call('Gimli received 25 points of damage -> Gimli HP=75')])

        self.dwarf.attack(self.player)
        self.assertEqual(60, self.player.hp)
        mock_print.assert_has_calls([call('Gimli attacks Dovahkiin with Axe'),
                                     call('Chop!'),
                                     call('Dovahkiin received 40 points of damage -> Dovahkiin HP=60'),
                                     call()])

        self.player.attack(self.dwarf)
        self.assertEqual(50, self.dwarf.hp)
        mock_print.assert_has_calls([call('Dovahkiin attacks Gimli with Sword'),
                                     call('Swish!'), call('Slash!'),
                                     call('Gimli received 25 points of damage -> Gimli HP=50'),
                                     call()])

        self.player.attack(self.dwarf)
        self.assertEqual(25, self.dwarf.hp)
        mock_print.assert_has_calls([call('Dovahkiin attacks Gimli with Sword'),
                                     call('Swish!'), call('Slash!'),
                                     call('Gimli received 25 points of damage -> Gimli HP=25'),
                                     call()])

        self.player.attack(self.dwarf)
        self.assertEqual(0, self.dwarf.hp)
        mock_print.assert_has_calls([call('Dovahkiin attacks Gimli with Sword'),
                                     call('Swish!'), call('Slash!'),
                                     call('Gimli received 25 points of damage -> Gimli HP=0'),
                                     call('Gimli has died!'),
                                     call()])

        # The dwarf is dead, so it cannot be attacked
        # The player's weapon doesn't break, because attacking a dead characters doesn't consume uses
        self.player.attack(self.dwarf)
        self.assertEqual(0, self.dwarf.hp)
        mock_print.assert_called_with('Gimli is dead! Cannot attack.\n')

        # The dwarf is dead, so it cannot attack
        self.dwarf.attack(self.player)
        self.assertEqual(60, self.player.hp)
        mock_print.assert_called_with('Gimli is dead! Cannot attack.\n')

        # The player attacks other enemy and its weapon breaks because only has 1 use left
        self.player.attack(self.elf)
        self.assertEqual(75, self.elf.hp)
        mock_print.assert_has_calls([call('Dovahkiin attacks Legolas with Sword'),
                                     call('Swish!'), call('Slash!'),
                                     call('Legolas received 25 points of damage -> Legolas HP=75'),
                                     call('Sword broke! It has no more uses.'),
                                     call()])

        # The player attacks with a broken weapon, so the elf's health doesn't change
        self.player.attack(self.elf)
        self.assertEqual(75, self.elf.hp)
        mock_print.assert_has_calls([call('Dovahkiin attacks Legolas with Sword'),
                                     call('Sword is broken! Cannot attack.')])

        # Player is attacked and dies
        self.elf.attack(self.player)
        self.assertEqual(45, self.player.hp)
        mock_print.assert_has_calls([call('Legolas attacks Dovahkiin with Bow'),
                                     call('Creak...'), call('Twang!'), call('Thud!'),
                                     call('Dovahkiin received 15 points of damage -> Dovahkiin HP=45'),
                                     call()])

        self.orc.attack(self.player)
        self.assertEqual(20, self.player.hp)
        mock_print.assert_has_calls([call('Garrosh attacks Dovahkiin with Sword'),
                                     call('Swish!'), call('Slash!'),
                                     call('Dovahkiin received 25 points of damage -> Dovahkiin HP=20'),
                                     call()])

        self.troll.attack(self.player)
        self.assertEqual(0, self.player.hp)
        mock_print.assert_has_calls([call('Thokk attacks Dovahkiin with Axe'),
                                     call('Chop!'),
                                     call('Dovahkiin received 40 points of damage -> Dovahkiin HP=0'),
                                     call('Dovahkiin has died!'),
                                     call()])


class BattleTestCase(unittest.TestCase):
    # Save the original stdout before each test
    def setUp(self) -> None:
        self.original_stdout = sys.stdout

    # Always restore the original stdout after each test
    def tearDown(self) -> None:
        sys.stdout = self.original_stdout

    def test_battle(self):
        # Redirect stdout to a buffer
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the battle in non-interactive mode (no user input is required)
        execute_battle(interactive=False)

        # Assert that the printed content is as expected
        with open('expected_battle_output.txt', 'r') as file:
            expected_output = file.read()
            self.assertEqual(expected_output, captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
