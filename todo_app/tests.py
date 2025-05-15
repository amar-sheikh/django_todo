from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Todo

class TestTodo(TestCase):

    def test_create_todo(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            task_description='Description',
            is_completed=True
        )
        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertEqual(self.todo.task_description, 'Description')
        self.assertTrue(self.todo.is_completed)
    
    def test_create_todo_with_empty_task_name_raises_validation_error(self):
        self.todo = Todo.objects.create(
            task_name='',
            task_description='Description',
            is_completed=True
        )
        
        with self.assertRaises(ValidationError):
            self.todo.full_clean()
    
    def test_create_todo_with_short_task_name_raises_validation_error(self):
        self.todo = Todo.objects.create(
            task_name='Tsk',
            task_description='Description',
            is_completed=True
        )
        
        with self.assertRaises(ValidationError):
            self.todo.full_clean()
    
    def test_create_todo_with_empty_description(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            task_description='',
            is_completed=True
        )

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertEqual(self.todo.task_description, '')
        self.assertTrue(self.todo.is_completed)
    
    def test_create_todo_without_description(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            is_completed=True
        )

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertIsNone(self.todo.task_description)
        self.assertTrue(self.todo.is_completed)
    
    def test_create_todo_without_is_completed(self):
        self.todo = Todo.objects.create(
            task_name='Task',
            task_description='Description',
        )

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertEqual(self.todo.task_description, 'Description')
        self.assertFalse(self.todo.is_completed)
    
    def test_create_todo_with_task_name_only(self):
        self.todo = Todo.objects.create(task_name='Task')

        self.todo.full_clean()
        self.assertEqual(self.todo.task_name, 'Task')
        self.assertIsNone(self.todo.task_description)
        self.assertFalse(self.todo.is_completed)

class TodoViewTests(TestCase):
    def setUp(self):
        self.todo_completed = Todo.objects.create(
            task_name='Completed Task',
            task_description='Done',
            is_completed=True
        )
        self.todo_not_completed = Todo.objects.create(
            task_name='Incomplete Task',
            task_description='Not done yet',
            is_completed=False
        )

    def test_todo_list_default_filter_shows_completed(self):
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, self.todo_completed.task_name)
        self.assertNotContains(response, self.todo_not_completed.task_name)

    def test_todo_list_filter_all(self):
        response = self.client.get(reverse('todo_list') + '?filter=all')
        self.assertContains(response, self.todo_completed.task_name)
        self.assertContains(response, self.todo_not_completed.task_name)

    def test_todo_list_filter_not_completed(self):
        response = self.client.get(reverse('todo_list') + '?filter=not_completed')
        self.assertNotContains(response, self.todo_completed.task_name)
        self.assertContains(response, self.todo_not_completed.task_name)

    def test_todo_list_filter_completed(self):
        response = self.client.get(reverse('todo_list') + '?filter=completed')
        self.assertContains(response, self.todo_completed.task_name)
        self.assertNotContains(response, self.todo_not_completed.task_name)
    
    def test_todo_search_by_task_name_exact_match(self):
        response = self.client.get(reverse('todo_list') + '?search=Completed Task&filter=all')
        self.assertContains(response, self.todo_completed.task_name)
        self.assertNotContains(response, self.todo_not_completed.task_name)

    def test_todo_search_by_task_name_partial_match(self):
        response = self.client.get(reverse('todo_list') + '?search=Incomplete&filter=all')
        self.assertContains(response, self.todo_not_completed.task_name)
        self.assertNotContains(response, self.todo_completed.task_name)

    def test_todo_search_with_filter_completed(self):
        response = self.client.get(reverse('todo_list') + '?search=Task&filter=completed')
        self.assertContains(response, self.todo_completed.task_name)
        self.assertNotContains(response, self.todo_not_completed.task_name)

    def test_todo_search_no_results(self):
        response = self.client.get(reverse('todo_list') + '?search=Nonexistent&filter=all')
        self.assertNotContains(response, self.todo_completed.task_name)
        self.assertNotContains(response, self.todo_not_completed.task_name)

    def test_create_todo(self):
        response = self.client.post(reverse('todo_create'), {
            'task_name': 'New Task',
            'task_description': 'New description',
            'is_completed': False
        })
        self.assertEqual(Todo.objects.count(), 3)
        self.assertRedirects(response, reverse('todo_list'))

    def test_create_todo_with_invalid_data(self):
        response = self.client.post(reverse('todo_create'), {
            'task_name': '',
            'task_description': 'New description',
            'is_completed': False
        })
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'task_name', 'This field is required.')

    def test_update_todo(self):
        response = self.client.post(reverse('todo_update', args=[self.todo_not_completed.id]), {
            'task_name': 'Updated Task',
            'task_description': 'Updated desc',
            'is_completed': True
        })
        self.assertRedirects(response, reverse('todo_list'))
        self.todo_not_completed.refresh_from_db()
        self.assertEqual(self.todo_not_completed.task_name, 'Updated Task')
        self.assertTrue(self.todo_not_completed.is_completed)

    def test_update_todo_with_invalid_data(self):
        response = self.client.post(reverse('todo_update', args=[self.todo_not_completed.id]), {
            'task_name': '',
            'task_description': 'Updated desc',
            'is_completed': True
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'task_name', 'This field is required.')
        self.todo_not_completed.refresh_from_db()
        self.assertEqual(self.todo_not_completed.task_name, 'Incomplete Task')
        self.assertEqual(self.todo_not_completed.task_description, 'Not done yet')
        self.assertFalse(self.todo_not_completed.is_completed)

    def test_delete_todo(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo_completed.id]))
        self.assertEqual(Todo.objects.count(), 1)
        self.assertRedirects(response, reverse('todo_list'))

    def test_delete_todo_with_invalid_id(self):
        invalid_id = 9999
        response = self.client.post(reverse('todo_delete', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)