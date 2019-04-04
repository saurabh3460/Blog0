from django.test import TestCase

# Create your tests here.
class Info:
    def show(self):
        print('')

    def __str__(self):
        return "It is Info Class"


print(Info())
