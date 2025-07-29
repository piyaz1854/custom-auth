from users.models import AccessRule, BusinessElement


def has_permission(user, action, element_name, is_owner=False):
    if not user.is_authenticated:
        return False 

    if not user.role:
        return False 

    try:
        element = BusinessElement.objects.get(name=element_name)
        rule = AccessRule.objects.get(role=user.role, element=element)
    except BusinessElement.DoesNotExist:
        return False
    except AccessRule.DoesNotExist:
        return False

    if action == 'read':
        return rule.read_all_permission if is_owner else rule.read_my_permission
    elif action == 'create':
        return rule.create_permission
    elif action == 'update':
        return rule.update_all_permission if is_owner else rule.update_my_permission
    elif action == 'delete':
        return rule.delete_all_permission if is_owner else rule.delete_my_permission

    return False
