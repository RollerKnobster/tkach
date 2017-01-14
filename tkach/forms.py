from flask_wtf import Form
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired


class ArrayForm(Form):
    array = TextAreaField('Enter your array: ', validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        return True
