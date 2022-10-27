from django.test import TestCase
from user.models import User, Group
from split.models import Expense

# Create your tests here.
import random
import string
from rest_framework.test import APIClient
from random import randint, choice


class SplitwiseTestCaseBase(TestCase):
    def create_random_text(self, length=8):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def create_random_number(self, length=8):
        return "".join(random.choices(string.digits[1:], k=length))

    def create_user(self, name=None):
        if name is None:
            name = self.create_random_text()

        User.objects.create(Name=name)

    def create_group(self, title=None, names=None):
        if not names:
            names = []
            for _ in range(randint(2, 10)):
                names.append(self.create_random_text())
        if not title:
            title = self.create_random_text()

        payload = {"Users": names, "Title": title}

        return self.client.post(self.group_URL, payload, format="json")

    def setUp(self):
        self.user_URL = "/user/"
        self.group_URL = "/group/"
        self.split_URL = "/split/"
        self.client = APIClient()


class SplitAppTestCase(SplitwiseTestCaseBase):
    def setUp(self):
        super().setUp()
        self.title = "match1"
        self.users = ["ronaldo", "messi", "kaka"]
        self.create_group(title=self.title, names=self.users)
    
    def cross_check_global_groups(self):
        correct_paymap = {}
        for u1 in self.users:
            for u2 in self.users:
                if u1 == u2:
                    continue
                s_names = sorted([u1, u2])
                key = s_names[0] + '__' + s_names[1]
                correct_paymap[key] = 0
        
        
        for expense in Expense.objects.all():
            payer = expense.Details['Payer']
            for borrower in expense.Details:
                if borrower not in [payer,'Payer']:
                    key = '__'.join(sorted([payer, borrower]))
                    if payer < borrower:
                        correct_paymap[key] += expense.Details[borrower]
                    else:
                        correct_paymap[key] -= expense.Details[borrower]
        group = Group.objects.get(Title='match1')
        self.assertEqual(correct_paymap, group.PayMap)
        for user in self.users:
            obj = User.objects.get(Name=user)
            for bal in obj.Balance:
                self.assertEqual(correct_paymap[bal], obj.Balance[bal])


    def test_create_expense(self):
        payload = {
            "Group": self.title,
            "Title": "dinner",
            "Amount": 99,
            "Details": {"Payer": "ronaldo", "ronaldo": 33, "messi": 33, "kaka": 33},
        }
        response = self.client.post(self.split_URL, payload, format="json")

        self.assertEqual(response.status_code, 201)

    def test_non_existent_user(self):
        payload = {
            "Group": self.title,
            "Title": "dinner",
            "Amount": 99,
            "Details": {"Payer": "ronaldo", "ronaldo": 33, "messi": 33, "modric": 33},
        }
        response = self.client.post(self.split_URL, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"modric": ["User modric Does not exist"]})

    def test_incorrect_sum(self):
        payload = {
            "Group": self.title,
            "Title": "dinner",
            "Amount": 100,
            "Details": {"Payer": "ronaldo", "ronaldo": 33, "messi": 33, "kaka": 33},
        }
        response = self.client.post(self.split_URL, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"details": ["Total does not sum up"]})

    def test_randomize_creation(self):
        # randomize for multiple group creation
        # randomize for uncertain number of users
        # check for correctness of the values
        for _ in range(randint(3, 10)):
            pop = randint(0,2)
            names = list(self.users)
            if pop:
                names.pop(pop)

            amount = len(names) * randint(1, 11)
            details = {'Payer': choice(names)}

            # Randomize further to have unequal distribution
            for each in names:
                details[each] = amount // len(names)

            payload = {
            "Group": self.title,
            "Title": self.create_random_text(),
            "Amount": amount,
            "Details": details,
            }
            self.client.post(self.split_URL, payload, format="json")
        self.cross_check_global_groups()
    

