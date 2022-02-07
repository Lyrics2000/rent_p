from django import forms
from django.core.exceptions import ValidationError

class CashAtHand(forms.Form):
    cash_at_hand = forms.IntegerField(widget=forms.NumberInput(
        attrs={  "type": "number", "style" : " color:#000000;width:100%;font-size:16px;border: 2px solid red;padding:10px"  , "placeholder" : "Cash At Hand" , "id" : "form_control_lgn_input" 
        
        }
    ))

    def clean(self,value):
        # data from the form is fetched using super function
        data = self.cleaned_data['cash_at_hand']
        if float(data)<= float(value):
            raise ValidationError("Enter Amount greater than delivery Amount")
        return data
        

    