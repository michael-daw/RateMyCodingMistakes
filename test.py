import os
import re
import inspect
import warnings
import tempfile
import importlib
import rango.models
from django.db import models
from django.test import TestCase
from django.conf import settings
from populate_rango import populate
from django.urls import reverse, resolve
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class TestDatabase(TestCase):

    def setUp(self):
        pass
    
    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
    
    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist, and does it have a default configuration?
        """
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable.{FAILURE_FOOTER}")
    
    def test_gitignore_for_database(self):
        """
        If you are using a Git repository and have set up a .gitignore, checks to see whether the database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        
        if git_base_dir.startswith('fatal'):
            warnings.warn("You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')
            
            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn("You don't appear to have a .gitignore file in place in your repository.")

class ModelTests(TestCase):

    def setUp(self):
        category_py = Category.objects.get_or_create(name='Python')
        Category.objects.get_or_create(name='Django')
        
        user = User.objects.create_user(username='test_user')
        
        Post.objects.get_or_create(category=category_py[0],
                                   title='post1',
                                   body='body2',
                                   op=user)

    def test_page_model(self):
        """
        Runs some tests on the Page model.
        Do the correct attributes exist?
        """
        category_py = Category.objects.get(name='Python')
        user = User.objects.create_user(username='test_user')
        post = Post.objects.get(title='post1')
        self.assertEqual(post.body, 'body2', f"{FAILURE_HEADER}Tests on the Post model failed.{FAILURE_FOOTER}")
        self.assertEqual(post.op, user, f"{FAILURE_HEADER}Tests on the Post model failed.{FAILURE_FOOTER}")
        
    def test_str_method(self):
        """
        Tests to see if the correct __str__() method has been implemented for each model.
        """
        category_py = Category.objects.get(name='Python')
        post = Post.objects.get(title='post1')
        
        self.assertEqual(str(category_py), 'Python', f"{FAILURE_HEADER}The __str__() method in the Category class has not been implemented.{FAILURE_FOOTER}")
        self.assertEqual(str(page), 'post1', f"{FAILURE_HEADER}The __str__() method in the Post class has not been implemented.{FAILURE_FOOTER}")

class LoginTests(TestCase):
    """
    A series of tests for checking the login functionality of Rango.
    """
    def test_login_url_exists(self):
        """
        Checks to see if the new login view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('main:login')
        except:
            pass
        
        self.assertEqual(url, '/main/login/', f"{FAILURE_HEADER}Have you created the main:login URL mapping correctly?{FAILURE_FOOTER}")

    def test_login_functionality(self):
        """
        Tests the login functionality.
        """
        user_object = create_user_object()

        response = self.client.post(reverse('main:login'), {'username': 'testuser', 'password': 'testabc123'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('rango:index'), f"{FAILURE_HEADER}We were not redirected to the Rate My Coding Mistakes homepage after logging in.{FAILURE_FOOTER}")

class RestrictedAccessTests(TestCase):
    """
    Some tests to test the restricted access view. Can users who are not logged in see it?
    """
    def test_restricted_url_exists(self):
        """
        Checks to see if the new restricted view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('main:account')
        except:
            pass
        
        self.assertEqual(url, '/main/account/', f"{FAILURE_HEADER}Have you created the rango:restricted URL mapping correctly?{FAILURE_FOOTER}")
    
    def test_bad_request(self):
        """
        Tries to access the restricted view when not logged in.
        This should redirect the user to the login page.
        """
        response = self.client.get(reverse('main:account'))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}We tried to access the restricted view when not logged in. We expected to be redirected, but were not.{FAILURE_FOOTER}")
        self.assertTrue(response.url.startswith(reverse('main:login')), f"{FAILURE_HEADER}We tried to access the restricted view when not logged in, and were expecting to be redirected to the login view. But we were not!{FAILURE_FOOTER}")
    
    def test_good_request(self):
        """
        Attempts to access the restricted view when logged in.
        This should not redirect. We cannot test the content here. Only links in base.html can be checked -- we do this in the exercise tests.
        """
        create_user_object()
        self.client.login(username='testuser', password='testabc123')

        response = self.client.get(reverse('main:account'))
        self.assertTrue(response.status_code, 200)


class LogoutTests(TestCase):
    """
    A few tests to check the functionality of logging out. Does it work? Does it actually log you out?
    """
    def test_bad_request(self):
        """
        Attepts to log out a user who is not logged in.
        This should according to the book redirect you to the login page.
        """
        response = self.client.get(reverse('main:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('main:login'))
    
    def test_good_request(self):
        """
        Attempts to log out a user who IS logged in.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Please check your login() view and try again.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homepage.
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen. Please check your logout() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('main:home'), f"{FAILURE_HEADER}When logging out a user, the book states you should then redirect them to the homepage. This did not happen; please check your logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out! Please check yout logout() view.{FAILURE_FOOTER}")
