from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Todo

class TodoListView(ListView):
    model = Todo
    template_name = 'todo/list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        queryset = Todo.objects.all()
        filter_val = self.request.GET.get('filter', 'completed')
        query = self.request.GET.get('search')

        if filter_val == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif filter_val == 'not_completed':
            queryset = queryset.filter(is_completed=False)

        if query:
            queryset = queryset.filter(task_name__icontains=query)

        return queryset

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
