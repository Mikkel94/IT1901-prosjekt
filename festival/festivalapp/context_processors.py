def userinfo(request):
    from .models import Employee
    if request.user.is_authenticated() and not 'admin' in request.path:
        emp = Employee.objects.get(user=request.user)
        sc = emp.employee_status

        return {
            'user': request.user,
            'emp': emp,
            'sc': sc
        }
    return {}