from rest_framework import permissions


class MixedPermissionMixin(object):
    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            return [permission() for permission in
                    self.permission_classes_by_action[self.action]]
        except:
            if self.action:
                action_func = getattr(self, self.action, {})
                actions_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = actions_func_kwargs.get(
                    'permission_classes')
            else:
                permission_classes = None

            return [permission() for permission in (permission_classes or self.permission_classes)]
