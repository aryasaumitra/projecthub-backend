from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Project, Task
import datetime


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.token_url = '/api/token/'
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "is_staff":True
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User registered successfully.", response.data["message"])

    def test_user_login(self):
        # Register the user
        self.client.post(self.register_url, self.user_data)
        # Login to get a token
        response = self.client.post(self.token_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword123",is_staff=True)
        self.token_url = '/api/token/'
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        self.project_data = {
            "name": "Test Project",
            "description": "Test project description",
            "start_date": datetime.date.today(),
            "end_date": datetime.date.today() + datetime.timedelta(days=10),
        }
        

    def test_create_project(self):
        userResponse = self.client.post(self.token_url,self.user_data)
        response = self.client.post('/api/projects/', self.project_data,headers={'Authorization': "Bearer "+userResponse.data['access']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, self.project_data["name"])

    def test_list_projects(self):
        Project.objects.create(**self.project_data)
        userResponse = self.client.post(self.token_url,self.user_data)
        response = self.client.get('/api/projects/',headers={'Authorization': "Bearer "+userResponse.data['access']})
        # self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_update_project(self):
        project = Project.objects.create(**self.project_data)
        updated_data = {"name": "Updated Project"}
        userResponse = self.client.post(self.token_url,self.user_data)
        response = self.client.patch(f'/api/projects/{project.id}/', updated_data,headers={'Authorization': "Bearer "+userResponse.data['access']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.name, "Updated Project")

    def test_delete_project(self):
        project = Project.objects.create(**self.project_data)
        userResponse = self.client.post(self.token_url,self.user_data)
        response = self.client.delete(f'/api/projects/{project.id}/',headers={'Authorization': "Bearer "+userResponse.data['access']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword123",is_staff=True)
        self.token_url = '/api/token/'
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        self.project = Project.objects.create(
            name="Test Project",
            description="Test project description",
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=10),
        )
        self.task_data = {
            "title": "Test Task",
            "description": "Test task description",
            "status": "Pending",
            "project": self.project.id,
            "assigned_to": self.user.id,
            "due_date": datetime.date.today() + datetime.timedelta(days=5),
        }
        

    def test_create_task(self):
        userResponse = self.client.post(self.token_url,self.user_data)
        response = self.client.post('/api/tasks/', self.task_data,headers={'Authorization': "Bearer "+userResponse.data['access']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, self.task_data["title"])

    # def test_list_tasks(self):
    #     userResponse = self.client.post(self.token_url,self.user_data)
    #     Task.objects.create(**self.task_data)
    #     response = self.client.get('/api/tasks/',headers={'Authorization': "Bearer "+userResponse.data['access']})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(len(response.data["results"]), 1)

#     def test_update_task(self):
#         task = Task.objects.create(**self.task_data)
#         updated_data = {"status": "Completed"}
#         response = self.client.patch(f'/api/tasks/{task.id}/', updated_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         task.refresh_from_db()
#         self.assertEqual(task.status, "Completed")

#     def test_delete_task(self):
#         task = Task.objects.create(**self.task_data)
#         response = self.client.delete(f'/api/tasks/{task.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Task.objects.count(), 0)

# class UserTaskTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username="user", password="user123")
#         self.project = Project.objects.create(
#             name="User Project",
#             description="User project description",
#             start_date=datetime.date.today(),
#             end_date=datetime.date.today() + datetime.timedelta(days=10),
#         )
#         self.task = Task.objects.create(
#             title="User Task",
#             description="User task description",
#             status="Pending",
#             project=self.project,
#             assigned_to=self.user,
#             due_date=datetime.date.today() + datetime.timedelta(days=5),
#         )
#         self.client.login(username="user", password="user123")

#     def test_user_can_view_assigned_tasks(self):
#         response = self.client.get('/api/tasks/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data["results"]), 1)
#         self.assertEqual(response.data["results"][0]["title"], self.task.title)

#     def test_user_can_update_task_status(self):
#         updated_data = {"status": "In Progress"}
#         response = self.client.patch(f'/api/tasks/{self.task.id}/', updated_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.task.refresh_from_db()
#         self.assertEqual(self.task.status, "In Progress")