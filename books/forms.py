#coding:utf-8
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label='用户名', error_messages={'required':'请输入用户名'}, widget=forms.TextInput(attrs={'placeholder':'用户名'}))
    password = forms.CharField(required=True, label='密码', error_messages={'required':'请输入密码'}, widget=forms.PasswordInput(attrs={'placeholder':'密码'}))
    password2 = forms.CharField(required=True, label='再次输入密码', error_messages={'required':'请再次输入密码'}, widget=forms.PasswordInput(attrs={'placeholder':'再次输入密码'}))
    email = forms.EmailField(label='邮箱')
    
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='用户名', error_messages={'required':'请输入用户名'}, widget=forms.TextInput(attrs={'placeholder':'用户名'}))
    password = forms.CharField(required=True, label='密码', error_messages={'required':'请输入密码'}, widget=forms.PasswordInput(attrs={'placeholder':'密码'}))

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(required=True, label='旧密码', error_messages={'required':'请输入旧密码'}, widget=forms.PasswordInput(attrs={'placeholder':'旧密码'}))
    newpassword = forms.CharField(required=True, label='新密码', error_messages={'required':'请输入新密码'}, widget=forms.PasswordInput(attrs={'placeholder':'新密码'}))
    newpassword1 = forms.CharField(required=True, label='再次输入新密码', error_messages={'required':'请再次输入新密码'}, widget=forms.PasswordInput(attrs={'placeholder':'再次输入新密码'}))

class MsgBoardForm(forms.Form):
    subject = forms.CharField(required=True, label='主题', error_messages={'required':'请输入主题!'})
    content = forms.CharField(required=True, label='内容', error_messages={'required':'请输入主题!'}, widget=forms.Textarea)
