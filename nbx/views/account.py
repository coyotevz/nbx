# -*- coding: utf-8 -*-

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, session, url_for)
from flask_principal import AnonymousIdentity, Identity, identity_changed

from nbx.forms import LoginForm
from nbx.models import User, db
from nbx.permissions import auth

account = Blueprint('account', __name__)

@account.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm(username=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.query.authenticate(form.username.data,
                                                      form.password.data)
        if user and authenticated:
            session.permanent = form.remember.data

            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            flash("Welcome back, %(name)s" % {'name': user.username}, "success")
            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('user.index', username=user.username)
            return redirect(next_url)
        else:
            flash("Sorry, invlid login", "error")
    return render_template('account/login.html', form=form)

@account.route('/logout/')
def logout():
    flash("You are now logged out", "success")
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('supplier.index'))

@account.route('/changepw/', methods=('GET', 'POST'))
def change_password():

    user = None

    if g.user:
        user = g.user

    elif 'activation_key' in request.values:
        user = User.query.filter_by(activation_key=request.values['activation_key']).first()

    if user is None:
        abort(403)

    form = ChangePasswordForm(activation_key=user.activation_key)

    if form.validate_on_submit():

        user.password = form.password.data
        user.activation_key = None

        db.session.commit()

        flash("Your password has been changed, please log in again", "success")
        return redirect(url_for('account.login'))

    return render_template('account/change_password.html', form=form)

@account.route('/edit/', methods=('GET', 'POST'))
@auth.require(401)
def edit():

    form = EditAccountForm(g.user)

    if form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.commit()

        flash("Your account has been updated", "success")
        return redirect(url_for('supplier.index'))

    return render_template('account/edit.html', form=form)

@account.route('/delete/', methods=('GET', 'POST'))
@auth.require(401)
def delete():

    # confirm password
    form = DeleteAccountForm()

    if form.validate_on_submit():
        db.session.delete(g.user)
        db.session.commit()

        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())

        flash("Your account has been deleted", "success")
        return redirect(url_for('supplier.index'))

    return render_template('account/delete_account.html', form=form)
