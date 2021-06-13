from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, BooleanField, DecimalField, TextAreaField, StringField,IntegerField, validators
from wtforms.validators import DataRequired



class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Discription', [validators.DataRequired()])
    color = TextAreaField('Colors', [validators.DataRequired()])


    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], 'Images only please')])
   
