from flask import Blueprint

from .models import User


auth = Blueprint('auth', __name__)

from . import views