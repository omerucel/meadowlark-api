from django.test import TestCase
from django.utils import simplejson

from meadowlark.tests import factories

class UsersResourceTest(TestCase):
    def test_201_post(self):
        response = self.client.post('/api/v1/users', {
            'email' : 'test@test.com',
            'username': 'test',
            'password': '12345678'
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('user'))
        self.assertTrue(data['user'].has_key('id'))
        self.assertTrue(data['user'].has_key('username'))
        self.assertTrue(data['user'].has_key('email'))
        self.assertTrue(data.has_key('token'))

    def test_already_in_use_400_post(self):
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
    def test_401_get(self):
        response = self.client.get('/api/v1/users/self')
        self.assertEquals(401, response.status_code)

    def test_200_get(self):
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
    def test_201_post(self):
        user = factories.UserFactory()

        response = self.client.post('/api/v1/access-tokens', {
            'username': user.username,
            'password': user.username.replace('username', 'password')
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('user'))
        self.assertTrue(data.has_key('token'))
        self.assertTrue(data['token'].__len__() == 64)

class AccessTokenSelfResourceTest(TestCase):
    def test_401(self):
        # GET
        response = self.client.get('/api/v1/access-tokens/self')
        self.assertEquals(401, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/access-tokens/self')
        self.assertEquals(401, response.status_code)

    def test_200(self):
        # GET
        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/access-tokens/self', {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('user'))
        self.assertTrue(data.has_key('token'))
        self.assertTrue(data['token'].__len__() == 64)

        # DELETE
        response = self.client.get('/api/v1/access-tokens/self?access_token=%s'
            %(access_token.token))
        self.assertEquals(200, response.status_code)

class FoldersResourceTest(TestCase):
    def test_404_post(self):
        access_token = factories.AccessTokenFactory()

        response = self.client.post('/api/v1/endpoints/1/folders', {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

    def test_401_post(self):
        endpoint = factories.EndpointFactory()

        response = self.client.post('/api/v1/endpoints/%d/folders' %(endpoint.id))
        self.assertEquals(401, response.status_code)

    def test_400_post(self):
        endpoint = factories.EndpointFactory()
        access_token = factories.AccessTokenFactory()

        response = self.client.post('/api/v1/endpoints/%d/folders' %(endpoint.id), {
            'access_token': access_token.token
        })
        self.assertEquals(400, response.status_code)

    def test_201_post(self):
        endpoint = factories.EndpointFactory()
        access_token = factories.AccessTokenFactory()

        response = self.client.post('/api/v1/endpoints/%d/folders' %(endpoint.id), {
            'access_token': access_token.token,
            'name': 'test'
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('id'))

class FolderResourceTest(TestCase):
    def test_401(self):
        # GET
        response = self.client.get('/api/v1/endpoints/1/folders/123')
        self.assertEquals(401, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/endpoints/1/folders/123')
        self.assertEquals(401, response.status_code)

    def test_404(self):
        # GET
        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/endpoints/1123/folders/123', {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        endpoint = factories.EndpointFactory()
        response = self.client.get('/api/v1/endpoints/%d/folders/123' %(endpoint.id), {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/endpoints/1123/folders/123?access_token=%s'
            %(access_token.token))
        self.assertEquals(404, response.status_code)

        response = self.client.get('/api/v1/endpoints/%d/folders/123?access_token=%s'
            %(endpoint.id, access_token.token))
        self.assertEquals(404, response.status_code)

    def test_403(self):
        access_token = factories.AccessTokenFactory()
        endpoint = factories.EndpointFactory()
        endpoint2 = factories.EndpointFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)

        # GET
        response = self.client.get('/api/v1/endpoints/%d/folders/%d' %(endpoint2.id, folder.id), {
            'access_token': access_token.token
        })
        self.assertEquals(403, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/endpoints/%d/folders/%d?access_token=%s'
            %(endpoint2.id, folder.id, access_token.token))
        self.assertEquals(403, response.status_code)

    def test_200(self):
        access_token = factories.AccessTokenFactory()
        endpoint = factories.EndpointFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)

        # GET
        response = self.client.get('/api/v1/endpoints/%d/folders/%d' %(endpoint.id, folder.id), {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('name'))
        self.assertEquals(folder.name, data['name'])

        # DELETE
        response = self.client.get('/api/v1/endpoints/%d/folders/%d?access_token=%s'
            %(endpoint.id, folder.id, access_token.token))
        self.assertEquals(200, response.status_code)

class FilesResourceTest(TestCase):
    def test_401_get(self):
        response = self.client.get('/api/v1/endpoints/1/folders/123/files')
        self.assertEquals(401, response.status_code)

    def test_404_get(self):
        access_token = factories.AccessTokenFactory()

        response = self.client.get('/api/v1/endpoints/1/folders/1/files', {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        endpoint = factories.EndpointFactory()
        response = self.client.get('/api/v1/endpoints/%d/folders/123/files' %(endpoint.id), {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

    def test_403_get(self):
        access_token = factories.AccessTokenFactory()
        endpoint = factories.EndpointFactory()
        endpoint2 = factories.EndpointFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)

        response = self.client.get('/api/v1/endpoints/%d/folders/%d/files' %(endpoint2.id, folder.id), {
            'access_token': access_token.token
        })
        self.assertEquals(403, response.status_code)

    def test_200_get(self):
        endpoint = factories.EndpointFactory()
        access_token = factories.AccessTokenFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)

        response = self.client.get('/api/v1/endpoints/%d/folders/%d/files' %(endpoint.id, folder.id), {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('files'))
        self.assertTrue(data['files'].__len__() == 0)

        file1 = factories.FileFactory(folder=folder)
        file2 = factories.FileFactory(folder=folder)

        response = self.client.get('/api/v1/endpoints/%d/folders/%d/files' %(endpoint.id, folder.id), {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('files'))
        self.assertTrue(data.has_key('meta'))
        self.assertTrue(data['files'].__len__() == 2)
        self.assertTrue(data['meta']['total_record'] == 2)

    def test_401_post(self):
        endpoint = factories.EndpointFactory()
        response = self.client.post('/api/v1/endpoints/%d/folders/123/files' %(endpoint.id))
        self.assertEquals(401, response.status_code)

    def test_404_post(self):
        access_token = factories.AccessTokenFactory()
        response = self.client.post('/api/v1/endpoints/1/folders/123/files', {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        endpoint = factories.EndpointFactory()
        response = self.client.post('/api/v1/endpoints/%d/folders/123/files' %(endpoint.id), {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

    def test_201_post(self):
        endpoint = factories.EndpointFactory()
        access_token = factories.AccessTokenFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)

        response = self.client.post('/api/v1/endpoints/%d/folders/%d/files' %(endpoint.id, folder.id), {
            'access_token': access_token.token,
            'file': open('meadowlark/tests/sample_file.txt', 'rb')
        })
        data = simplejson.loads(response.content)
        self.assertEquals(201, response.status_code)
        self.assertTrue(data.has_key('id'))

    def test_403_post(self):
        endpoint = factories.EndpointFactory()
        endpoint2 = factories.EndpointFactory()
        access_token = factories.AccessTokenFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)

        response = self.client.post('/api/v1/endpoints/%d/folders/%d/files' %(endpoint2.id, folder.id), {
            'access_token': access_token.token,
            'file': open('meadowlark/tests/sample_file.txt', 'rb')
        })
        self.assertEquals(403, response.status_code)

class FileResourceTest(TestCase):
    def test_401(self):
        # GET
        response = self.client.get('/api/v1/endpoints/1/folders/1/files/1')
        self.assertEquals(401, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/endpoints/1/folders/1/files/1')
        self.assertEquals(401, response.status_code)

    def test_404(self):
        # GET
        access_token = factories.AccessTokenFactory()
        response = self.client.get('/api/v1/endpoints/1123/folders/1/files/1', {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        endpoint = factories.EndpointFactory()
        response = self.client.get('/api/v1/endpoints/%d/folders/1/files/1' %(endpoint.id), {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)
        response = self.client.get('/api/v1/endpoints/%d/folders/%d/files/1' %(endpoint.id, folder.id), {
            'access_token': access_token.token
        })
        self.assertEquals(404, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/endpoints/1123/folders/1/files/1?access_token=%s' 
            %(access_token.token))
        self.assertEquals(404, response.status_code)

        response = self.client.delete('/api/v1/endpoints/%d/folders/1/files/1?access_token=%s' 
            %(endpoint.id, access_token.token))
        self.assertEquals(404, response.status_code)

        response = self.client.delete('/api/v1/endpoints/%d/folders/%d/files/1?access_token=%s'
            %(endpoint.id, folder.id, access_token.token))
        self.assertEquals(404, response.status_code)

    def test_403(self):
        access_token = factories.AccessTokenFactory()
        endpoint = factories.EndpointFactory()
        endpoint2 = factories.EndpointFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)
        file1 = factories.FileFactory(folder=folder)

        # GET
        response = self.client.get('/api/v1/endpoints/%d/folders/%d/files/%d' %(endpoint2.id, folder.id, file1.id), {
            'access_token': access_token.token,
        })
        self.assertEquals(403, response.status_code)

        # DELETE
        response = self.client.delete('/api/v1/endpoints/%d/folders/%d/files/%d?access_token=%s' 
            %(endpoint2.id, folder.id, file1.id, access_token.token))
        self.assertEquals(403, response.status_code)

    def test_200_get(self):
        access_token = factories.AccessTokenFactory()
        endpoint = factories.EndpointFactory()
        folder = factories.FolderFactory(endpoint=endpoint, user=access_token.user)
        file1 = factories.FileFactory(folder=folder)

        # GET
        response = self.client.get('/api/v1/endpoints/%d/folders/%d/files/%d' %(endpoint.id, folder.id, file1.id), {
            'access_token': access_token.token
        })
        data = simplejson.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertTrue(data.has_key('name'))
        self.assertTrue(data.has_key('id'))
        self.assertTrue(data.has_key('size'))
        self.assertTrue(data.has_key('extension'))

        # DELETE
        response = self.client.delete('/api/v1/endpoints/%d/folders/%d/files/%d?access_token=%s' 
            %(endpoint.id, folder.id, file1.id, access_token.token))
        self.assertEquals(200, response.status_code)