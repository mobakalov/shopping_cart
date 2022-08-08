from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.models import User, Product, cart
from flask_login import login_required, current_user




shop = Blueprint('shop', __name__, template_folder='shoptemplates')


@shop.route('/shop', methods=['GET', 'POST'])
@login_required
def show_inventory():
    ## Find all our items that we sell
    items=Product.query.all()
    return render_template('shop.html', items=items)


@shop.route('/cart', methods=['GET', 'POST'])
@login_required
def my_cart():
    # get all the items user has added to their cart
    cart_items = current_user.shop
    return render_template('cart.html',cart_items=cart_items)


@shop.route('/add_item/<int:id>', methods=['GET', 'POST'])
@login_required
def add_item(id):
    user = current_user
    item = Product.query.get(id)
    user.add_to_cart(item)
    return render_template('cart.html', cart_items=user.shop)

@shop.route('/remove_item/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_item(id):
    deleted = cart.query.get((current_user.id,id))
    if deleted:
        deleted.delete()
        flash(f'You have removed item {id} from cart', 'warning')
    return render_template('cart.html', cart_items=current_user.shop)

@shop.route('/clear_cart', methods=['GET', 'POST'])
@login_required
def clear_cart():
    deleted = cart.query.filter_by(user_id=current_user.id).all()
    if deleted:
        for i in deleted:
            i.delete()
            flash(f'You have removed item {id} from cart', 'warning')
    return render_template('cart.html', cart_items=current_user.shop)
