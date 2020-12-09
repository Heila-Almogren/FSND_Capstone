import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *


class CATestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.movie = {
            "title": "new movie",
            "realease_date": "19/12/2020"
        }

        self.actor = {
            "name": "Carl",
            "age": "50",
            "gender": "male"
        }

        # RUN: source setup.sh
        self.assistant = {
            'Authorization': 'Bearer ' + os.environ.get('ASSISTANT')
        }
        self.director = {
            'Authorization': 'Bearer ' + os.environ.get('DIRECTOR')
        }
        self.executive = {
            'Authorization': 'Bearer ' + os.environ.get('PRODUCER')
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Testing GET methods

    def test_get_movies(self):
        """Testing GET movies"""

        # assert assistant can acces
        res1 = self.client().get('/movies', headers=self.assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 200)

        # assert director can acces
        res2 = self.client().get('/movies', headers=self.director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can acces
        res3 = self.client().get('/movies', headers=self.executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_get_actors(self):
        """Testing GET actors"""

        # assert assistant can acces
        res1 = self.client().get('/actors', headers=self.assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 200)

        # assert director can acces
        res2 = self.client().get('/actors', headers=self.director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can acces
        res3 = self.client().get('/actors', headers=self.executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)
        # self.assertTrue(data['totalQuestions'])
        # self.assertTrue(len(data['questions']))

    # Testing POST methods

    def test_post_movies(self):
        """Testing POST movies"""

        # assert assistant cannot post
        res1 = self.client().post('/movies',
                                  headers=self.assistant, json=self.movie)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director cannot post
        res2 = self.client().post('/movies',
                                  headers=self.director, json=self.movie)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 401)

        # assert executive can post
        res3 = self.client().post('/movies',
                                  headers=self.executive, json=self.movie)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_post_actors(self):
        """Testing POST actors"""

        # assert assistant cannot post
        res1 = self.client().post('/actors',
                                  headers=self.assistant, json=self.actor)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can post
        res2 = self.client().post('/actors',
                                  headers=self.director, json=self.actor)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can post
        res3 = self.client().post('/actors',
                                  headers=self.executive, json=self.actor)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    # Testing PATCH methods

    def test_patch_movies(self):
        """Testing PATCH movies"""

        # assert assistant cannot patch
        res1 = self.client().patch(
            '/movies/1', headers=self.assistant, json=self.movie)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can patch
        res2 = self.client().patch(
            '/movies/1', headers=self.director, json=self.movie)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can patch
        res3 = self.client().patch(
            '/movies/1', headers=self.executive, json=self.movie)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_patch_actors(self):
        """Testing PATCH actors"""

        # assert assistant cannot patch
        res1 = self.client().patch(
            '/actors/1', headers=self.assistant, json=self.actor)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can patch
        res2 = self.client().patch(
            '/actors/1', headers=self.director, json=self.actor)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can patch
        res3 = self.client().patch(
            '/actors/1', headers=self.executive, json=self.actor)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    # Testing DELETE methods

        # Please make sure that record exists first,
        # or change the number to any other existing one, or insert it:

        # insert into movies
        # (id, title, release_date)
        # values (1, 'random movie', '2020-12-19');

        # insert into actors
        # (id, name, age, gender)
        # values (1, 'random person', 'male');

    def test_delete_movies(self):
        """Testing DELETE movies"""

        # assert assistant cannot delete
        res1 = self.client().delete(
            '/movies/1', headers=self.assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director cannot delete
        res2 = self.client().delete(
            '/movies/1', headers=self.director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 401)

        # assert executive can delete
        res3 = self.client().delete(
            '/movies/1', headers=self.executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_delete_actors(self):
        """Testing DELETE actors"""

        # assert assistant cannot delete
        res1 = self.client().delete(
            '/actors/1', headers=self.assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can delete
        res2 = self.client().delete(
            '/actors/1', headers=self.director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can delete
        res3 = self.client().delete(
            '/actors/1', headers=self.executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)


if __name__ == "__main__":
    unittest.main()
