from django.test import TestCase
from django.utils import simplejson

from meadowlark.tests import factories

class UsersResourceTest(TestCase):
    def test_post(self):
        response = self.client.post('/api/v1/users', {
            'email' : 'test@test.com',
            'username': 'test',
            'password': '12345678'
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('id'))

        user_one = factories.UserFactory()
        response = self.client.post('/api/v1/users', {
            'email' : user_one.email,
            'username': user_one.username,
            'password': '12345678'
        })
        data = simplejson.loads(response.content)
        self.assertEquals(400, response.status_code)
        self.assertTrue(data.has_key('validation_errors'))
        self.assertEquals('already-in-use', data['validation_errors']['email'][0])
        self.assertEquals('already-in-use', data['validation_errors']['username'][0])

class UsersSelfResourceTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/users/self')
        data = simplejson.loads(response.content)
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/users/self', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(access_token.user.id, data['id'])
        self.assertEquals(access_token.user.username, data['username'])
        self.assertEquals(access_token.user.email, data['email'])

class AccessTokensResourceTest(TestCase):
    def test_post(self):
        user = factories.UserFactory(password = 'deneme123')

        response = self.client.post('/api/v1/access-tokens', {
            'username': user.username,
            'password': 'deneme123'
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('user'))
        self.assertTrue(data.has_key('token'))
        self.assertTrue(data['token'].__len__() == 64)

class AccessTokenSelfResourceTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/access-tokens/self')
        data = simplejson.loads(response.content)
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/access-tokens/self', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('user'))
        self.assertTrue(data.has_key('token'))
        self.assertTrue(data['token'].__len__() == 64)

class FoldersResourceTest(TestCase):
    def test_post(self):
        response = self.client.post('/api/v1/folders')
        data = simplejson.loads(response.content)
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.post('/api/v1/folders', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(400, response.status_code)

        response = self.client.post('/api/v1/folders', {
            'access_token': access_token.token,
            'name': 'test'
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('id'))

class FolderResourceTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/folders/123')
        data = simplejson.loads(response.content)
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/folders/123', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(404, response.status_code)

        folder = factories.FolderFactory(user=access_token.user)
        response = self.client.get('/api/v1/folders/%d' %folder.id , {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('name'))
        self.assertEquals(folder.name, data['name'])

class FolderFilesResourceTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/folders/123/files')
        data = simplejson.loads(response.content)
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/folders/123/files', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(404, response.status_code)

        folder = factories.FolderFactory(user=access_token.user)
        response = self.client.get('/api/v1/folders/%d/files' %folder.id , {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('files'))
        self.assertTrue(data['files'].__len__() == 0)

        response = self.client.post('/api/v1/folders/%d/files' %folder.id , {
            'access_token': access_token.token,
            'file': open('meadowlark/tests/sample_file.txt', 'rb')
        })
        data = simplejson.loads(response.content)

        response = self.client.post('/api/v1/folders/%d/files' %folder.id , {
            'access_token': access_token.token,
            'file': open('meadowlark/tests/sample_file.txt', 'rb')
        })
        data = simplejson.loads(response.content)

        response = self.client.get('/api/v1/folders/%d/files' %folder.id , {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('files'))
        self.assertTrue(data.has_key('meta'))
        self.assertTrue(data['files'].__len__() == 2)
        self.assertTrue(data['meta']['total_record'] == 2)

    def test_post(self):
        response = self.client.post('/api/v1/folders/123/files')
        data = simplejson.loads(response.content)
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.post('/api/v1/folders/123/files', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(404, response.status_code)

        folder = factories.FolderFactory(user=access_token.user)
        response = self.client.post('/api/v1/folders/%d/files' %folder.id , {
            'access_token': access_token.token,
            'file': open('meadowlark/tests/sample_file.txt', 'rb')
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('id'))

class FileResourceTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/files/1')
        self.assertEquals(401, response.status_code)

        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/files/1', {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        folder = factories.FolderFactory(user=access_token.user)
        response = self.client.post('/api/v1/folders/%d/files' %folder.id , {
            'access_token': access_token.token,
            'file': open('meadowlark/tests/sample_file.txt', 'rb')
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('id'))

        file_id = data['id']

        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/files/%d' %file_id, {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('name'))
        self.assertTrue(data.has_key('id'))
        self.assertTrue(data.has_key('size'))
        self.assertTrue(data.has_key('extension'))