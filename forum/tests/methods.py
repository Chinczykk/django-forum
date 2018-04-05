def check_form_for_errors(self, data, errors, Form):
    form = Form(data)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors, errors)