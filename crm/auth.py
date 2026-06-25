PERMISSIONS = {
    'Admin': ['create', 'update', 'delete', 'view', 'restore'],
    'Sales': ['create', 'view', 'update'],
    'Viewer': ['view']
}
def has_permission(role, action): return action in PERMISSIONS.get(role, [])
