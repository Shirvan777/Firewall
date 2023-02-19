from django import forms  
from NSA.models import Rules
class RulesForm(forms.ModelForm):  
    class Meta:  
        model = Rules 
        fields = "__all__"
         #["source_ip","dest_ip","source_port","dest_port","PROTOCOL_TYPES","ACTION"]  
    # def clean(self):
         
    #     # extract the username and text field from the data
    #     source_ip = self.cleaned_data.get('source_ip')
    #     dest_ip = self.cleaned_data.get('dest_ip')
 
    #     # conditions to be met for the username length
    #     k = 0
    #     for i in source_ip:
    #         if i == ".":
    #             k += 1
    #     if k != 3:    
    #         self._errors['source_ip'] = self.error_class([
    #             'Source Ip is not valid'])
    #     y = 0
    #     for i in dest_ip:
    #         if i == ".":
    #             y += 1
    #     if y != 3:    
    #         self._errors['dest_ip'] = self.error_class([
    #             'Destination Ip is not valid'])
 
    #     # return any errors if found
    #     return self.cleaned_data