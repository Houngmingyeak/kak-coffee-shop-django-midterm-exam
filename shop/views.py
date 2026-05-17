from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Coffee
from .forms import CoffeeForm


def coffee_list(request):
    """Display all coffee items with optional search/filter."""
    coffees = Coffee.objects.all()

    # Search by name
    query = request.GET.get('q', '')
    if query:
        coffees = coffees.filter(name__icontains=query)

    # Filter by category
    category = request.GET.get('category', '')
    if category:
        coffees = coffees.filter(category=category)

    # Filter by availability
    available_only = request.GET.get('available', '')
    if available_only == 'true':
        coffees = coffees.filter(is_available=True)

    categories = Coffee.CATEGORY_CHOICES
    context = {
        'coffees': coffees,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'available_only': available_only,
    }
    return render(request, 'coffee_list.html', context)


def add_coffee(request):
    """Add a new coffee item."""
    if request.method == 'POST':
        form = CoffeeForm(request.POST, request.FILES)
        if form.is_valid():
            coffee = form.save()
            messages.success(request, f'"{coffee.name}" has been added successfully!')
            return redirect('coffee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CoffeeForm()

    return render(request, 'add_coffee.html', {'form': form})


def update_coffee(request, pk):
    """Update an existing coffee item."""
    coffee = get_object_or_404(Coffee, pk=pk)

    if request.method == 'POST':
        form = CoffeeForm(request.POST, request.FILES, instance=coffee)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{coffee.name}" has been updated successfully!')
            return redirect('coffee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CoffeeForm(instance=coffee)

    return render(request, 'update_coffee.html', {'form': form, 'coffee': coffee})


def delete_coffee(request, pk):
    """Delete a coffee item."""
    coffee = get_object_or_404(Coffee, pk=pk)

    if request.method == 'POST':
        name = coffee.name
        coffee.delete()
        messages.success(request, f'"{name}" has been deleted successfully!')
        return redirect('coffee_list')

    return render(request, 'delete_coffee.html', {'coffee': coffee})
