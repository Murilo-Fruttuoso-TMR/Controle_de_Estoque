from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models import User
from app.services import log_action


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active_user:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            log_action(
                user,
                "login",
                f"Usuário {user.username} autenticou no sistema.",
                entity_type="user",
                entity_id=user.id,
                ip_address=request.remote_addr,
            )
            flash(f"Bem-vindo, {user.full_name}.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.dashboard"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    log_action(
        current_user,
        "logout",
        f"Usuário {current_user.username} encerrou a sessão.",
        entity_type="user",
        entity_id=current_user.id,
        ip_address=request.remote_addr,
    )
    logout_user()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for("auth.login"))
