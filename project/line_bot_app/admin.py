from django.contrib import admin
from line_bot_app.models import *

admin.site.register(個人_Table)
admin.site.register(群組_Table)
admin.site.register(個人_群組_LinkTable)
admin.site.register(類別_個人_Table)
admin.site.register(個人_類別_LinkTable)
admin.site.register(子類別_個人_Table)
admin.site.register(個人帳目_收入_支出_Table)
admin.site.register(類別_群組_Table)
admin.site.register(群組_類別_LinkTable)
admin.site.register(子類別_群組_Table)
admin.site.register(群組帳目_Table)
admin.site.register(分帳資訊_應收_應付_Table)
