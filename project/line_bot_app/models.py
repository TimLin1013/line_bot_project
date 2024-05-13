from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class 個人_Table(models.Model):
    個人_id = models.IntegerField(primary_key=True)
    姓名 = models.TextField()

    class Meta:
        managed = True
        db_table = '個人_table'

class 群組_Table(models.Model):
    群組_id = models.IntegerField(db_column='群組_ID', primary_key=True)  # Field name made lowercase.
    群組名稱 = models.TextField()

    class Meta:
        managed = False
        db_table = '群組_table'

class 個人_群組_LinkTable(models.Model):
    個人_群組_link_table_id = models.IntegerField(db_column='個人_群組_link_table_ID',
                                                  primary_key=True)  # Field name made lowercase.
    群組 = models.ForeignKey(群組_Table, models.DO_NOTHING, db_column='群組_ID')  # Field name made lowercase.
    個人 = models.ForeignKey(個人_Table, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = '個人_群組_link_table'


class 類別_個人_Table(models.Model):
    類別_個人_id = models.IntegerField(db_column='類別_個人_ID', primary_key=True)  # Field name made lowercase.
    類別名稱 = models.TextField()
    類別描述 = models.TextField()

    class Meta:
        managed = False
        db_table = '類別_個人_table'

class 個人_類別_LinkTable(models.Model):
    類別_個人 = models.OneToOneField(類別_個人_Table, models.DO_NOTHING, db_column='類別_個人_ID', primary_key=True)  # Field name made lowercase.
    個人 = models.ForeignKey(個人_Table, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = '個人_類別_link_table'
        unique_together = (('類別_個人', '個人'),)

class 子類別_個人_Table(models.Model):
    子類別_個人_id = models.IntegerField(db_column='子類別_個人_ID', primary_key=True)  # Field name made lowercase.
    子類別名稱 = models.TextField()
    子類別描述 = models.TextField()
    類別_個人 = models.ForeignKey(類別_個人_Table, models.DO_NOTHING, db_column='類別_個人_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '子類別_個人_table'

class 個人帳目_收入_支出_Table(models.Model):
    個人帳目_id = models.IntegerField(db_column='個人帳目_ID', primary_key=True)  # Field name made lowercase.
    項目名稱 = models.TextField(blank=True, null=True)
    交易類型_收入_支出 = models.TextField(blank=True, null=True)
    日期 = models.TextField(blank=True, null=True)
    地點 = models.TextField(blank=True, null=True)
    金額 = models.TextField(blank=True, null=True)
    詳細資訊_備註 = models.TextField(blank=True, null=True)
    是否完成確認動作 = models.TextField(blank=True, null=True)
    類別_個人 = models.ForeignKey(類別_個人_Table, models.DO_NOTHING, db_column='類別_個人_ID', blank=True, null=True)  # Field name made lowercase.
    個人 = models.ForeignKey(個人_Table, models.DO_NOTHING, blank=True, null=True)
    子類別_個人 = models.ForeignKey(子類別_個人_Table, models.DO_NOTHING, db_column='子類別_個人_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '個人帳目_收入_支出_table'

class 類別_群組_Table(models.Model):
    類別_群組_id = models.IntegerField(db_column='類別_群組_ID', primary_key=True)  # Field name made lowercase.
    類別名稱 = models.TextField()
    類別描述 = models.TextField()

    class Meta:
        managed = False
        db_table = '類別_群組_table'

class 群組_類別_LinkTable(models.Model):
    群組 = models.ForeignKey(群組_Table, models.DO_NOTHING, db_column='群組_ID')  # Field name made lowercase.
    類別_群組 = models.ForeignKey(類別_群組_Table, models.DO_NOTHING, db_column='類別_群組_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '群組_類別_link_table'

class 子類別_群組_Table(models.Model):
    子類別_群組_id = models.IntegerField(db_column='子類別_群組_ID', primary_key=True)  # Field name made lowercase.
    子類別名稱 = models.TextField()
    子類別描述 = models.TextField(blank=True, null=True)
    類別_群組 = models.ForeignKey(類別_群組_Table, models.DO_NOTHING, db_column='類別_群組_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '子類別_群組_table'

class 群組帳目_Table(models.Model):
    群組帳目_id = models.IntegerField(primary_key=True)
    項目名稱 = models.TextField()
    交易類型_收入_支出 = models.TextField()
    日期 = models.TextField()
    地點 = models.TextField()
    金額 = models.TextField()
    詳細資訊_備註 = models.TextField()
    是否完成確認動作 = models.TextField()
    群組 = models.ForeignKey(群組_Table, models.DO_NOTHING, db_column='群組_ID')  # Field name made lowercase.
    類別_群組 = models.ForeignKey(類別_群組_Table, models.DO_NOTHING, db_column='類別_群組_ID')  # Field name made lowercase.
    子類別_群組 = models.ForeignKey(子類別_群組_Table, models.DO_NOTHING, db_column='子類別_群組_ID')  # Field name made lowercase.
    付款人 = models.ForeignKey(個人_Table, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = '群組帳目_table'

class 分帳資訊_應收_應付_Table(models.Model):
    分帳資訊_id = models.IntegerField(db_column='分帳資訊_ID', primary_key=True)  # Field name made lowercase.
    金額 = models.TextField(blank=True, null=True)
    預先付錢 = models.CharField(max_length=45, blank=True, null=True)
    是否付清_還錢 = models.TextField(blank=True, null=True)
    付款人 = models.ForeignKey(個人_Table, models.DO_NOTHING, blank=True, null=True, related_name='付款人')
    欠款人 = models.ForeignKey(個人_Table, models.DO_NOTHING, blank=True, null=True, related_name='欠款人')
    群組帳目 = models.ForeignKey(群組帳目_Table, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '分帳資訊_應收_應付_table'









