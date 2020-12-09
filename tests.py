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

        self.new_movie = {
            "title": "new movie",
            "realease_date": "19/12/2020"
        }

        self.new_actor = {
            "name": "Carl",
            "age": "50",
            "gender": "male"
        }

        self.headers_assistant = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5UNnVZOGQ4TG5yaTZYSGkzaGlmVCJ9.eyJpc3MiOiJodHRwczovL2hlaWxhZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjYmI4NTcwMjU3MGMwMDZlOWI3YjJhIiwiYXVkIjoiTW92aWVzIiwiaWF0IjoxNjA3NTIwNzMzLCJleHAiOjE2MDc2MDcxMzMsImF6cCI6IjZHZ2tiZlY0NUtWaE81a2M2anEzT3Q3aXR2cFhXOThqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.a49Xt1evmluncsXatltBwBoPROzqEndOx_3yf7EEPsuourjlHUaLnSufTs-hbUrXTyGj9OXYeDg5XGyG47UZSrPu2y4Nxea2Pjg3tj_ZaC71JWef81ay_jgfkctJUatHysANTM5syuz9_WMjyE3lKe4feexgJmCeZ7homgrpj_p1P7V_nzV3w2-vq407r1FvrB2frAn_SCErDBrF2sXp-ytR1ZEYStN22fYTpPwDusMgLUiRdJuUhTPB4R1FWyRO91ts0x77xQsXiFC2l9VBm-_kr2bM61IXO8HzwAgbKfVnOfDnkuvKG5I4Rww8zhhZ4BId-7m4wo6yD-cyefG1Qg'
        }
        self.headers_director = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5UNnVZOGQ4TG5yaTZYSGkzaGlmVCJ9.eyJpc3MiOiJodHRwczovL2hlaWxhZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjYmQyMDczODUxOGYwMDZmMmFmODM2IiwiYXVkIjoiTW92aWVzIiwiaWF0IjoxNjA3NTIxMTAzLCJleHAiOjE2MDc2MDc1MDMsImF6cCI6IjZHZ2tiZlY0NUtWaE81a2M2anEzT3Q3aXR2cFhXOThqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.enhvEH_8rNrTyYZIsQnzQ0hL1aL5Zs3_9eM0N6_9gmo_3t7hWQuBg_nl8Ot07Nbjsf_NgSh2xHIiM4AHwOGnQpTBNgR0a0hDXM-_p8J86NZyGMDK7CYbvFlrm7TcU1R50egbxrnlPsr_-HhJG6wsxLF9Z5NXTrAX8f-tiGp7AQd_QtA8pvIH9NUx0UjI_RljboYIz8-8FXvS6tGtwK_oA1vSyq_K_T7GhrxAN9l_Bff7ivS_xfsGl7OmbgIAc9hYxpJtoJolPQQPvbz7_EfkOi7gp5UxVY9H9WIW88rm6F3rOLW-BzupDpr6UzBzk6_VjOl1LnvzXW2kUVh42F2BNQ'
        }
        self.headers_executive = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5UNnVZOGQ4TG5yaTZYSGkzaGlmVCJ9.eyJpc3MiOiJodHRwczovL2hlaWxhZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjYmQyODAwMjU3MGMwMDZlOWI3YzBlIiwiYXVkIjoiTW92aWVzIiwiaWF0IjoxNjA3NTIxNDY1LCJleHAiOjE2MDc2MDc4NjUsImF6cCI6IjZHZ2tiZlY0NUtWaE81a2M2anEzT3Q3aXR2cFhXOThqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.CHwumlSHwwU_DV-qymfDCgE57c9L2Rq2XchSL8b28Nxz2xbBoX8hFi3dyvbY5LzZiOAiqcsXVyAfsa8TsgrCi7hfnHsUAawOt9jfW6tqe6zxRaoFIQhV0s7OG_oO6JqfUuoBhhHJk2on9-ikW2EY2Jkf9FvZH6jEVm_Q5fn7DZaxGHi6TxARjmR1R_PKJP3-fYQyKt8zipZh0QL7bRFerHPvy41QtFmxff2QkJ2YspKjo_C_ZIYf0Flb47Xq9QC9bMMmiR_mP3nibBRyozRMKUlrkMzz0iNHfGD87FIJ7tEEC_muQZmUp2pOQSW9AlXU7q0PjP8xwiuUb35JqULCAA'
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Testing GET methods

    def test_get_movies(self):
        """Testing GET movies"""

        # assert assistant can acces
        res1 = self.client().get('/movies', headers=self.headers_assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 200)

        # assert director can acces
        res2 = self.client().get('/movies', headers=self.headers_director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can acces
        res3 = self.client().get('/movies', headers=self.headers_executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_get_actors(self):
        """Testing GET actors"""

        # assert assistant can acces
        res1 = self.client().get('/actors', headers=self.headers_assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 200)

        # assert director can acces
        res2 = self.client().get('/actors', headers=self.headers_director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can acces
        res3 = self.client().get('/actors', headers=self.headers_executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)
        # self.assertTrue(data['totalQuestions'])
        # self.assertTrue(len(data['questions']))

    # Testing POST methods

    def test_post_movies(self):
        """Testing POST movies"""

        # assert assistant cannot post
        res1 = self.client().post('/movies', headers=self.headers_assistant, json=self.new_movie)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director cannot post
        res2 = self.client().post('/movies', headers=self.headers_director, json=self.new_movie)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 401)

        # assert executive can post
        res3 = self.client().post('/movies', headers=self.headers_executive, json=self.new_movie)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_post_actors(self):
        """Testing POST actors"""

        # assert assistant cannot post
        res1 = self.client().post('/actors', headers=self.headers_assistant, json=self.new_actor)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can post
        res2 = self.client().post('/actors', headers=self.headers_director, json=self.new_actor)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can post
        res3 = self.client().post('/actors', headers=self.headers_executive, json=self.new_actor)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    # Testing PATCH methods

    def test_patch_movies(self):
        """Testing PATCH movies"""

        # assert assistant cannot patch
        res1 = self.client().patch(
            '/movies/1', headers=self.headers_assistant, json=self.new_movie)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can patch
        res2 = self.client().patch(
            '/movies/1', headers=self.headers_director, json=self.new_movie)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can patch
        res3 = self.client().patch(
            '/movies/1', headers=self.headers_executive, json=self.new_movie)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_patch_actors(self):
        """Testing PATCH actors"""

        # assert assistant cannot patch
        res1 = self.client().patch(
            '/actors/1', headers=self.headers_assistant, json=self.new_actor)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can patch
        res2 = self.client().patch(
            '/actors/1', headers=self.headers_director, json=self.new_actor)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can patch
        res3 = self.client().patch(
            '/actors/1', headers=self.headers_executive, json=self.new_actor)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    # Testing DELETE methods

        # Please make sure that record exists first, or change the number to any other existing one, or insert it:
        # insert into movies (id, title, release_date) values (1, 'random movie', '2020-12-19');
        # insert into actors (id, name, age, gender) values (1, 'random person', 'male');

    def test_delete_movies(self):
        """Testing DELETE movies"""

        # assert assistant cannot delete
        res1 = self.client().delete(
            '/movies/1', headers=self.headers_assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director cannot delete
        res2 = self.client().delete(
            '/movies/1', headers=self.headers_director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 401)

        # assert executive can delete
        res3 = self.client().delete(
            '/movies/1', headers=self.headers_executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)

    def test_delete_actors(self):
        """Testing DELETE actors"""

        # assert assistant cannot delete
        res1 = self.client().delete(
            '/actors/1', headers=self.headers_assistant)
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 401)

        # assert director can delete
        res2 = self.client().delete(
            '/actors/1', headers=self.headers_director)
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)

        # assert executive can delete
        res3 = self.client().delete(
            '/actors/1', headers=self.headers_executive)
        data3 = json.loads(res3.data)
        self.assertEqual(res3.status_code, 200)


if __name__ == "__main__":
    unittest.main()
