import unittest
import os
import tempfile
import app

class BasicTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_database(self):
        tester = os.path.exists('blog.db')
        self.assertTrue(tester)

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a blank temp database before each test."""
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        """Destroy blank temp database after each test."""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        """Login helper function."""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function."""
        return self.app.get('/logout', follow_redirects=True)

    # assert functions

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries' in rv.data

    def test_login_logout(self):
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'Successfully logged in' in rv.data
        rv = self.logout()
        assert b'Successfully logged out' in rv.data
        rv = self.login(
            app.app.config['USERNAME'] + 'x',
            app.app.config['PASSWORD']
        )
        assert b'Invalid username' in rv.data
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid password' in rv.data

    def test_posts(self):
        self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        rv = self.app.post('/posts', data=dict(
            title='First Post',
            body='This is a test'
        ), follow_redirects=True)
        assert b'No entries' not in rv.data
        assert b'First Post' in rv.data
        assert b'This is a test' in rv.data

if __name__ == '__main__':
    unittest.main()