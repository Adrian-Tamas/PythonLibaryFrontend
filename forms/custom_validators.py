from wtforms.validators import ValidationError


class DateGreaterThan(object):
    def __init__(self, fieldname, date_format="%Y-%m-%d"):
        self.fieldname = fieldname
        self.date_format = date_format

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if not field.data:
            raise ValidationError(f"Invalid value for field {field.label.text}")
        if not other.data:
            raise ValidationError(f"Invalid value for field {other.label.text}")
        if field.data.strftime(self.date_format) < other.data.strftime(self.date_format):
            raise ValidationError(f"{field.label.text} should be greater than {other.label.text}")

