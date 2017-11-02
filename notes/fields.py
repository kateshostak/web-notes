from django import forms


class DataListWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(DataListWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(DataListWidget, self).render(name, value, attrs=attrs)
        data_list = f'<datalist id="list__{self._name}">'
        for item in self._list:
            data_list += f'<option value="{item[0]}">'
        data_list += '</datalist>'

        return (text_html + data_list)
