def userinfo(request):
    from .models import Employee
    if request.user.is_authenticated():
        emp = Employee.objects.get(user=request.user)

        return {
            'user': request.user,
            'emp': emp
        }
    return {}