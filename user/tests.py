from rest_framework import status
from split.tests import SplitwiseTestCaseBase
from random import randint

from user.models import Group
# Create your tests here.

class UserAppTestCase(SplitwiseTestCaseBase):
    def setUp(self):
        super().setUp()  
    
    def test_user_CRUD(self):
        name = self.create_random_text()
        payload = {'Name': name}
        response = self.client.post(self.user_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.user_URL + f'{name}/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ["User Deletion Not Allowed"])

    def test_group_CRUD(self):
        # test group creation, and users creation with it
        names, title = [], self.create_random_text()
        for _ in range(randint(2, 10)):
            names.append(self.create_random_text())
        payload = {
            'Users': names,
            'Title': title
        }

        
        response = self.create_group(names=names, title=title)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # All non-existent users created
        for name in names:
            response = self.client.get(f'{self.user_URL}{name}/')
            self.assertEqual(response.status_code, 200)
        
        
        # Cant delete group if any payment not settled
        group = Group.objects.get(Title=title)
        for u1 in names:
            for u2 in names:
                if u1 == u2:
                    continue
                sorted_users = sorted([u1, u2])
                group.PayMap[f'{sorted_users[0]}__{sorted_users[1]}'] = self.create_random_number()
        group.save()
        
        response = self.client.delete(self.group_URL+f'{title}/')
        self.assertEqual(response.json(), ['Group cant be deleted as payment not settled'])
    
        # cant remove user if its payment not settled
        popped = [names.pop(0)]
        payload = {
            'Users': names
        }

        response = self.client.patch(f'{self.group_URL}{title}/', payload, format='json')
        self.assertEqual(response.json(), [f'Users {str(popped)} cant be deleted as payment not settled'])

        payload = {
            'Users': names,
            'Title': title
        }
        response = self.client.patch(f'{self.group_URL}{title}/', payload, format='json')
        self.assertEqual(response.json(), ['Cant update title of Group'])
        # get success




