from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(title="My Task", description="Details")
        self.assertEqual(task.title, "My Task")
        self.assertEqual(task.description, "Details")
        self.assertFalse(task.completed)  # Check default
        self.assertTrue(task.created_at)  # Check timestamp

    def test_task_str(self):
        task = Task.objects.create(title="String Task")
        self.assertEqual(str(task), "String Task")


class TaskViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Existing Task")

    def test_task_list_view(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')
        self.assertContains(response, "Existing Task")

    def test_task_create_view_get(self):
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_form.html')

    def test_task_create_view_post(self):
        response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'Description',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertEqual(Task.objects.count(), 2) # 1 existing + 1 new
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view_get(self):
        response = self.client.get(reverse('task-update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_form.html')

    def test_task_update_view_post(self):
        response = self.client.post(reverse('task-update', args=[self.task.id]), {
            'title': 'Updated Title',
            'description': 'Updated Desc',
            'completed': True
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertTrue(self.task.completed)

    def test_task_delete_view_get(self):
        response = self.client.get(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_confirm_delete.html')

    def test_task_delete_view_post(self):
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
