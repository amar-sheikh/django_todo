from django.test import TestCase
from django.core.exceptions import ValidationError
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