from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, CartItem, Order, OrderItem, Review
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import OrderForm, ReviewForm

# Create your views here.

def is_admin(user):
    return user.is_staff  # або user.groups.filter(name='admin').exists()



def home(request):
    popular_dishes = Dish.objects.filter(is_popular=True)[:5]
    return render(request, 'main/home.html', {'popular_dishes': popular_dishes})

def menu(request):
    sushi_sets = Dish.objects.filter(category='Сети')
    drinks = Dish.objects.filter(category='Напої')
    desserts = Dish.objects.filter(category='Десерти')
    return render(request, 'menu.html', {
        'sushi_sets': sushi_sets,
        'drinks': drinks,
        'desserts': desserts,
    })

def dish_detail(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    reviews = Review.objects.filter(dish=dish, approved=True)
    return render(request, 'dish_detail.html', {'dish': dish, 'reviews': reviews})

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, dish=dish)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('menu')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        item.quantity = max(1, quantity)
        item.save()
    return redirect('cart')


@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('menu')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    dish=item.dish,
                    quantity=item.quantity,
                    price=item.dish.price
                )
            cart_items.delete()
            return render(request, 'order_confirmation.html', {'order': order})
    else:
        form = OrderForm()

    total = sum(item.dish.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total': total})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def repeat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    new_order = order.repeat_order()
    return redirect('checkout')


@login_required
def leave_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.dish = dish
            review.approved = True  # щоб одразу показувався
            review.save()
            return redirect('dish_detail', dish_id=dish.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/leave_review.html', {'form': form, 'dish': dish})


@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')\

@user_passes_test(lambda u: u.is_staff)
def review_list(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    reviews = Review.objects.filter(dish=dish, approved=True)
    return render(request, 'main/review_list.html', {'dish': dish, 'reviews': reviews})

@user_passes_test(lambda u: u.is_staff)
def approve_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.approved = True
    review.save()
    return redirect('review_moderation')

@login_required
def review_list(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    reviews = Review.objects.filter(dish=dish, approved=True)
    return render(request, 'main/review_list.html', {'dish': dish, 'reviews': reviews})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Перевірка: тільки автор може видалити свій коментар
    if review.user != request.user:
        return redirect('dish_detail', dish_id=review.dish.id)

    if request.method == 'POST':
        dish_id = review.dish.id
        review.delete()
        return redirect('dish_detail', dish_id=dish_id)

    return render(request, 'reviews/confirm_delete.html', {'review': review})
