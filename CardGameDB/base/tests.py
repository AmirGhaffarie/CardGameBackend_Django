from django.test import TestCase
from base.models import Rarity
# Create your tests here.

class Test_Rarity(TestCase):
    def test_making_rarity(self):
        rar = Rarity(name ="Mamad",chance=150)
        self.assertEqual(rar.name,"Mamad")
        self.assertEqual(rar.chance,150)
        self.assertEqual(rar.emoji,'NoEmoji')
