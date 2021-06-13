from itertools import product
from wtforms import fields
from flask_wtf import FlaskForm
from shop.admin.routes import brands
from flask import redirect,render_template,url_for, flash, request, session, current_app, session
from shop import db, app, photos, search
from .models import Brand, Category, Addproduct
from sqlalchemy.exc import IntegrityError
from .forms import Addproducts 
import secrets
import os


def barnds():
    barnds = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return barnds

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories




@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products= Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)  
    return render_template('products/index.html', products=products, barnds=barnds(), categories=categories())

@app.route('/result')
def result():   
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name', 'description'] , limit=6)
    return render_template('products/result.html', products=products, barnds=barnds(), categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product, barnds=barnds() ,categories=categories())


@app.route('/brand/<int:id>')
def get_brand(id):
   brand = Addproduct.query.filter_by(brand_id=id)
   return render_template('products/index.html',brand=brand, barnds=barnds(), categories=categories() )


@app.route('/categories/<int:id>')
def get_category(id):
    get_cat_prod = Addproduct.query.filter_by(category_id=id)
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories(), barnds=barnds())



@app.route('/addbrand', methods=['POST', 'GET'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/updatebrand.html', title='Update brand',brands='brands',updatebrand=updatebrand)



@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit(brand)
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        try:
            db.session.add(cat)
            flash(f'The category {getbrand} was added to your database', 'success')
            db.session.commit()
        except IntegrityError:
            db.session.rollback  
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/updatebrand.html', title='Update category Page',updatecat=updatecat)


@app.route('/deletecategory/<int:id>', methods=['GET','POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The category {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The category {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        color = form.color.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'))
        image_2 = photos.save(request.files.get('image_2'))
        image_3 = photos.save(request.files.get('image_3'))
        addproduct = Addproduct(name=name, price=price, discount=discount, stock=stock, color=color, description=description, 
            brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3 )
        db.session.add(addproduct)
        db.session.commit()
        flash(f'The product {name} has been added to your database', 'success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.color = form.color.data
        product.description = form.description.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                 os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                 product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                 product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                 os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                 product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                 product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                 os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                 product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                 product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.description
   # brand = product.brand.name
    #category = product.category.name 
    return render_template('products/updateproduct.html', form=form, title='Update Product',getproduct=product, product=product, brands=brands, categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','danger')
    return redirect(url_for('admin'))