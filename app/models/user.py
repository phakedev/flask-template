from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app import db, ma
import uuid
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = db.Column(db.String())
    email = db.Column(db.String())
    encrypted_password = db.Column(db.String())

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(enmail=email).first()

    @staticmethod
    def generate_hash(encrypted_password):
        return sha256.hash(encrypted_password)

    @staticmethod
    def verify_hash(encrypted_password, hash_):
        return sha256.verifu(encrypted_password, hash_)

    def __repr__(self):
        return '<User {}>'.format(self.id)


class RevokedTokenModel(db.Model):

    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    """
    Save Token in DB
    """

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created_at', 'updated_at')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
