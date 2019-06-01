from app.auth.models import User, Permission, AnonymousUser, Role
from basics import BasicTestCaseSettings

class UserModelTestCase(BasicTestCaseSettings):

    def setUp(self):
        super().setUp()
        Role.insert_roles()
        self.user = User(email="user@email.com", password='randompass')
        self.admin_role = Role.query.filter_by(name="Administrator").first()
        self.user_role = Role.query.filter_by(name="User").first()

    def test_password_setter(self):
        self.assertTrue(self.user.password_hash is not None)

    def test_password_getter(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification(self):
        self.assertTrue(self.user.verify_password('randompass'))
        self.assertFalse(self.user.verify_password('anotherpass'))

    def test_password_hash_is_random(self):
        another_user = User(password='randompass')
        self.assertNotEqual(self.user.password_hash, another_user.password_hash)

    def test_user_has_a_role(self):
        self.assertTrue(self.user.role_id is not None)

    def test_user_role(self):
        role = Role.query.get(self.user.role_id)
        self.assertEqual(role.name, self.user_role.name)

    def test_user_permissions(self):
        self.assertTrue(self.user.can(Permission.COMMENT))
        self.assertFalse(self.user.can(Permission.ADMIN))

    def test_anonymous_user_permissions(self):
        anonymous_user = AnonymousUser()
        self.assertFalse(anonymous_user.can(Permission.COMMENT))
        self.assertFalse(anonymous_user.can(Permission.ADMIN))