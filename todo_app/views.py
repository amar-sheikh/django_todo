from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

class TodoListView(ListView):
    model = Todo
    template_name = 'todo/list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.all()

class TodoCreateView(CreateView):
    model = Todo
    fields = ['task_name', 'task_description', 'is_completed']
    template_name = 'todo/form.html'
    success_url = reverse_lazy('todo_list')

class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['task_name', 'task_description', 'is_completed']
    template_name = 'todo/form.html'
    success_url = reverse_lazy('todo_list')

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/confirm_delete.html'
    success_url = reverse_lazy('todo_list')
