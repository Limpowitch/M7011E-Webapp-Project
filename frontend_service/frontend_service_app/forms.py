import requests
from django import forms

class RecipeForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=[])  # Choices are populated dynamically
    description = forms.CharField(widget=forms.Textarea)
    time = forms.IntegerField()
    cost = forms.IntegerField()
    kcal = forms.IntegerField()
    portions = forms.IntegerField()
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fetch category choices from the backend API
        try:
            # Debugging: Check if the API call works
            print("Fetching categories from backend...")
            response = requests.get('http://localhost:8001/categories/')
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.json()}")
            if response.status_code == 200:
                categories = response.json()
                self.fields['category'].choices = [(c['id'], c['name']) for c in categories]
            else:
                self.fields['category'].choices = []
        except requests.exceptions.RequestException:
            self.fields['category'].choices = []
