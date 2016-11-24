# -*- coding: utf-8 -*-

from flask_principal import RoleNeed, Permission

admin = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator'))
auth = Permission(RoleNeed('authenticated'))

# this is assigned when you want to block a permission to all
# never assing this role to anyone !
null = Permission(RoleNeed('null'))
